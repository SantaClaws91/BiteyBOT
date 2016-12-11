from packages.twitch import request
from packages.configuration import file
from packages.welcome import welcome

def save_ops(chan, wlcm=False):
    chan = chan.strip('#').strip(':')
    op = file.readyaml(chan, 'operators.yml')
    if op == None:
        op = list()
    temp_op = request.operators(chan)
    if not temp_op:
        return list()
    if temp_op == None:
        return list()
    for user in temp_op:
        if wlcm:
            welcome.on_start(temp_op, chan)
        if user not in op:
            op.append(user)
    file.writeyaml(op, chan, 'operators.yml')
    return op

from packages.configuration.configuration import config
from packages.log.log import ircLog

operators = dict()
for chan in config['irc']['channels']:
    chan = chan.strip('#').strip(':')
    operators[chan] = list(save_ops(chan, wlcm=True))
    ircLog.info('Collecting operators for #'+ chan)
