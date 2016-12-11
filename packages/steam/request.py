import requests
import re

from packages.time.time import sec_to_string
from packages.log.log import mainLog

STEAM_WEB_API_KEY = "9E3142E7D7DC28C31FA9B0AF292043F7"

mode = [
    'GetOwnedGames',
    'GetRecentlyPlayedGames'
    ]

def get_steam_api(steamID, api=mode[0]):
    url = (
        "http://api.steampowered.com/IPlayerService/"+ api +
        "/v0001/"
        "?key="+ STEAM_WEB_API_KEY +
        "&steamid="+ str(steamID) +
        "&format=json"
        )

    try:
        r = requests.get(url)
        data = r.json()
        return data
    except:
        return
        mainLog.exception('Steam API fail')

def time_played_seconds(appid, steamID, recent=False):
    time = 'playtime_forever'
    if recent:
        time = 'playtime_2weeks'
        object_ = get_steam_api(steamID, mode[1])
    else:
        object_ = get_steam_api(steamID, mode[0])
    if not object_:
        return None
    if not object_['response']:
        return None
    object_ = object_['response']
    if not object_['games']:
        return None
    object_ = object_['games']

    for index in object_:
        if not index['appid'] == appid:
            continue
        return index[time] * 60

def replace_string(string, steamID):
    match = re.match(
        '.*\$played\((\d*)\).*',
        string
        )
    recent = False
    if not match:
        match = re.match(
        '.*\$playedrecent\((\d*)\).*',
        string
        )
        recent = True
        if not match:
            return string
    appid = match.group(1)

    repl = '$played('+ appid +')'
    if recent == True:
        repl = '$playedrecent('+ appid +')'

    time_delta = time_played_seconds(int(appid), steamID, recent)
    if time_delta == None:
        return ""
    seconds_to_string = sec_to_string(time_delta)

    return string.replace(repl, seconds_to_string)
