import json
import datetime
from typing import Any, TypedDict, OrderedDict


class Readings(TypedDict):
    t: int  # temperature
    h: int  # humidity
    r: float  # rain


# DateTime has format YYYYMMDDhhmmss.
DateTime = str


def parse_datetime(datestr: str) -> datetime.datetime:
    return datetime.datetime.strptime(datestr, "%Y%m%d%H%M%S")


Weather = dict[DateTime, Readings]


def read_data(filename: str) -> Weather:
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        return {}

    data: Weather = json.load(file)
    file.close()
    return data


def write_data(data: Weather, filename: str) -> None:
    file = open(filename, "w")
    json.dump(data, file)
    file.close()


def max_temperature(data: Weather, date: str) -> int | None:
    max = None
    for datestr in data:
        if datestr.startswith(date):
            if max is None or data[datestr]["t"] > max:
                max = data[datestr]["t"]
    return max


def min_temperature(data: Weather, date: str) -> int | None:
    min = None
    for datestr in data:
        if datestr.startswith(date):
            if min is None or data[datestr]["t"] < min:
                min = data[datestr]["t"]
    return min


def max_humidity(data: Weather, date: str) -> int | None:
    max = None
    for datestr in data:
        if datestr.startswith(date):
            if max is None or data[datestr]["h"] > max:
                max = data[datestr]["h"]
    return max


def min_humidity(data: Weather, date: str) -> int | None:
    min = None
    for datestr in data:
        if datestr.startswith(date):
            if min is None or data[datestr]["h"] < min:
                min = data[datestr]["h"]
    return min


def tot_rain(data: Weather, date: str) -> float:
    tot = 0.0
    for datestr in data:
        if datestr.startswith(date):
            tot += data[datestr]["r"]
    return tot


def daily_readings(data: Weather, date: str) -> OrderedDict[DateTime, Readings]:
    readings = OrderedDict[DateTime, Readings]()
    for datestr in data:
        if datestr.startswith(date):
            readings[datestr] = data[datestr]
    return readings


def report_daily(data: Weather, date: str) -> str:
    readings = daily_readings(data, date)
    text = """\
========================= DAILY REPORT ========================
Date                      Time  Temperature  Humidity  Rainfall
====================  ========  ===========  ========  ========
"""

    for date in readings:
        reading = readings[date]
        pdate = parse_datetime(date)
        rdate = pdate.strftime("%B %-d, %Y")
        rtime = pdate.strftime("%H:%M:%S")
        text += f"\
{rdate: <20}  \
{rtime: <8}  \
{reading['t']: >11}  \
{reading['h']: >8}  \
{reading['r']: >8.2f}\n"

    return text


def report_historical(data: Weather):
    text = """\
============================== HISTORICAL REPORT ===========================
                          Minimum      Maximum   Minumum   Maximum     Total
Date                  Temperature  Temperature  Humidity  Humidity  Rainfall
====================  ===========  ===========  ========  ========  ========
"""

    # Collect all the readings for its year-month-day components.
    dates = OrderedDict[str, None]()
    for datestr in data:
        pdate = parse_datetime(datestr)
        rdate = pdate.strftime("%Y%m%d")
        dates[rdate] = None

    # Using the collected dates, report the min/max/total for each day.
    for date in dates:
        # Reformat the date to be more readable. Very cool API, Python.
        dstr = datetime.datetime.strptime(date, "%Y%m%d").strftime("%B %-d, %Y")
        mint = min_temperature(data, date)
        maxt = max_temperature(data, date)
        minh = min_humidity(data, date)
        maxh = max_humidity(data, date)
        rain = tot_rain(data, date)
        text += f"\
{dstr: <20}  \
{mint: >11}  \
{maxt: >11}  \
{minh: >8}  \
{maxh: >8}  \
{rain: >8.2f}\n"

    return text
