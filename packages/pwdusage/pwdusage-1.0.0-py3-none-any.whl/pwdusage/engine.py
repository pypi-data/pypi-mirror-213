#!/usr/bin/env python
# UsageEngine Module - Class for usage calculations.
# -*- coding: utf-8 -*-
"""
 Author: BuongiornoTexas
 For more information see https://github.com/jasonacox/pypowerwall

"""
# cspell: ignore pydantic simples astype simplejson rollforward pydatetime
# cspell: ignore dayofweek pwdusage

# I've gone back and forth on treating this as a module with globals or a class.
# I've ended up going class as there is enough going on that it will just
# be easier to work as a class even if a lot of elements ore fairly static.
# And ... given it is run in threading context, it also makes handling thread locking
# quite a lot simpler.

# import datetime
import simplejson  # type: ignore

from argparse import ArgumentParser

from itertools import pairwise
from threading import Lock
from typing import Any, Optional, Type, Union
from zoneinfo import ZoneInfo
from datetime import datetime, timezone, time
from pandas import (  # type:ignore
    DataFrame,
    Series,
    notnull,
    offsets,
    Timestamp,
    DatetimeIndex,
    Timedelta,
)
from numpy import int64 as np_int64
from dataclasses import dataclass, InitVar
from dataclasses import replace as dc_replace
from os import getenv
from logging import DEBUG as LOG_DEBUG

from influxdb_client import InfluxDBClient, QueryApi  # type: ignore

from pwdusage.common import PDColName, log
from pwdusage.base_agent import UsageAgent

DEFAULT_CONFIG = "./usage.json"
SUPPLY_PRIORITY = "supply_priority"
WEEK_ANCHORS = {
    "MONTH": -1,
    "MON": 0,
    "TUE": 1,
    "WED": 2,
    "THU": 3,
    "FRI": 4,
    "SAT": 5,
    "SUN": 6,
}
YEAR_ANCHORS = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}

# InfluxDB _time will become our index.
INFLUX_TIME = "_time"
# Link demand priority to home breakdown
SUPPLY_TO_DEMAND = {
    PDColName.GRID_SUPPLY: PDColName.GRID_TO_HOME,
    PDColName.PW_SUPPLY: PDColName.PW_TO_HOME,
    PDColName.SOLAR_SUPPLY: PDColName.SOLAR_TO_HOME,
}
# Residual order.
RESIDUALS = [
    PDColName.RESIDUAL_DEMAND_1,
    PDColName.RESIDUAL_DEMAND_2,
    PDColName.RESIDUAL_DEMAND_FINAL,
]
# Map influx column names to pandas column names.
INFLUX_TO_PANDAS = {
    "from_grid": PDColName.GRID_SUPPLY.value,
    "to_grid": PDColName.GRID_EXPORT.value,
    "from_pw": PDColName.PW_SUPPLY.value,
    "solar": PDColName.SOLAR_SUPPLY.value,
    "home": PDColName.HOME_DEMAND.value,
}


def safe_iso_utc_to_dt(
    iso_utc: Union[str, datetime], new_tz: Optional[ZoneInfo] = None
) -> datetime:
    # iso_utc should either be the UTC string format with trailing Z, or utc datetime.
    # As python doesn't deal with trailing Z until 3.11, handle it manually to
    # allow for older installations. Returns UTC time unless provide with a
    # timezone.
    if isinstance(iso_utc, str):
        if iso_utc[-1] != "Z":
            raise ValueError(f"Expected isoformat utc time ending Z. Got {iso_utc}")
        # Create safe utc time.
        dt = datetime.fromisoformat(iso_utc[:-1])
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = iso_utc

    if new_tz is not None:
        dt = dt.astimezone(new_tz)

    return dt


@dataclass
class TariffPeriod:
    # Hour range in a day when tariff name applies.
    tariff: str
    start: time
    end: time


@dataclass
class TariffSchedule:
    # A tariff schedule that specifies:
    #   - The days of the week that the schedule applies for.
    #   - A table of the different tariff periods in each day of the schedule.
    name: str
    days: set[int]
    periods: list[TariffPeriod]

    def tariff_defined(self, tariff: str) -> bool:
        for t_period in self.periods:
            if t_period.tariff == tariff:
                return True

        return False


