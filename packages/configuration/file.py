import os
import yaml
from packages.log import log

def mkdir(chan):
    chan = chan.strip('#')
    dir_ = 'channels/' + chan
    if not os.path.exists(dir_):
        os.makedirs(dir_)

def readyaml(chan, file):
    chan = chan.strip('#')
    try:
        with open('channels/{chan}/{file}'.format(chan=chan, file=file), 'r') as stream:
            return yaml.load(stream)
    except FileNotFoundError:
        log.mainLog.debug('File {chan}/{file} not found.'.format(chan=chan, file=file))
        writeyaml(dict(), chan, file)
        return None

def writeyaml(string, chan, file):
    chan = chan.strip('#')
    mkdir(chan)
    with open('channels/{chan}/{file}'.format(chan=chan, file=file), 'w') as stream:
        yaml.dump(string, stream, default_flow_style=False)
