from packages.irc import connect
from packages.log import log
import time

from packages.configuration import file
from packages.configuration import configuration
from packages.configuration.userinfo import config
from packages.commands import handler
from packages.welcome import welcome

bot = config['irc']['bot']

connect.connect(
    bot['host'],
    bot['port'],
    bot['nick'],
    bot['password']
    )

ircsock = connect.ircsock

reconnect = 0

print('Connecting to ' + bot['host'] + '...')
log.ircLog.info('Connecting to ' + bot['host'] + '...')
from packages.twitch.moderators import operators

while 1:
    try:
        ircmsg = ircsock.recv(4096).decode('UTF-8')
        if not ircmsg:
            if reconnect > 3:
                print('Connection failed. Check to see if server information is configured correctly')
                log.mainLog.debug('Connection failed. Check to see if server information is configured correctly')
                raise SystemExit
            reconnect += 1
            time.sleep(10)
            print('Attempting reconnect...')
            log.mainLog.debug('Attempting reconnect...')
            connect(
                bot['host'],
                bot['port'],
                bot['nick'],
                bot['password']
                )
            continue
        temp = ircmsg.split('\n')
        
        for line in temp:
            line = line.rstrip()
            ##log.ircLog.debug(line)

            if line.startswith('PING'):
                connect.send('PONG ' + line.split(':')[1] + '\r\n')
                continue
            data = line.split(' ')
            
            if len(data) < 2:
                continue
            if data[1] == '001':        #irc code for welcome message.
                configuration.writeconfig(config)
                connect.on_connect(config)
                if bot['host'] == 'irc.chat.twitch.tv' or bot['host'] == 'irc.twitch.tv':
                    connect.send('CAP REQ :twitch.tv/membership\r\n')
                continue
            if data[1] in ['002', '003', '004', '353', '366', '372', '375', '376', 'CAP']:
                #This is all junk causing unnecessary errors.
                continue

            user = data.pop(0)
            if '!' in user:
                user = user.split('!')[0][1:]
            if user == bot['nick']:
                continue
            if user == '*':
                continue
            method = data.pop(0)
            chan = data.pop(0).strip(':').strip('#')

            welcome.greeting(user, chan, operators[chan])
            
            if method == 'MODE':
                if not user.strip(':') == 'jtv':
                    continue
                if data[0] == '-o':
                    continue
                if not chan in operators:
                    operators[chan] = list()
                
                if data[1] in operators[chan]:
                    continue
                operators[chan].append(data[1])
                file.writeyaml(operators[chan], chan, 'operators.yml')
                continue

            if method == 'PART':
                #Assign part time to welcome msg here...
                welcome.on_part(user, chan)
                continue
            
            if method != 'PRIVMSG':
                continue
            if handler.command_handling(user, data, chan) == True:
                continue

            #auto_post handling here...
            
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        log.mainLog.exception('Got exception on main handler')