class UsagePlan:
    # This started as a data class, but with too much going on, has transitioned to
    # a full class. Oddities probably reflect this.
    #
    # Plan name is redundant here, as it is also used as the key in the
    # plan dict, but it's convenient for debugging to have it as part of the
    # object as well.
    _name: str
    # Each plan carries the raw config for user agent specific information.
    _raw_plan_json: dict[str, Any]
    report_cols: list[PDColName]
    # I suspect the agent is more correctly done by some sort of type factory. But
    # that's beyond my current ability, and I expect a small number of agents, so
    # work with a less general structure.
    _agent: Optional[UsageAgent]
    _agent_class: Type[UsageAgent]
    # Season key/subkey is season name/tariff schedule name.
    _seasons: dict[str, dict[str, TariffSchedule]]

    def _get_agent(self) -> None:
        try:
            name = self._raw_plan_json["agent"]
        except KeyError:
            raise KeyError(f"Missing usage agent for usage plan {self._name}.")

        match name:
            case "Simple":
                # follow this structure to add new agents.
                from pwdusage.simple_agent import SimpleAgent

                self._agent_class = SimpleAgent
            case _:
                raise ValueError(f"Unknown agent {name} in usage plane {self._name}")

        if self._agent_class.can_persist():
            # Instantiate persistent agent if allowed.
            self._agent = self._agent_class(plan_json=self.raw_json)
        else:
            self._agent = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def raw_json(self) -> dict[str, Any]:
        # The caller could modify this, but really shouldn't
        return self._raw_plan_json

    @property
    def agent(self) -> UsageAgent:
        if self._agent is not None:
            # persistent agent if available.
            return self._agent

        # Otherwise, dynamic instance
        return self._agent_class(plan_json=self.raw_json)

    def season_defined(self, season: str) -> bool:
        return season in self._seasons

    def season_schedules(self, season: str) -> dict[str, TariffSchedule]:
        return self._seasons[season]

    def tariff_defined(self, season: str, tariff: str) -> bool:
        if season not in self._seasons:
            return False

        for schedule in self._seasons[season].values():
            if schedule.tariff_defined(tariff):
                return True

        return False

    def _init_seasons(self) -> None:
        # CREATE seasons dictionary!
        self._seasons = {}

        if "seasons" not in self._raw_plan_json:
            raise KeyError(f"No seasons defined for usage plan {self._name}")

        prev_season: Optional[dict[str, TariffSchedule]] = None
        for season_name, schedules in self._raw_plan_json["seasons"].items():
            # Create season and local ref for convenience
            self._seasons[season_name] = {}
            season = self._seasons[season_name]

            for schedule_json in schedules:
                # Construct (partial) tariff schedule as kwarg.
                kwarg: dict[str, Any] = {}
                if "schedule" not in schedule_json:
                    raise KeyError(
                        f"A schedule of usage plan '{self._name}/{season_name} is "
                        f"missing a 'schedule': 'name' pair."
                    )
                schedule_name = schedule_json["schedule"]
                # Useful to have name accessible inside entry as well as key.
                kwarg["name"] = schedule_name

                # construct schedule
                if "days" in schedule_json:
                    kwarg["days"] = set(schedule_json["days"])

                # Construct tariff periods.
                if "periods" in schedule_json:
                    periods = list()
                    for this, next in pairwise(schedule_json["periods"].items()):
                        periods.append(
                            TariffPeriod(
                                tariff=this[1],
                                start=time.fromisoformat(this[0]),
                                end=time.fromisoformat(next[0]),
                            )
                        )

                    # For a single entry - pairwise was non-op.
                    # Time value is irrelevant.
                    this = list(schedule_json["periods"].items())[-1]
                    if len(schedule_json["periods"]) == 1:
                        next = this
                    else:
                        next = list(schedule_json["periods"].items())[0]

                    periods.append(
                        TariffPeriod(
                            tariff=this[1],
                            start=time.fromisoformat(this[0]),
                            end=time.fromisoformat(next[0]),
                        )
                    )
                    kwarg["periods"] = periods

                if prev_season is not None and schedule_name in prev_season:
                    # We can construct by replacement
                    season[schedule_name] = dc_replace(
                        prev_season[schedule_name], **kwarg
                    )
                else:
                    # New dataclass.
                    try:
                        season[schedule_name] = TariffSchedule(**kwarg)
                    except:
                        # The alternative to this is to default to all day and/or
                        # every day if periods or days are missing. Not sure which
                        # would be better. Defaulted to requiring users tell us what
                        # they actually want for the first sets in a season.
                        raise ValueError(
                            f"Schedule {schedule_name} for  {self._name}/{season_name} is "
                            f"either missing 'days' or 'periods' entries or contains "
                            f"other errors."
                        )

            # Finally, duplicate any unchanged schedules from previous season.
            if prev_season is not None:
                for schedule_name in prev_season.keys():
                    if schedule_name not in season:
                        # Using dc replace to create a new instance.
                        season[schedule_name] = dc_replace(prev_season[schedule_name])

            prev_season = season

    def __init__(self, plan_json: dict[str, Any]) -> None:
        # Very limited error checking for now. Push back to user for now.
        # Maybe do better input preconditioning in future with
        # something like pydantic (probably not worth the effort)

        self._raw_plan_json = plan_json
        try:
            self._name = plan_json["name"]
        except KeyError:
            raise KeyError(f"Usage plan in input has no 'name' field.")

        self._get_agent()

        self.report_cols = []
        for report in plan_json["report"]:
            pd_col = PDColName.from_str(report)
            if pd_col is not None:
                self.report_cols.append(pd_col)
            else:
                raise ValueError(
                    f"Unrecognised report name '{report}' for usage plan '{self._name}'."
                )

        self._init_seasons()


