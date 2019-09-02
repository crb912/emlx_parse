"""
Date and Time Converting.
"""

import datetime

from dateutil import parser
import pytz

IOS_UTC_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
UTC_FORMAT = '%Y-%m-%dT%H:%M:%S+00:00'


def time_str_to_utc_str(time_str: str) -> str:
    """Return UTC str from arbitrary timezone time string.

    About ISO8601 date string:  https://en.wikipedia.org/wiki/ISO_8601
    Combined date and time representations:
         "2007-04-05T14:30Z" or "2007-04-05T12:30-02:00".

    >>> time_str_to_utc_str('2012-11-01T04:16:13-04:00')  # ISO8601 format
    '2012-11-01T08:16:13+00:00'
    >>> time_str_to_utc_str('8 Jul 2019 20:22:47 +0800')  # Email data format
    '2019-07-08T12:22:47+00:00'
    >>> time_str_to_utc_str('8 Jul 2019 20:22:47 +0800 (GMT+08:00)')
    '2019-07-08T12:22:47+00:00'
    """

    try:
        dt = parser.parse(time_str)
        dt = dt.replace(tzinfo=pytz.utc) - dt.utcoffset()
        return dt.strftime(UTC_FORMAT)
    except ValueError:
        if '(' in time_str:
            return time_str_to_utc_str(time_str.split('(')[0])


def utc_str_to_local_str(utc_str: str, utc_format: str, local_format: str):
    """Return local time strings form UTC time strings.

    :param utc_str: UTC time string
    :param utc_format: format of UTC time string
    :param local_format: format of local time string
    :return: local time string

    >>> utc = '2018-10-17T00:00:00.111Z'
    >>> utc_str_to_local_str(utc, '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%S')
    '2018-10-17T08:00:00'
    """
    temp1 = datetime.datetime.strptime(utc_str, utc_format)
    temp2 = temp1.replace(tzinfo=datetime.timezone.utc)
    local_time = temp2.astimezone()
    return local_time.strftime(local_format)


def utc_str_to_timestamp(utc_str: str, utc_format: str) -> int:
    """Return timestamp from UTC time strings.

    >>> utc_str_to_timestamp('2018-10-17T00:00:00', '%Y-%m-%dT%H:%M:%S')
    1539734400
    """
    temp1 = datetime.datetime.strptime(utc_str, utc_format)
    temp2 = temp1.replace(tzinfo=datetime.timezone.utc)
    return int(temp2.timestamp())


def timestamp_to_utc_str(ts: int) -> str:
    """
    :param ts: time stamp
    >>> timestamp_to_utc_str(1562588568)
    '2019-07-08T12:22:48Z'
    """
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
