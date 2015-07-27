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


def ensure_user():
    """ Make sure the config file has a user setup. If it doesn't, tell the user how to configure
    this, and then exit the script. """

    with open(CONFIG_FILE, 'r') as config_file:
        config = json.load(config_file)

    if 'user' in config:
        return

    # If we get here, there isn't a user configured. Alert the user and tell them how to configure
    print('\nPlease configure an existing cloudCache user by running the following command:')
    print('cc config user [username] --> ex: cc config user euphwes')
    print('\nTo create and configure a new user, run the following command:')
    print('cc newuser [username] --> ex: cc newuser euphwes')
    sys.exit(0)


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    ensure_config()
    ensure_user()