@dataclass
class CalendarEntry:
    # Start date is redundant here, as it is also used as the key in the
    # UsageEngine calendar dict, but it's convenient for debugging to have it as part
    # of the object as well.
    start_date: datetime
    # the name of the plan to apply.
    plan: str
    # plan season to apply.
    season: str
    # tariff: tariff name -> dict[PDColName, rate].
    tariffs: dict[str, dict[PDColName, float]]
    # plan dict used for post init validation.
    plans: InitVar[dict[str, UsagePlan]]
    # Adding an end date allows the Usage engine to do much work with a single calendar
    # entry rather than requiring a pair of entries.
    end_date: Optional[datetime] = None
    # Likewise, adding a pointer to the plan object makes life easier later.
    _plan_instance: Optional[UsagePlan] = None

    def __post_init__(self, plans: dict[str, UsagePlan]) -> None:
        # Very basic validation.
        try:
            self._plan_instance = plans[self.plan]
        except KeyError:
            raise ValueError(
                f"Calendar f{self.start_date} specifies plan '{self.plan}', "
                f"but this usage plan is undefined."
            )

        if not self._plan_instance.season_defined(self.season):
            raise ValueError(
                f"Calendar '{self.start_date}/{self.plan}/{self.season}' specifies "
                f"season {self.season}, but this season is not defined for the usage "
                f"plan."
            )

        # Validate rates and update.
        for tariff in self.tariffs:
            if not self._plan_instance.tariff_defined(self.season, tariff):
                raise ValueError(
                    f"Undefined tariff '{tariff}' in calendar entry "
                    f"'{self.start_date}/{self.plan}/{self.season}'."
                )

            # Tariff may be supplied with string or PDColName and mypy can't detect
            # this - a cost of using dataclass_replace. So check and validate
            rate_table: dict[PDColName, float] = {}
            for rate_name, rate in self.tariffs[tariff].items():
                if isinstance(rate_name, PDColName):
                    # if one instance of tariff is a PDColName, they all should be,
                    # so skip out.
                    break

                # Otherwise sanitize the string input.
                rate_label = PDColName.from_str(rate_name)
                if rate_label is None:
                    raise ValueError(
                        f"Invalid rate label '{rate_name}' in rate table\nfor "
                        f"'{self.start_date}/{self.plan}/{self.season}/{tariff}.'"
                    )

                rate_table[rate_label] = rate

            if len(rate_table) > 0:
                # Only update if needed if we have new sanitized inputs.
                self.tariffs[tariff] = rate_table


