from datetime import datetime
import random

from packages.twitch import request
from packages.configuration import file
from packages.irc.connect import sendmsg

welcome = dict()
welcome_path = 'welcome.yml'
welcome_default = {
            'partdelay': 3600,
            'welcome': {
              'default': [
                  'Hello {nick}! Welcome back!',
                  'Oh there you are {nick}! Welcome back!',
                  'Hey there {nick}!',
                  'Welcome back {nick}!',
                  "Look who's back, it's {nick}! Welcome back {nick}!",
                  'Special treat for us! {nick} is back!!',
                  'Our favorite {nick} is back! Welcome back {nick}!'
                  ]
              }
            }

def on_part(user, chan):
    chan = chan.strip('#').strip(':')
    if not chan in welcome:
        welcome[chan] = dict()
    welcome[chan][user] = datetime.now()

def on_start(operators, chan):
    for user in operators:
        if not chan in welcome:
            welcome[chan] = dict()
        welcome[chan][user] = True

def greeting(user, chan, operators):
    chan = chan.strip('#').strip(':').strip('*')
    if not chan:
        return
    welcomemsg = file.readyaml(chan, welcome_path)
    if welcomemsg == None:
        welcomemsg = welcome_default
        file.writeyaml(welcomemsg, chan, welcome_path)

    if not chan in welcome:
        welcome[chan] = dict()
        
    timeDelta = welcomemsg['partdelay'] + 1
    if user in welcome[chan]:
        if welcome[chan][user] == True:
            return
        timeDelta = datetime.now() - welcome[chan][user]
        timeDelta = timeDelta.total_seconds()

    if timeDelta <= welcomemsg['partdelay']:
        welcome[chan][user] = True
        return
    
    if user in welcomemsg['welcome']:
        sendmsg(
            chan,
            welcomemsg['welcome'][user].format(nick=user, chan=chan)
            )
        welcome[chan][user] = True
        return
    if user in operators:
        sendmsg(
            chan,
            random.choice(
                welcomemsg['welcome']['default']
                ).format(nick=user, chan=chan)
            )
        welcome[chan][user] = True
        return
