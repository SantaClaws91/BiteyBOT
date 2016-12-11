import yaml

from packages.log import log

def readconfig():
    try:
        with open('config.yaml', 'r') as stream:
            return yaml.load(stream)
    except FileNotFoundError:
        log.mainLog.info('Config file not found. Creating new configurations...')
        writeconfig(default_config)
        return default_config
    except yaml.YAMLError:
        from os import rename
        rename('config.yaml', 'config.yaml.corrupted')
        writeconfig(default_config)
        return default_config

def writeconfig(string):
    with open("config.yaml", 'w') as stream:
        yaml.dump(string, stream, default_flow_style=False)
        return default_config

default_config = {
    'timezone_difference': 0,
    'irc': {
      'bot': {
        'nick': '',
        'host': '',
        'port': '',
        'password': '',
        'pswbool': ''
        },
      'channels': []
      },
    'admin': []
    }

def check_library(config):
    for item in default_config:
        if not item in config:
            config[item] = default_config[item]
            continue
        if not default_config[item]:
            continue
        for item2 in default_config[item]:
            if not item2 in config[item]:
                config[item][item2] = default_config[item][item2]
                continue
            if not default_config[item][item2]:
                continue
            for item3 in default_config[item][item2]:
                if not item3 in config[item][item2]:
                    config[item][item2][item3] = default_config[item][item2][item3]
                    continue
                if not default_config[item][item2][item3]:
                        continue
                for item4 in default_config[item][item2][item3]:
                    if not item4 in config[item][item2][item3]:
                        config[item][item2][item3][item4] = default_config[item][item2][item3][item4]
                        continue
    return config

config = readconfig()