class UsageEngine:
    # To make the usage engine thread safe-ish, all changes to class variables should be
    # protected by thread locking. These variables to hold data that changes
    # infrequently - configuration data shared across instances of the usage engine.
    # There is a very unlikely edge case of the user updating config and threads
    # loading the old and new user config out of order. I'm not going to make any
    # attempt to catch this, as it can be fixed by a simple reload.

    # Class variables:
    _lock = Lock()
    _influx_client: Optional[InfluxDBClient] = None
    _query_api: Optional[QueryApi] = None
    _timezone: Optional[ZoneInfo] = None
    _bucket: str = ""
    _priority: list[PDColName] = []
    _plans: dict[str, UsagePlan] = {}
    _calendar: dict[datetime, CalendarEntry] = {}

    # May or may not use these. Easy to implement now and delete later if not required.
    _cost_unit: str
    _energy_unit: str

    # Instance variables - these should be thread safe, as the server creates new
    # instance for each call of usage engine.
    # Time range is in local time!
    _range_start: datetime
    _range_stop: datetime
    # Data frame for this query.
    _frame: DataFrame
    # Ideally the report cols should be an ordered list by grouping and user preference.
    # But it's hard to manage how we add columns in pandas, so for now throw hands up
    # the air and make an unordered dict and fix later when creating tables or
    # within grafana (not fun!).
    # Key is the final column name that will be sent to grafana, values are the type
    # strings for the return json.
    _report_cols: dict[str, str]
    # And finally, a dict for over-riding column names with user specified
    # versions. As no one will be happy with my versions. (Which is fine.)
    # Key is the PDColName to override, str is the new string value for the override.
    _col_overrides: dict[PDColName, str]
    # http request dictionary if any (I strongly suspect we will never use this).
    _request_content: Optional[dict[str, Any]] = None

    # Grafana payload parameters
    # Default behaviour is to enable resampling to sensible intervals.
    resample: bool = True
    summary_report: bool = False
    report_month_to_date: bool = False
    report_year_to_date: bool = False
    _week_anchor: str = "MONTH"
    _year_anchor: str = "JAN"

    @staticmethod
    def _validate_anchor(anchor: str, options: dict[str, int]) -> str:
        u_value = anchor.upper()
        if u_value in options.keys():
            return u_value
        else:
            raise ValueError(f"Invalid anchor '{anchor}'")

    @property
    def week_anchor(self) -> str:
        return self._week_anchor

    @week_anchor.setter
    def week_anchor(self, value: str) -> None:
        self._week_anchor = self._validate_anchor(value, WEEK_ANCHORS)

    @property
    def year_anchor(self) -> str:
        return self._year_anchor

    @year_anchor.setter
    def year_anchor(self, value: str) -> None:
        self._year_anchor = self._validate_anchor(value, YEAR_ANCHORS)

    def __init__(self, json_path: Optional[str] = None) -> None:
        # Load configuration if required. For now, make the basis a check on
        # _influx_client
        if self._influx_client is None:
            self.reload_config(json_path=json_path)

    @classmethod
    def _init_settings(cls, config: dict[str, Any], json_file: str) -> None:
        # process settings
        settings = config["settings"]
        cls._influx_client = InfluxDBClient(settings["influx_url"])
        cls._bucket = settings["bucket"]
        cls._timezone = ZoneInfo(settings["timezone"])

        # Set up _col_overrides.
        cls._col_overrides = {}
        if "rename" in settings:
            for name, override in settings["rename"].items():
                pd_name = PDColName.from_str(name)
                if pd_name is None:
                    raise ValueError(f"Unrecognised 'rename' field {name} in settings.")
                else:
                    cls._col_overrides[pd_name] = override

        # initialise remaining instance variables
        cls._query_api = cls._influx_client.query_api()

        # grab influxdb buckets for validation
        buckets = cls._query_api.query("buckets()")
        # Unlikely to have more than one DB, but just in case check all
        bucket_list = [r["name"] for b in buckets for r in b.records]
        # sanitise bucket
        if cls._bucket not in bucket_list:
            temp = cls._bucket
            cls._bucket = ""
            raise KeyError(f"Invalid data bucket name '{temp}' in '{json_file}'")

        # For now, set demand priority as a global, but this could move to per plan
        # if anyone needs to change their allocation with plan (I don't see any case
        # for this at the moment).
        # Assume default.
        cls._priority = [
            PDColName.GRID_SUPPLY,
            PDColName.PW_SUPPLY,
            PDColName.SOLAR_SUPPLY,
        ]
        if SUPPLY_PRIORITY in settings:
            priority = [PDColName.from_str(x) for x in settings[SUPPLY_PRIORITY]]
            # check priorities were found!
            all_found = all([x in priority for x in cls._priority])
            if not all_found or len(settings[SUPPLY_PRIORITY]) != 3:
                # List-ish will do as long the elements are present. Not checking
                # instance.
                name_list = [x.name for x in cls._priority]
                raise TypeError(
                    f"\nDemand priority must be a list containing either all of the "
                    f"following Enum names: "
                    f"\n    {name_list}, "
                    f"\nor their equivalent string values."
                    f"\nList either contains invalid elements or is missing a "
                    f"required element.\n(Got {settings[SUPPLY_PRIORITY]})"
                )
            else:
                # mypy can't know we have eliminated None at this point
                cls._priority = priority  # type: ignore[assignment]

        # Create energy and cost units with sensible defaults.
        cls._cost_unit = "$"
        if "cost_unit" in settings:
            cls._cost_unit = settings["cost_unit"]

        cls._energy_unit = "kWh"
        if "energy_unit" in settings:
            cls._energy_unit = settings["energy_unit"]

        if "resample" in settings:
            cls.resample = bool(settings["resample"])

        if "week_anchor" in settings:
            cls._week_anchor = UsageEngine._validate_anchor(
                settings["week_anchor"], WEEK_ANCHORS
            )

        if "year_anchor" in settings:
            cls._year_anchor = UsageEngine._validate_anchor(
                settings["year_anchor"], YEAR_ANCHORS
            )

    @classmethod
    def _load_calendar(cls, calendar_json: dict[str, Any]) -> None:
        prev_event: CalendarEntry
        cls._calendar = {}

        # Create a new dict from the json with date strings converted to datetimes.
        # Because we only get offset information in isoformat strings,
        # assume the date/time is correct local time and simply force the correct
        # timezone (i.e. drop any hour offset in the iso string)
        calendar = {
            datetime.fromisoformat(d_str).replace(tzinfo=cls._timezone): item
            for d_str, item in calendar_json.items()
        }
        # Date sort. Belt and braces.
        calendar = dict(sorted(calendar.items()))

        # Now we use a dataclass to store each calendar entry. This advantage of this
        # approach is we can incrementally change calendar entries. The disadvantage
        # is that we need to construct init values here and then validate in
        # the calendar entry post_init. It works, but I suspect if I was more
        # confident in deep copy, that would have been a better way to go?
        # Very clunky, but worth the pain for incremental calendars.
        first_entry = True
        for date_v, data in calendar.items():
            # Construct keyword args. This way we can use replace to incrementally
            # update calendars (e.g. only changing season or rate data).
            # Because of the way we are doing this, validation is best deferred to
            # post_init.
            #
            kwargs: dict[str, Any] = dict()
            kwargs["start_date"] = date_v
            for key in ["plan", "season", "tariffs"]:
                if key in data:
                    kwargs[key] = data[key]
            kwargs["plans"] = cls._plans

            if first_entry:
                try:
                    cls._calendar[date_v] = CalendarEntry(**kwargs)
                except Exception as err:
                    raise ValueError(
                        f"\nCalendar entry '{date_v}' is the first calendar entry and"
                        f"\nmust have all calendar fields defined and all fields must "
                        f"be valid.\nMore info: {err}"
                    )
                first_entry = False
            else:
                cls._calendar[date_v] = dc_replace(prev_event, **kwargs)
            # Record previous event for incremental updates.
            prev_event = cls._calendar[date_v]

        # And finally, add end_date to calendar entries to simplify time period calcs
        # later. Note: I and any other devs need to be careful to ensure end_date
        # is excluded from indices/masks when breaking up calendar periods. Final
        # end date remains None.
        for this, next in pairwise(cls._calendar.values()):
            this.end_date = next.start_date

    @classmethod
    def reload_config(cls, json_path: Optional[str] = None) -> None:
        # path to json file muse be specified in interactive mode.
        with cls._lock:
            # Thread safe config update.
            if json_path is None:
                # JSON file pulled from environment variable in server mode.
                json_path = getenv("USAGE_JSON", DEFAULT_CONFIG)

            try:
                with open(json_path, "r") as fp:
                    config = simplejson.load(fp)
            except FileNotFoundError:
                raise FileNotFoundError(
                    "Usage engine JSON configuration file not found."
                    "\nSpecify 'USAGE_JSON' environment variable, provide "
                    "'usage.json' file in working directory, or provide valid path for "
                    "CLI version."
                )

            # Broken into multiple sections if this gets too long.
            cls._init_settings(config, json_path)

            if "plans" not in config:
                raise KeyError("No usage plan data in config file.")

            # Reset plans dict. This also discards any usage agents.
            cls._plans = {}

            for data in config["plans"]:
                plan = UsagePlan(data)
                cls._plans[plan.name] = plan

            if "calendar" not in config:
                raise KeyError("No calendar data in config file.")
            cls._load_calendar(config["calendar"])

    @staticmethod
    def metrics() -> str:
        # Right now, I'm confident I'm not doing this correctly.
        # But, it's working fine for the usage engine as implemented
        # and I'm not going to take the time to figure it out.
        # As we are not being clever with name spaces or multiple data bases,
        # provide a minimal response for the metrics.
        # However, to allow future flexibility (and correction of whatever
        # I'm doing wrong), implementing this as a usage engine method.
        # A problem for future me or someone else to correct when it becomes
        # important.
        #
        # Implemented as a static method for now, as it doesn't require any
        # class or instance data. Left in the class, as this may change in future.

        return simplejson.dumps(
            [
                {
                    "label": "Usage",
                    "value": "usage",
                }
            ]
        )

    def _get_influx_data(self) -> None:
        # Build the core data frame from InfluxDB usage data.

        # This query should really be made with bind parameters to
        # minimise possible injection attacks.
        # However, they aren't supported in InfluxDB 1.8.
        # so until we upgrade, we are living with minimally sanitized inputs:
        #    - The bucket name is checked against buckets in the database.
        # Belt and braces on timezone to ensure UTC.
        query = f"""
            from(bucket: "{self._bucket}")
            |> range(start: {self._range_start.astimezone(timezone.utc).isoformat()}, 
                     stop: {self._range_stop.astimezone(timezone.utc).isoformat()})
            |> filter(fn: (r) => r._measurement == "http")
            |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
            |> keep(columns: [`"{INFLUX_TIME}", "from_grid", "to_grid", "from_pw",
                              "solar", "home"])
        """

        assert self._query_api is not None
        df = self._query_api.query_data_frame(query, data_frame_index=INFLUX_TIME)
        # I suspect this is superfluous given the filtering approach.
        # But, belt and braces.
        df = df.sort_index(ascending=True)

        # Convert index from utc to local time zone - convert back to utc when
        # we are done.
        df.index = df.index.tz_convert(self._timezone)

        # Convert InfluxDB names to friendly names (sorry @jasoncox!).
        df = df.rename(columns=INFLUX_TO_PANDAS)

        # update instance.
        self._frame = df

    def _core_usage(self) -> None:
        """Calculates the core usage data and augments the data frame. Agents may
        process this further."""

        # Local pointer to instance frame. All calcs in this method update the instance.
        df = self._frame

        # Now things get a bit clunky. Work through supply priority and allocate
        # supply to meet home demand.
        last_residual = PDColName.HOME_DEMAND
        # And column names for residual demands
        # Loop through priorities.
        for i in range(len(self._priority)):
            this_residual = RESIDUALS[i]
            supply = self._priority[i]
            # Allocate available supply to residual. The clip prevents overallocation.
            # I make no attempt to balance supply, as Tesla data can be odd, and
            # influx may introduce additional errors. I'm assuming the errors
            # will be small and ignorable.
            df[this_residual.value] = (df[last_residual.value] - df[supply.value]).clip(
                lower=0.0
            )

            # And record supply allocated to demand.
            df[SUPPLY_TO_DEMAND[supply].value] = (
                df[last_residual.value] - df[this_residual.value]
            )

            # Update residual.
            last_residual = this_residual

        # Excess grid supply assumed to be sent to powerwall.
        df[PDColName.GRID_CHARGING.value] = (
            df[PDColName.GRID_SUPPLY.value] - df[PDColName.GRID_TO_HOME.value]
        )

        # Lastly, the utility groups.
        # Self consumption from powerwall less grid charging of powerwall.
        df[PDColName.SELF_PW_NET_OF_GRID.value] = (
            df[PDColName.PW_TO_HOME.value] - df[PDColName.GRID_CHARGING.value]
        )
        # Self consumption of solar + unaccounted residual.
        df[PDColName.SELF_SOLAR_PLUS_RES.value] = (
            df[PDColName.SOLAR_TO_HOME.value]
            + df[PDColName.RESIDUAL_DEMAND_FINAL.value]
        )
        # Include residual in self consumption, but not net of grid charging.
        # Be careful about which you want to use in your cost models.
        df[PDColName.SELF_TOTAL.value] = (
            +df[PDColName.PW_TO_HOME.value] + df[PDColName.SELF_SOLAR_PLUS_RES.value]
        )

        # Supply charge special case. We don't do it at all, and handle as a special
        # case in the usage agent.
        # df[PDColName.SUPPLY_CHARGE.value] = 1.0

        # Finally, set the default tariff name.
        df[PDColName.TARIFF.value] = "None"

    def _process_periodic_data(self) -> None:
        # Use the calendar to split usage range into (sub-)seasons and get usage data.
        # This could probably be done in a precise pythonic way, but spelling it out
        # so I can read the code in future.
        # season_start will either be the season start or the start of the usage range.
        # season_end will either be the end of a season or the end of the usage range.
        season_start = self._range_start
        # Calendar dictionary is sorted in time order.
        for entry in self._calendar.values():
            if entry.start_date >= self._range_stop:
                # This season starts after the end of the usage range.
                # So we're done and dusted.
                break

            if season_start <= entry.start_date:
                # Only applies if there are no valid earlier calendar entries
                # containing season_start. By definition, season_start can't be earlier
                # than current entry start date.
                season_start = entry.start_date

            if season_start >= self._range_stop:
                # Gone past the end of the usage range. Nothing more to do.
                break

            if entry.end_date is not None:
                if season_start >= entry.end_date:
                    # Calendar entry expires before season_start, and there are more
                    # calendar entries to come. Skip to next entry.
                    continue

                else:
                    # We've already made sure season_start is contained by the current
                    # entry. So now season_end is either end of current entry or end
                    # of range. This is a long min, but I want it to be clear!
                    if self._range_stop > entry.end_date:
                        # Note this is 1 s before next start date.
                        # Utterly needful because pandas slice used below is INCLUSIVE
                        # unlike regular python slices.
                        season_end = entry.end_date
                    else:
                        season_end = self._range_stop

            else:
                # we are in the final entry. By definition, all remaining
                # data is from this period.
                season_end = self._range_stop

            # Now we have done that painful process, process the season range.
            self._apply_calendar(entry, season_start, season_end)

            # Finally, update season_start for the next iteration
            # (which will get 1s added on in next iteration anyway).
            season_start = season_end

    def _add_energy_reports(
        self, tariff: str, tariff_idx: Series, usage_plan: UsagePlan
    ) -> None:
        # Add per tariff columns here. This is also the time we do any user
        # specified over-ride of default PDColName. For all of the next bits,
        # write back into the raw frame to avoid issues with
        # Pandas SettingWithCopyWarnings.
        # For a start, update the tariff.
        self._frame.loc[tariff_idx, PDColName.TARIFF.value] = tariff

        for column in usage_plan.report_cols:
            if column in {
                PDColName.TIME,
                PDColName.TARIFF,
                PDColName.SUPPLY_CHARGE,
            }:
                # Special cases.
                # Time is passed automatically. Tariff is automatically
                # included in labels and would not survive aggregation. Supply
                # charge is not meaningful for reporting at this level
                # (1 per time) - only meaningful as a cost.
                # So drop these silently.
                continue

            # Right now, only working with energy types. If this changes, will
            # need to do more here.
            full_name = column.value_with_override(self._col_overrides)
            full_name = f"{tariff} {full_name} ({self._energy_unit})"
            if full_name not in self._report_cols:
                self._report_cols[full_name] = "number"
            # Make a reporting copy of the column data.
            self._frame.loc[tariff_idx, full_name] = self._frame.loc[
                tariff_idx, column.value
            ]

    def _apply_calendar(
        self, entry: CalendarEntry, season_start: datetime, season_end: datetime
    ) -> None:
        # Filters the season range into tariff periods, tags each period with the
        # tariff name and applies the agent to the period.

        # As most of this is done with the index, lets work with the index as a series
        df_index = self._frame.index.to_series()

        # Build up the masks step by step.
        season_idx = df_index.loc[
            df_index.between(season_start, season_end, inclusive="left")
        ]

        if season_idx.empty:
            # nothing to do.
            return

        # Break each tariff period into hour groups and day of week groups.
        # Order does not matter, but I'll go by day and then hour for readability.
        # Also, for readability (but probably not efficiency), I'm creating a mask
        # on the whole frame index. This also saves problems with Pandas
        # SettingWithCopyWarnings later.
        usage_plan = self._plans[entry.plan]
        for schedule in usage_plan.season_schedules(entry.season).values():
            # As there may be multiple periods per day, worth creating a reusable day
            # index.
            day_idx = season_idx.loc[
                # cspell: disable-next-line
                season_idx.index.dayofweek.isin(schedule.days)
            ]

            if day_idx.empty:
                continue

            for period in schedule.periods:
                if len(schedule.periods) == 1:
                    # Special case - if only one index defined, it applies for
                    # all hours selected by the day filter.
                    tariff_idx = day_idx
                else:
                    # Otherwise use between_time to grab the hour blocks excluding the
                    # end time.
                    tariff_idx = day_idx.between_time(
                        start_time=period.start,
                        end_time=period.end,
                        inclusive="left",
                    )

                if tariff_idx.empty:
                    continue

                # Add report energy report columns for tariff.
                self._add_energy_reports(
                    tariff=period.tariff, tariff_idx=tariff_idx, usage_plan=usage_plan
                )

                # Create kwargs for agent. Right now, this is just demo data - the
                # simple agent doesn't need any of this. Future agents may need more
                # added here.
                kwargs: dict[str, Any] = {
                    "season": entry.season,
                    "plan": entry.plan,
                    "season_start": season_start,
                    "season_end": season_end,
                }
                # Run the usage agent on the dataset.
                usage_plan.agent.usage(
                    self._frame,
                    tariff=period.tariff,
                    tariff_idx=tariff_idx,
                    rates=entry.tariffs[period.tariff],
                    cost_unit=self._cost_unit,
                    report_cols=self._report_cols,
                    col_override=self._col_overrides,
                    kwargs=kwargs,
                )

    def _set_report_range(
        self, start_utc: Union[str, datetime], stop_utc: Union[str, datetime]
    ) -> None:
        # Utility to set up datetime range for reporting.
        # datetime must be UTC, isoformat string or datetime.
        # As we explicitly convert to a datetime, we also auto-sanitise this input.

        start: Timestamp
        end: Timestamp

        if self.report_month_to_date or self.report_year_to_date:
            now = Timestamp.now(tz=self._timezone).normalize()
            # pandas makes the next bits very easy!
            if self.report_year_to_date:
                anchor = YEAR_ANCHORS[self._year_anchor]
                start = offsets.YearBegin(month=anchor).rollback(now)
                # Could do this with modulo, but hard to read.
                if anchor == 1:
                    anchor = 12
                else:
                    anchor = anchor - 1
                end = offsets.YearEnd(month=anchor).rollforward(now)

            else:
                start = offsets.MonthBegin().rollback(now)
                end = offsets.MonthEnd().rollforward(now)

            # Clean up
            end = end + offsets.Hour(23) + offsets.Minute(59) + offsets.Second(59)
            self._range_start = start.to_pydatetime()
            self._range_stop = end.to_pydatetime()

        else:
            # Use specified ranges.
            self._range_start = safe_iso_utc_to_dt(start_utc, new_tz=self._timezone)
            self._range_stop = safe_iso_utc_to_dt(stop_utc, new_tz=self._timezone)

        log.debug(
            f"Usage query range from '{self._range_start}' to '{self._range_stop}'."
        )

    def _aggregate(self) -> None:
        # Perform data aggregation as required.

        if self.summary_report:
            # Over rides everything else. Sum returns a series, so we convert it back
            # to a frame and transpose it - because the json export expects a frame
            # and this eliminates the need for special case code.
            self._frame = self._frame.sum(numeric_only=True).to_frame().T
            # And because the index is [0], replace it with an appropriate datetime
            self._frame.index = DatetimeIndex([self._range_start])

        elif self.resample:
            start = Timestamp(self._range_start)
            stop = Timestamp(self._range_stop)
            if start.date() == stop.date():
                # Both on the same, resample to hours.
                self._frame = self._frame.resample(
                    "H", closed="left", label="left"
                ).sum(numeric_only=True)

            elif (stop - start) <= Timedelta(days=7):
                # Both in roughly the same week, resample to days. Will result in
                # up to 8 days shown depending on how the query is structured.
                # grafana now-7d will definitely cause this!
                # Good enough is close enough.
                self._frame = self._frame.resample(
                    "D", closed="left", label="left"
                ).sum(numeric_only=True)

            elif start.year == stop.year and start.month == stop.month:
                # to_period is the elegant of doing this check, but pandas raises a
                # UserWarning about losing tz info that we don't want to suppress.
                # So we go with a more heavy handed check.
                if self.week_anchor == "MONTH":
                    # anchor on first day of month
                    anchor = offsets.MonthBegin().rollback(start).dayofweek
                else:
                    anchor = WEEK_ANCHORS[self.week_anchor]
                self._frame = self._frame.resample(
                    offsets.Week(weekday=anchor), closed="left", label="left"
                ).sum(numeric_only=True)

            elif (stop.year - start.year) * 12 + stop.month - start.month <= 11:
                # Anything less than a year, sample on monthly basis.
                # I think the above test captures this, but ... I may have missed an
                # edge case.
                self._frame = self._frame.resample(
                    "MS", closed="left", label="left"
                ).sum(numeric_only=True)

            else:
                # Resample on yearly basis, honour anchor.
                self._frame = self._frame.resample(
                    "AS-" + self.year_anchor, closed="left", label="left"
                ).sum(numeric_only=True)

        else:
            # if we are not resampling, do nothing to the frame.
            pass

    def usage(
        self,
        start_utc: Union[str, datetime],
        stop_utc: Union[str, datetime],
        payload: Optional[dict[str, Any]] = None,
        request_content: Optional[dict[str, Any]] = None,
    ) -> str:
        # Arguments:
        #  start_utc - start_time, iso format string UTC time ending in Z, or utc
        #    datetime.
        #  stop_utc - start_time, iso format string UTC time ending in Z, or utc
        #   datetime.
        #  payload - payload dictionary, which may contain the following entries:
        #    "resample": True | False, also accessible via self.resample class attribute
        #    "month_to_date": True | False, accessible by self.report_month_to_date
        #    "year_to_date": True | False, accessible by self.report_year_to_date
        #    "summary": True | False, accessible by self.summary_report
        #  request_content - json http request dictionary. Not used in V1.0, but
        #    provided for potential future use.

        if request_content is not None:
            # store it if we have it.
            self._request_content = request_content

        if payload is not None:
            if "resample" in payload:
                self.resample = bool(payload["resample"])
            if "month_to_date" in payload:
                self.report_month_to_date = bool(payload["month_to_date"])
            if "year_to_date" in payload:
                self.report_year_to_date = bool(payload["year_to_date"])
            if "summary" in payload:
                self.summary_report = bool(payload["summary"])

        # Create report columns list.
        self._report_cols = {}

        # Set up query time range.
        self._set_report_range(start_utc=start_utc, stop_utc=stop_utc)

        # Pull the raw data
        self._get_influx_data()
        # Set up the core data frame
        self._core_usage()

        # Break the data into seasons and schedules, tag tariffs and add
        # cost data.
        self._process_periodic_data()

        self._aggregate()

        # And now we process the frame into json tables
        return self._frame_to_json_tables()

    def _frame_to_json_tables(self) -> str:
        # List of tables to return. Right now, only one table.
        tables: list[dict[str, Any]] = list()

        # Because it just makes life easier, reduce the reporting frame to data columns
        # and do renaming along the way. Need to keep tariff name in the new frame. If
        # I do need to break out cost, energy and other, this where it's identified.
        df = self._frame[list(self._report_cols.keys())]
        # Annoyingly, we need to do an explicit time conversion to ms here, and need to
        # add time to our report dict
        df.insert(0, PDColName.TIME.value, df.index.astype(np_int64) / int(1e6))
        self._report_cols[PDColName.TIME.value] = "time"

        # Next bit cribs heavily from
        # https://github.com/panodata/grafana-pandas-datasourced
        # First pass, return one big table. May need to break down by cost, energy and
        # other if this is a grafana requirement (I hope not!)
        # If we need to create additional tables, follow this recipe for each table and
        # append each table dict to tables list.

        this_table: dict[str, Any] = {
            "type": "table",
            "name": "usage",
        }

        this_table["columns"] = []
        for name in df.columns.tolist():
            ret_type = self._report_cols[name]
            this_table["columns"].append({"text": name, "type": ret_type})

        # And the data. Simples!
        this_table["rows"] = df.where(notnull(df), None).values.tolist()

        # And add to our list of tables.
        tables.append(this_table)

        # NOTE - MUST USE SIMPLEJSON FOR THIS. Avoids choking on Nan in grafana plugin.
        return simplejson.dumps(tables, ignore_nan=True)


