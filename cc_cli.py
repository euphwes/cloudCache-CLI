""" The cloudCache CLI application module. """

import sys, json, requests
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


def save_config(config):
    """ Save the config info from the supplied dict to the config file as JSON. """

    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file, indent=4, separators=(',', ': '))


def ensure_config():
    """ Ensures a config file exists. Write default server location and port. Don't touch anything
    if the config file already exists. """

    if not exists(CONFIG_FILE):
        config = {'server': 'localhost', 'port': '8888'}
        save_config(config)


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
    """ Configure the application with either the user, the server, or the port. """

    key, val = args[0], args[1]

    if key not in ('user', 'server', 'port', 'api key', 'access token', 'token expires'):
        print('\nThe configuration option "{}"" is not valid.'.format(key))
        print('You may only configure "user", "server", or "port".')
        sys.exit(0)

    config = load_config()
    config[key] = val
    save_config(config)
    echo_config()


def new_user(args):
    """ Create a new user, and save the relevant details to the config. """

    body = {
        'username'  : args[0],
        'first_name': args[1],
        'last_name' : args[2],
        'email'     : args[3]
    }

    config = load_config()
    url = 'http://{}:{}/users/'.format(config['server'], config['port'])

    response = requests.post(url, data=json.dumps(body))
    response = json.loads(response.text)

    if response['status'] == 'OK':
        config['user']    = response['user']['username']
        config['api key'] = response['user']['api_key']
        save_config(config)
    else:
        print('\n** {} **'.format(response['message']))

    echo_config()


def echo_config():
    """ Echos the current configuration to the console. Right-justifies all the configuration
    keys to make it easier to read. """

    config = load_config()
    max_key_length = max(len(key) for key in config.keys())

    print('\ncloudCache CLI current configuration:\n')
    for config_key, config_val in config.items():
        print('\t{}: {}'.format(config_key.rjust(max_key_length), config_val))

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    sys.argv.pop(0)  # discard the first argument, which is the script name

    CMD_DICT = {
        'config' : config_app,
        'newuser': new_user
    }

    ensure_config()

    # If no arguments are provided, just echo the current configuration and exit the script
    if len(sys.argv) == 0:
        echo_config()
        sys.exit(0)

    # If the command is 'config', perform the configuration and exit the script
    # If the command is 'newuser', create the user via the REST API, save config, and exit
    COMMAND = sys.argv.pop(0)
    if COMMAND in ('config', 'newuser'):
        CMD_DICT[COMMAND](sys.argv)
        sys.exit(0)

    # Before executing any other command, ensure a user is configured
    ensure_user()
