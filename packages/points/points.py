from packages.configuration import file
from packages.log.log import ircLog
from datetime import datetime

file_ = 'points.yml'

users = dict()

def on_join(user, chan):
    if not user in users:
        on_add("biteybot", chan, user)
        users[user] = datetime.now()
        return
    
    timeDelta = datetime.now() - users[user]
    if timeDelta > 6*60*60:
        return
    on_add(user, chan, user)

def on_add(user, chan, arg):
    chan = chan.strip('#').lower()
    arg = arg.strip('@').lower()
    
    points = file.readyaml(chan, file_)
    if user == arg:
        return None
    if not arg in points:
        points[arg] = 0
    points[arg] += 1
    file.writeyaml(points, chan, file_)

def announce(user, chan):
    chan = chan.strip('#')
    points = file.readyaml(chan, file_)
    if not points:
        return None
    if not user in points:
        return 0
    return points[user]

def points_prefix(arg, chan):
    points = file.readyaml(chan, file_)

    if points == None:
        points= {
            'cmd': arg,
            'delay': 45
            }
    else:
        points['cmd'] = arg
    
    file.writeyaml(points, chan, file_)
    print('Point prefix is now '+ arg)
    ircLog.info('Point prefix is now '+ arg)
    return