if __name__ == "__main__":
    """Provide command for debugging dumps."""
    parser = ArgumentParser(
        description="Simple debug interface to Powerwall Dashboard usage engine."
        "\nstart and end are required, month to date, year to date not supported."
    )
    parser.add_argument(
        "--start",
        # cspell: disable-next-line
        help="Start date/time for reporting. Local time, no tz info - YYYY-MM-DDTHH:MM.",
        required=True,
    )

    parser.add_argument(
        "--end",
        # cspell: disable-next-line
        help="Start date/time for reporting. Local time, no tz info - YYYY-MM-DDTHH:MM.",
        required=True,
    )

    parser.add_argument(
        "--config",
        # cspell: disable-next-line
        help="Path to json config file.",
        required=True,
    )

    parser.add_argument("--summary", help="Summary report only.", action="store_true")

    parser.add_argument(
        "--disable-resample", help="Summary report only.", action="store_true"
    )

    parser.add_argument(
        "--outfile", help="Output file/filepath, writes .csv format", required=True
    )

    parser.add_argument("--debug", help="Provide debug logging.", action="store_true")

    args = parser.parse_args()

    # Create our usage instance.
    usage = UsageEngine(json_path=args.config)
    usage.resample = not args.disable_resample
    usage.summary_report = args.summary

    # Sort out the dates we want.
    # This is very clunky. Convert string to time, add local timezone, convert to utc.
    # usage will then revert back to local time zone ...
    # Includes lazy reach into usage instance for tz info.
    start = (
        datetime.fromisoformat(args.start)
        .replace(tzinfo=usage._timezone)
        .astimezone(tz=timezone.utc)
    )
    stop = (
        datetime.fromisoformat(args.end)
        .replace(tzinfo=usage._timezone)
        .astimezone(tz=timezone.utc)
    )

    if args.debug:
        log.setLevel(LOG_DEBUG)

    usage.usage(start_utc=start, stop_utc=stop, payload=None, request_content=None)

    # Because I'm over this, reach in to grab frame.
    usage._frame.to_csv(args.outfile)
