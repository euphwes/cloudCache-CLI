""" The cloudCache CLI application module. """

import sys, json
from os.path import exists

# -------------------------------------------------------------------------------------------------

CONFIG_FILE = '.ccconfig'

# -------------------------------------------------------------------------------------------------

def ensure_config():
    """ Ensures a config file exists. Write default server location and port. """

    if not exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as config_file:
            config = dict()
            config['server'] = 'localhost'
            config['port'] = '8888'
            config_file.write(json.dumps(config, indent=4, separators=(',', ': ')))


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    ensure_config()
