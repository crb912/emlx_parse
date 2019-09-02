from emlx_parse.time_utls import time_str_to_utc_str, timestamp_to_utc_str


def convert_time(src_string: str):
    """
    >>> convert_time('Mon, 8 Jul 2019 20:22:47 +0800')
    '2019-07-08T12:22:47+00:00'
    """
    if isinstance(src_string, str):
        try:
            return time_str_to_utc_str(src_string.split(',')[-1])
        except ValueError:
            print('emlx invalid time format: {}'.format(src_string))
    return


def convert_time_from_plist(time_stamp: int):
    """
    >>> convert_time_from_plist(1562588568)
    '2019-07-08T12:22:48Z'
    """
    if isinstance(time_stamp, int):
        return timestamp_to_utc_str(time_stamp)
    return





