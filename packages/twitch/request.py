import requests

from packages.log import log

def get_twitch_info(api, chan):
    url = 'https://api.twitch.tv/kraken/{api}/{chan}'.format(api=api, chan=chan.strip('#'))
    try:
        r = requests.get(url)
        data = r.json()
    except:
        log.mainLog.debug('request ' + url + ' failed.')
        return None
    if not data:
        return None
    if not 'stream' in data:
        return None
    return data['stream']

def get_twitch_chatters(chan):
    url = "https://tmi.twitch.tv/group/user/{}/chatters".format(chan.strip('#'))
    try:
        r = requests.get(url)
        data = r.json()
    except:
        log.mainLog.debug('request ' + url + ' failed.')
        return None
    return data

def operators(chan):
    chan = chan.strip('#').strip(':')
    op = dict(get_twitch_chatters(chan))
    if not op:
        return None
    if not 'chatters' in op:
        return None
    op = op['chatters']
    if not 'moderators' in op:
        return None
    return op['moderators']
