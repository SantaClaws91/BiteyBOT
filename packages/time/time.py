import re
from datetime import datetime

from packages.twitch.request import get_twitch_info

def match_datetime(string):
    match = re.match(
        '.*\$dur\(((?P<year>\d*)-(?P<month>\d*)-(?P<day>\d*)T(?P<hour>\d*):(?P<minute>\d*):(?P<second>\d*)Z)\).*',
        string
        )
    if not match:
        return string

    #This needs revisiting! Bad code. Multiple datetimes would malfunction mm.
    t0 = datetime.strptime(match.group(1), '%Y-%m-%dT%H:%M:%SZ')
    time_delta = datetime.now() - t0
    time_delta = time_delta.total_seconds()
    sec_conv = sec_to_string(time_delta)

    sub = re.sub(
        '\$dur\(((?P<year>\d*)-(?P<month>\d*)-(?P<day>\d*)T(?P<hour>\d*):(?P<minute>\d*):(?P<second>\d*)Z)\)',
        sec_conv,
        string
        )
    return sub

def uptime(string, twitch_info):
    if not '$uptime' in string:
        return string

    if not twitch_info:
        return string.replace('$uptime', 'None')

    if not 'created_at' in twitch_info:
        return string.replace('$uptime', 'None')

    created_at = twitch_info['created_at']

    t0 = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')

    time_delta = datetime.now() - t0
    time_delta = time_delta.total_seconds()

    #Need a time zone option.
    from __main__ import config    
    time_zone_difference = 0
    if config:
        if 'timezone_difference' in config:
            time_zone_difference = 3600*config['timezone_difference']
    
    time_delta = time_delta - time_zone_difference

    if type(time_delta) == type(None):
        return ""

    uptime = sec_to_string(time_delta)

    return string.replace('$uptime', uptime)

def sec_to_string(time_delta):
    if type(time_delta) == type(None):
        return ""

    time_delta = abs(time_delta)
    
    second = ''
    minute = ''
    hour = ''
    day = ''
    week = ''
    month = ''
    year = ''

    ## Over 8 weeks
    if time_delta >= 8*604800:
        Y, s = divmod(time_delta, 31556926)
        M, s = divmod(s, 2629743.83)
        d, s = divmod(s, 86400)

        if Y:
            year = str(Y) + ' year '
            if not int(Y) == 1:
                year = year.strip() + 's '
        if M:
            month = str(M) + ' month '
            if not int(M) == 1:
                month = month.strip() + 's '
        if d:
            day = str(d) + ' day '
            if not int(d) == 1:
                day = day.strip() + 's '

        return '{}{}{}'.format(year, month, day).strip().replace('.0', '')

    ## Over 2 weeks
    if time_delta >= 2*604800:
        w, s = divmod(time_delta, 604800)
        d, s = divmod(s, 86400)
        h, s = divmod(s, 3600)

        if w:
            week = str(w) + ' week '
            if not int(w) == 1:
                week = week.strip() + 's '
        if d:
            day = str(d) + ' day '
            if not int(d) == 1:
                day = day.strip() + 's '
        if h:
            hour = str(h) + ' hour '
            if not int(h) == 1:
                hour = hour.strip() + 's '

        return '{}{}{}'.format(week, day, hour).strip().replace('.0', '')

    ## Over 48 hours
    if time_delta >= 48*3600:
        d, s = divmod(time_delta, 86400)
        h, s = divmod(s, 3600)
        m, s = divmod(s, 60)

        if d:
            day = str(d) + ' day '
            if not int(d) == 1:
                day = day.strip() + 's '
        if h:
            hour = str(h) + ' hour '
            if not int(h) == 1:
                hour = hour.strip() + 's '
        if m:
            minute = str(m) + ' min '
            if not int(m) == 1:
                minute = minute.strip() + 's '

        return '{}{}{}'.format(day, hour, minute).strip().replace('.0', '')

    ## Under 48 hours
    h, s = divmod(time_delta, 3600)
    m, s = divmod(s, 60)

    if h:
        hour = str(h) + ' hour '
        if not int(h) == 1:
            hour = hour.strip() + 's '
    if m:
        minute = str(m) + ' min '
        if not int(m) == 1:
            minute = minute.strip() + 's '
    if s:
        s = int(s)
        second = str(s) + ' sec '
        if not int(s) == 1:
            second = second.strip() + 's '

    return '{}{}{}'.format(hour, minute, second).strip().replace('.0', '')
