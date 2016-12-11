from datetime import datetime

from packages.configuration.file import writeyaml
from packages.irc.connect import sendmsg

def write_commands(string, chan):
    writeyaml(string, chan, 'commands.yaml')

def add_dur(string):
    repl = datetime.now()
    repl = repl.strftime('%Y-%m-%dT%H:%M:%SZ')

    return string.replace('$dur(now)', '$dur(' + repl + ')')

def add_cmd(arguments, chan, chat_cmd):
    cmd = arguments.pop(0).lower()
    string = ' '.join(arguments)

    if '$dur(now)' in string:
        string = add_dur(string)
    
    message = 'command ' + cmd + ' was edited.'
    if not cmd in chat_cmd['cmd']:
        message = 'command ' + cmd + ' was added.'
        
    chat_cmd['cmd'][cmd] = string

    sendmsg(
        chan,
        message
        )
    write_commands(chat_cmd, chan)

def app_cmd(arguments, chan, chat_cmd):
    cmd = arguments.pop(0).lower()
    string = ' '.join(arguments)

    if '$dur(now)' in string:
        string = add_dur(string)

    if not type(chat_cmd['cmd'][cmd]) == type(list()):
        chat_cmd['cmd'][cmd] = list(str(chat_cmd['cmd'][cmd]))

    chat_cmd['cmd'][cmd].append(string)
    sendmsg(
        chan,
        'Appending command to '+ cmd
        )
    write_commands(chat_cmd, chan)

def rem_cmd(arguments, chan, chat_cmd):
    cmd = arguments[0].lower()
    if cmd in chat_cmd['cmd']:
        del chat_cmd['cmd'][cmd]
    sendmsg(
        chan,
        'Command ' + cmd + ' has been removed.'
        )
    write_commands(chat_cmd, chan)
