def request_info(config):
    bot = config['irc']['bot']
    if not bot['host']:
        input_ = input("is host: irc.chat.twitch.tv (Y/n) ")
        if input_.lower() == "y":
            host = "irc.chat.twitch.tv"
            port = 6667
            bot['port'] = port
        else:
            host = input("Insert host address: ")
        bot['host'] = host
        port = None

    if not bot['port'] and not port:
        input_ = input("Is port 6667 (Y/n) ")
        if input_.lower() == "y":
            port = 6667
        else:
            port = int(input("Insert port: "))
        bot['port'] = port

    if not bot['nick']:
        nick = input("Insert bot nick: ")
        bot['nick'] = nick

    if not bot['password']:
        if bot['pswbool'] != False:
            password = input("Insert password (leave blank if non): ")
            bot['password'] = password
            if not password:
                bot['pswbool'] = False

    if not config['irc']['channels']:
        chan = input("Insert channel: ")
        if not chan.startswith('#'):
            chan = '#' + chan
        config['irc']['channels'].append(chan)
    return config

from packages.configuration.configuration import check_library, config
config = check_library(config)
config = request_info(config)
