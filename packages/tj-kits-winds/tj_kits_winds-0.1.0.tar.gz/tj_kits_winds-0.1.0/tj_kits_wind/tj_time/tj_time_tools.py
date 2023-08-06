import datetime
import time
from typing import List, Literal, Union
from pydantic import BaseModel

"""
 从 秒 开始, 每向下一级 单位是 1:1000
 
 1 s = 1000 ms  (毫秒)
 1 ms = 1000 μs (微秒)   
    这是 python dt, dt_str, dt_delta 的最小的时间单位
 1 μs = 1000 ns (纳秒)
    python 时间戳可以 表现到 纳秒 (bit=19)
 1 ns = 1000 ps (皮秒)

    python中,
        dt_str 和 print(datetime.datetime.now())  默认显示 6位小数 即 微秒
        即使 传入 19 位时间戳 转换, 也只能到 微秒 
"""

__all__ = ['TIME_FORMAT_NORMAL_us', 'TIME_FORMAT_NORMAL', 'TIME_FORMAT_NORMAL_SHORT', 'TIME_FORMAT_ISO',
           'TIME_FORMAT_ISO_SHORT', 'get_ts', 'get_now', 'trans_dt_ts', 'trans_dt_str', 'trans_ts_str',
           'get_diff', 'get_diff_simple', 'get_diff_just_total']

TIME_FORMAT_NORMAL_us = "%Y-%m-%d %H:%M:%S.%f"  # 微秒
TIME_FORMAT_NORMAL = "%Y-%m-%d %H:%M:%S"
TIME_FORMAT_NORMAL_SHORT = "%Y-%m-%d"
TIME_FORMAT_ISO = "%m/%d/%Y %H:%M:%S"
TIME_FORMAT_ISO_SHORT = "%m/%d/%Y"


class TimeDiff(BaseModel):
    days: int
    hours: int
    minutes: int
    seconds: int
    mss: int
    uss: int
    total_days: int
    total_hours: int
    total_minutes: int
    total_seconds: float


class TimeDiffJustTotal(BaseModel):
    total_days: int
    total_hours: int
    total_minutes: int
    total_seconds: float


class TimeDiffSimple(BaseModel):
    days: int
    hours: int
    minutes: int
    seconds: int
    mss: int
    uss: int


def get_ts(ts_int: int | None = None, bits: int = 10) -> int:
    """
    如果 ts_int 为 None, 返回 指定位数的当前 int(时间戳)
        now_ts = get_ts()
        now_ts = get_ts(bits=13)
    如果 ts_int 有值, 返回 按位数 格式化后的 int(时间戳)
    注意: 函数不保证 按位数 格式化后的 int 是正确 的时间戳值得
        ts = get_ts(1686015673, 13)
        ts = get_ts(1686045596611672)
        ts = get_ts(1686045596611672, 19)
    """

    if bits not in [10, 13, 16, 19]:
        bits = 10

    if not ts_int:
        now_ts = datetime.datetime.now().timestamp()
        if bits == 10:  # 秒
            return int(now_ts)
        if bits == 13:  # 毫秒
            return int(now_ts * 1000)
        if bits == 16:  # 微秒
            return int(now_ts * 1000 * 1000)
        if bits == 19:  # 纳秒
            return time.time_ns()
    else:
        ts_str = str(ts_int)
        len_ts_str = len(ts_str)

        if len_ts_str >= bits:
            res = ts_str[:bits]
        else:
            complement = str(10 ** (bits - len_ts_str))
            res = ts_str + complement[1:]

        return int(res)


def get_now(r_dt: bool = False, r_str: bool = False, r_ts: bool = False,
            bits: int = 10, format_str: str = TIME_FORMAT_NORMAL) -> datetime.datetime | str | int:
    """
    不给定任何参数的情况下, 与 get_ts 用法一致,返回当前 时间 10位 时间戳
        res = get_now(r_str=True)
        res = get_now(r_dt=True)
        res = get_now(bits=10)
        res = get_now(bits=13)
        res = get_now(bits=19)
    """

    if not (r_dt or r_str or r_ts):
        return get_ts(bits=bits)

    if r_ts:
        return get_ts(bits=bits)

    dt = datetime.datetime.now()
    if r_dt:
        return dt
    if r_str:
        return dt.strftime(format_str)


def trans_dt_str(dt_or_str: datetime.datetime | str, format_str: str = TIME_FORMAT_NORMAL) \
        -> datetime.datetime | str:
    """
    入参为 datetime.datetime 则返回 str
    入参为 str 则返回 datetime.datetime
        res = trans_dt_str("2023-06-07 14:57:33", TIME_FORMAT_NORMAL)
        2023-06-07 14:57:33

        res = trans_dt_str("06/07/2012 14:57:33", TIME_FORMAT_ISO)
        2012-06-07 14:57:33

        res = trans_dt_str(datetime.datetime.now(), TIME_FORMAT_ISO_SHORT)
        06/07/2023
    """

    if isinstance(dt_or_str, str):
        # return datetime
        return datetime.datetime.strptime(dt_or_str, format_str)
    elif isinstance(dt_or_str, datetime.datetime):
        # return str
        return dt_or_str.strftime(format_str)


