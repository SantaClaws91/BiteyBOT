import socket
from packages.log import log

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send(plaintext):
    ircsock.send(bytes(plaintext, 'UTF-8'))

def connect(host, port, nick, password):
    ircsock.connect((host, port))

    if password:
        send("PASS " + password + "\n")
    send("USER " + nick + " " + nick + " " + nick + " : its biteybot\n")
    send("NICK " + nick + "\n")

def joinchan(chan):
    if not chan.startswith('#'):
        chan = '#'+ chan
    send("JOIN "+ chan +"\n")
    print("Joining channel: "+ chan)

def partchan(chan, config):
    if not chan.startswith('#'):
        chan = '#'+ chan
    config = readconfig()
    send("PART "+ chan +"\n")
    print("Parting channel: "+ chan)
    if chan in config['irc']['channels']:
        config['irc']['channels'].remove(chan)
        writeconfig(config)

def sendmsg(chan, msg):
    if not chan.startswith('#'):
        chan = '#'+ chan
    send("PRIVMSG "+ chan +" :"+ msg +"\n")

def on_connect(config):
    irc = config['irc']
    print("{} is connected.\n".format(irc['bot']['nick']))
    channels = irc['channels']
    if not channels:
        temp_chan = input("Insert channel: ")
        if not temp_chan.startswith('#'):
            temp_chan = '#'+ temp_chan
        channels.append(temp_chan)

    for chan in channels:
        joinchan(chan)
    
