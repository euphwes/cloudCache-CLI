""" The cloudCache CLI application module. """

import sys, json
from os.path import exists, dirname, realpath, join

# -------------------------------------------------------------------------------------------------

# Get the dir of this script, and append the config filename to that path, since we want the config
# file to always be at the same location (next to the script), not in the working directory
CONFIG_FILE = join(dirname(realpath(__file__)), '.ccconfig')

# -------------------------------------------------------------------------------------------------

def ensure_config():
    """ Ensures a config file exists. Write default server location and port. Don't touch anything
    if the config file already exists. """

    if not exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as config_file:
            config = dict()
            config['server'] = 'localhost'
            config['port'] = '8888'
            config_file.write(json.dumps(config, indent=4, separators=(',', ': ')))


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    ensure_config()