def trans_dt_ts(dt_or_ts: datetime.datetime | int, bits: int = 10) -> datetime.datetime | int:
    """
    dt = trans_dt_str("2019-02-12 18:29:36")
    res_ts = trans_dt_ts(dt, bits=19)
    print(res_ts)

    res_dt = trans_dt_ts(res_ts)
    print(res_dt)
    """

    if bits not in (10, 13, 16, 19):
        bits = 10

    if isinstance(dt_or_ts, datetime.datetime):
        ori_ts = dt_or_ts.timestamp()
        if bits == 10:  # 秒
            return int(ori_ts)
        if bits == 13:  # 毫秒
            return int(ori_ts * 1000)
        if bits == 16:  # 微秒
            return int(ori_ts * 1000 * 1000)
        if bits == 19:  # 纳秒
            return int(ori_ts * 1000 * 1000 * 1000)

    if isinstance(dt_or_ts, int):
        ts_str = str(dt_or_ts)
        len_ts_str = len(ts_str)

        # python 的时间戳类型 10位整数 对应的是 年月日时分秒, 小数位对应的是 毫秒,纳秒
        if len_ts_str > 10:
            res_ts_str = ts_str[:10] + "." + ts_str[10:]
        elif len_ts_str < 10:
            complement = str(10 ** (10 - len_ts_str))
            res_ts_str = ts_str + complement[1:]
        else:
            res_ts_str = ts_str

        # len_ts_str == 10 则直接转换
        ts = float(res_ts_str)

        dt = datetime.datetime.fromtimestamp(ts)
        return dt


def trans_ts_str(ts_or_str: int | str, bits: int = 10, format_str: str = TIME_FORMAT_NORMAL) -> int | str:
    """
    流程:
        ts to str: ts -> datetime -> str
        str to ts: str -> datetime -> ts

    res = trans_ts_str("2018-02-25 16:00:05", bits=10)
    print(res)
    res = trans_ts_str("2019-02-25 16:00:05", bits=13)
    print(res)
    res = trans_ts_str("2020-02-25 16:00:05", bits=19)
    print(res)

    res = trans_ts_str(1519545605, format_str=TIME_FORMAT_ISO)
    print(res)
    res = trans_ts_str(1551081605000, format_str=TIME_FORMAT_ISO_SHORT)
    print(res)
    res = trans_ts_str(1582617605000000, format_str=TIME_FORMAT_NORMAL)
    print(res)
    """

    if isinstance(ts_or_str, int):
        dt = trans_dt_ts(ts_or_str, bits)
        dt_str = trans_dt_str(dt, format_str)
        return dt_str

    if isinstance(ts_or_str, str):
        dt = trans_dt_str(ts_or_str, format_str)
        ts = trans_dt_ts(dt, bits)
        return ts


#
def get_diff_just_total(dt1: datetime.datetime, dt2: datetime.datetime, reverse: bool = False) -> TimeDiffJustTotal:
    if reverse:
        diff = dt2 - dt1
    else:
        diff = dt1 - dt2

    total_seconds = diff.total_seconds()
    total_days = int(total_seconds / (3600 * 24))

    total_hours = int(total_seconds / 3600)
    total_minutes = int(total_seconds / 60)

    time_diff = TimeDiffJustTotal(
        total_days=total_days,
        total_hours=total_hours,
        total_minutes=total_minutes,
        total_seconds=total_seconds)
    return time_diff


def get_diff_simple(dt1: datetime.datetime, dt2: datetime.datetime, reverse: bool = False) -> TimeDiffSimple:
    if reverse:
        diff = dt2 - dt1
    else:
        diff = dt1 - dt2

    total_seconds = diff.total_seconds()
    total_days = int(total_seconds / (3600 * 24))

    total_hours = int(total_seconds / 3600)
    total_minutes = int(total_seconds / 60)

    #
    days_float = total_seconds / (3600 * 24)
    days_int = int(days_float)
    days_residue_float = days_float - days_int  # 0.xxxx d

    # 0.xxxx d  -> xx.xxxx hours
    hours_float = days_residue_float * 24
    hours_int = int(hours_float)
    hours_residue_float = hours_float - hours_int  # 0.xxxx h

    # 0.xxxx h -> xx.xxxx minutes
    minutes_float = hours_residue_float * 60
    minutes_int = int(minutes_float)
    minutes_residue_float = minutes_float - minutes_int  # 0.xxxx m

    # 0.xxxx m -> xx.xxxx seconds
    seconds_float = minutes_residue_float * 60
    seconds_int = int(seconds_float)

    total_seconds_str = str(total_seconds)
    total_seconds_split = total_seconds_str.split(".")
    if len(total_seconds_split) == 1:
        ms = 0
        us = 0
    else:
        ms_us_str = total_seconds_split[1]

        if len(ms_us_str) >= 6:
            ms_us_str = ms_us_str[:6]
        else:
            complement = str(10 ** (6 - len(ms_us_str)))
            ms_us_str = ms_us_str + complement[1:]
        ms = int(ms_us_str[:3])
        us = int(ms_us_str[3:])

    time_diff = TimeDiffSimple(
        days=total_days,
        hours=hours_int,
        minutes=minutes_int,
        seconds=seconds_int,
        mss=ms,
        uss=us,
    )
    return time_diff


def get_diff(dt1: datetime.datetime, dt2: datetime.datetime, reverse: bool = False) -> TimeDiff:
    total = get_diff_just_total(dt1, dt2, reverse)
    simple = get_diff_simple(dt1, dt2, reverse)

    time_diff = TimeDiff(
        days=simple.days,
        hours=simple.hours,
        minutes=simple.minutes,
        seconds=simple.seconds,
        mss=simple.mss,
        uss=simple.uss,
        total_days=total.total_days,
        total_hours=total.total_hours,
        total_minutes=total.total_minutes,
        total_seconds=total.total_seconds
    )
    return time_diff


def get_diff_with_trans(d1: int | str | datetime.datetime, d2: int | str | datetime.datetime,
                        bits: int = 10, format_str: str = TIME_FORMAT_NORMAL,
                        reverse: bool = False, total: bool = False,
                        simple: bool = False) -> TimeDiff | TimeDiffSimple | TimeDiffJustTotal:
    raise NotImplementedError
