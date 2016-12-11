from datetime import datetime

from packages.configuration import file, configuration
from packages.irc.connect import sendmsg
from packages.log.log import ircLog
from packages.commands import addcmd
from packages.commands.convertmsg import convert, repl_msg
from packages.points import points
from packages.irc.connect import joinchan, partchan
from packages.twitch import editors

command_executed = dict()

def command_handling(user, arguments, chan):
    chan = chan.strip('#').strip(':')

    chat_cmd = file.readyaml(chan, 'commands.yaml')

    if not chat_cmd:
        chat_cmd = {
            'cmd': dict(),
            'delay': 45
            }
        addcmd.write_commands(chat_cmd, chan)
    cmd = chat_cmd['cmd']
    delay = chat_cmd['delay']

    if not chan in command_executed:
        command_executed[chan] = {
            'cmd': dict(),
            'auto_post': list(),
            'points': dict()
            }
    cmd_ex = command_executed[chan]
    command = arguments.pop(0).strip(':').lower()
    #Non operator commands:
    if command in cmd:
        if command in cmd_ex['cmd']:
            timeDelta = datetime.now() - cmd_ex['cmd'][command]
            if timeDelta.total_seconds() < delay:
                return True

        message = cmd[command].format(nick=user, chan=chan)
        message = repl_msg(arguments, message)
        message = convert(message, chan)

        ##Points:
        if '$points' in message:
            point_count = points.announce(user, chan)
            if point_count == None:
                return True
            message = message.replace('$points', str(point_count))
            
        sendmsg(
            chan,
            message
            )
        ircLog.info('Executing command: '+ message)
        cmd_ex['cmd'][command] = datetime.now()
        return True

    points_ = file.readyaml(chan, 'points.yml')
    if points_:
        if 'cmd' in points_:
            point_cmd = points_['cmd']

            if command == point_cmd:
                if user in cmd_ex['points']:
                    timeDelta = datetime.now() - cmd_ex['points'][user]
                    if timeDelta < points_['delay']:
                        return True
                if points.on_add(user, chan, arguments[0]) == None:
                    return True
                ircLog.info(user + ' gave ' + arguments[0] + ' a '+ point_cmd)
                cmd_ex['points'][user] = datetime.now()
                return True

    from __main__ import operators
    
    #Admin Commands:
    if user in configuration.config['admin']:
        if command == '$part':
            partchan(arguments[0].strip('#').strip(':'))
            return True
        
        elif command == '$join':
            newchan = arguments[0].strip('#').strip(':')
            if not newchan in operators:
                from packages.twitch.moderators import save_ops
                operators[newchan] = list(save_ops(newchan, wlcm=True))
            joinchan(newchan)
            configuration.config['irc']['channels'].append('#' + newchan)
            configuration.writeconfig(configuration.config)
            return True

    #Operator commands:
    if not user in operators[chan]:
        return True

    if command == '#add':
        addcmd.add_cmd(arguments, chan, chat_cmd)
        return True
    if command == '#app':
        addcmd.app_cmd(arguments, chan, chat_cmd)
        return True
    if command in ['#rem',  '#del', '#remove']:
        addcmd.rem_cmd(arguments, chan, chat_cmd)
        return True
    if command == '#points':
        points.points_prefix(arguments[0], chan)
        return True
    if command == '#topic':
        editors.new_topic(' '.join(arguments), chan)
        return True
    if command == '#game':
        editors.new_game(' '.join(arguments), chan)
        return True
