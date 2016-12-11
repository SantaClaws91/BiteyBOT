import requests

if __name__ != '__main__':
    from packages.log import log

accesstoken = 'cwxvu35rucaqviti2kvdhjxsg7rb26'
clientID = '91yc6gwdiju5sae40wjqf0pvx4v97hu'

headers = {
    'Authorization':'OAuth ' + accesstoken,
    'Accept': 'application/vnd.twitchtv.v3+json',
    'Client-ID': clientID
    }

def new_topic(topic, channel, accesstoken=accesstoken, clientID=clientID):
    params = {
    'channel[status]': topic
    }
    try:
        requests.put('https://api.twitch.tv/kraken/channels/' + channel, headers = headers, params = params).raise_for_status()
    except:
        log.mainLog.exception('Unauthorized attempt at editing.')

def new_game(game, channel, accesstoken=accesstoken, clientID=clientID):
    params = {
        'channel[game]': game
        }
    try:
        requests.put('https://api.twitch.tv/kraken/channels/' + channel, headers = headers, params = params).raise_for_status()
    except:
        log.mainLog.exception('Unauthorized attempt at editing.')
