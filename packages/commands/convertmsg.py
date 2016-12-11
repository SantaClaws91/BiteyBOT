import re
import random

from packages.time import time
from packages.configuration import file
from packages.steam import request
from packages.twitch.request import get_twitch_info

def convert(message, chan):
    arguments = message.split()
    if type(message) == type(list()):
        message = rand_repl_msg(message)

    message = time.match_datetime(message)       #Needs revisiting. See time.py
##    message = repl_msg(message)

    if '$topic' in message or '$uptime' in message:
        twitch_info = get_twitch_info('streams', chan)
        if twitch_info == None:
            return ''
        message = time.uptime(message, twitch_info)
        message = twitch_topic(message, twitch_info)

    if '$played(' in message or '$playedrecent(' in message:
        steamID = file.readyaml(chan, 'userinfo.yml')
        if steamID:
            if 'steamID' in steamID:
                steamID = steamID['steamID']
                message = request.replace_string(message, steamID)

    return message
        
def rand_repl_msg(cmd):
    if not cmd:
        return
    arguments = cmd.split()
    n_args = len(arguments)
    temp_cmd = list(cmd)

    while n_args >= 0:
        if not temp_cmd:
            n_args -= 1
            temp_cmd = list(cmd)
            
        choice = random.choice(temp_cmd)
        temp_cmd.remove(choice)
        
        if n_args == 0:
            match = re.match(
                '.*(\$\d).*',
                choice
                )
            if match:
                continue
            return choice

        if not '$' + str(n_args) in choice:
            continue
        if '$' + str(n_args + 1) in choice:
            continue
        return choice

def repl_msg(arguments, string):
    match = re.findall(
        '\$(\d)',
        string
        )
    if not match:
        return string
    
    for m in match:
        i = int(m) - 1
        if not arguments[i]:
            return ''
        string = string.replace('$' + m, arguments[i])

    return string

def twitch_topic(string, twitch_info):
    if not '$topic' in string:
        return string

    if not twitch_info:
        return string.replace('$topic', 'None')

    if 'channel' in twitch_info:
        twitch_info = twitch_info['channel']
    else:
        return string
    if not 'status' in twitch_info:
        return string
    topic = twitch_info['status']
    return string.replace('$topic', topic)
