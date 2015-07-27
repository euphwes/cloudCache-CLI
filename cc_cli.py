""" The cloudCache CLI application module. """

import sys, json
from os.path import exists, dirname, realpath, join

# -------------------------------------------------------------------------------------------------

# Get the dir of this script, and append the config filename to that path, since we want the config
# file to always be at the same location (next to the script), not in the working directory
CONFIG_FILE = join(dirname(realpath(__file__)), '.ccconfig')

# -------------------------------------------------------------------------------------------------

def load_config():
    """ Loads the config from the config file and returns it as a dict. """

    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)


def ensure_config():
    """ Ensures a config file exists. Write default server location and port. Don't touch anything
    if the config file already exists. """

    if not exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as config_file:
            config = dict()
            config['server'] = 'localhost'
            config['port'] = '8888'
            json.dump(config, config_file, indent=4, separators=(',', ': '))


def ensure_user():
    """ Make sure the config file has a user setup. If it doesn't, tell the user how to configure
    this, and then exit the script. """

    if 'user' in load_config():
        return

    # If we get here, there isn't a user configured. Alert the user and tell them how to configure
    print('\nPlease configure an existing cloudCache user by running the following command:')
    print('cc config user [username] --> ex: cc config user euphwes')
    print('\nTo create and configure a new user, run the following command:')
    print('cc newuser [username] --> ex: cc newuser euphwes')
    sys.exit(0)


def config_app(args):
    """ Configure the application with whatever value the user provides. """

    key, val = args[0], args[1]

    config = load_config()

    config[key] = val

    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file, indent=4, separators=(',', ': '))

    sys.exit(0)


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sys.argv.pop(0)  # discard the first argument, which is the script name

    ensure_config()

    CMD_DICT = {'config': config_app}

    # If the command is 'config', perform the config
    # If not, ensure a user exists in config and then run any other command
    if len(sys.argv) > 0:
        COMMAND = sys.argv.pop(0)

        if COMMAND == 'config':
            CMD_DICT[COMMAND](sys.argv)
        else:
            ensure_user()
