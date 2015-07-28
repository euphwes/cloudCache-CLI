""" The cloudCache CLI application module. """

import sys, json, requests, arrow
from os.path import exists, dirname, realpath, join

# -------------------------------------------------------------------------------------------------

# Get the dir of this script, and append the config filename to that path, since we want the config
# file to always be at the same location (next to the script), not in the working directory
CONFIG_FILE = join(dirname(realpath(__file__)), '.ccconfig')

# -------------------------------------------------------------------------------------------------

CFG_SERVER        = 'server'
CFG_PORT          = 'port'
CFG_USER          = 'user'
CFG_API_KEY       = 'api key'
CFG_ACCESS_TOKEN  = 'access token'
CFG_TOKEN_EXPIRES = 'token expires'

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
        config = {CFG_SERVER: 'localhost', CFG_PORT: '8888'}
        save_config(config)


def ensure_user():
    """ Make sure the config file has a user setup. If it doesn't, tell the user how to configure
    this, and then exit the script. """

    if CFG_USER in load_config():
        return

    # If we get here, there isn't a user configured. Alert the user and tell them how to configure
    print('\nPlease configure an existing cloudCache user by running the following command:')
    print('cc config user [username] --> ex: cc config user euphwes')
    print('\nTo create and configure a new user, run the following command:')
    print('cc newuser [username] --> ex: cc newuser euphwes')
    sys.exit(0)


def ensure_api_key():
    """ Make sure we have an API key for the configured user. If we don't, make the appropriate
    API call to get one. """

    config = load_config()

    if CFG_API_KEY in config:
        return

    # If we get here, we don't have an API key, so let's go get one
    server   = config[CFG_SERVER]
    port     = config[CFG_PORT]
    username = config[CFG_USER]
    url      = 'http://{}:{}/users/{}'.format(server, port, username)

    response = requests.get(url)
    response = json.loads(response.text)

    if response['status'] == 'OK':
        config[CFG_API_KEY] = response['user']['api_key']
        save_config(config)
    else:
        print('\n** {} **'.format(response['message']))
        sys.exit(0)


def ensure_access_token():
    """ Make sure the config file has an access token, which is not expired. If it's expired,
    delete it and obtain a new one. """

    config = load_config()

    if CFG_ACCESS_TOKEN in config and CFG_TOKEN_EXPIRES in config:
        token_time = arrow.get(config[CFG_TOKEN_EXPIRES])
        if token_time > arrow.now():
            # token exists, and is still valid, so we can return
            return
        else:
            # token exists, but is expired, so delete it
            del config[CFG_ACCESS_TOKEN]
            del config[CFG_TOKEN_EXPIRES]
            save_config(config)

    # If we get here, either the token doesn't exist, or was expired and deleted. Get a new one
    server   = config[CFG_SERVER]
    port     = config[CFG_PORT]
    username = config[CFG_USER]
    api_key  = config[CFG_API_KEY]
    url      = 'http://{}:{}/access/{}/{}'.format(server, port, username, api_key)

    response = requests.get(url)
    response = json.loads(response.text)

    if response['status'] == 'OK':
        config[CFG_ACCESS_TOKEN] = response['access token']['access_token']
        config[CFG_TOKEN_EXPIRES] = response['access token']['expires_on']
        save_config(config)
    else:
        print('\n** {} **'.format(response['message']))
        sys.exit(0)


def config_app(args):
    """ Configure the application with either the user, the server, or the port. """

    key, val = args[0], args[1]

    if key not in (CFG_USER, CFG_SERVER, CFG_PORT):
        print('\nThe configuration option "{}"" is not valid.'.format(key))
        print('You may only configure "user", "server", or "port".')
        sys.exit(0)

    config = load_config()
    config[key] = val

    # If we're changing the user, delete any access token and api key since those will be invalid
    if key == CFG_USER:
        for del_key in (CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES):
            if del_key in config:
                del config[del_key]

    save_config(config)
    echo_config()


def show_users(args):
    """ Show all users. """

    config = load_config()

    server       = config[CFG_SERVER]
    port         = config[CFG_PORT]
    username     = config[CFG_USER]
    access_token = config[CFG_ACCESS_TOKEN]

    headers = {
        'username'    : username,
        'access token': access_token
    }

    url = 'http://{}:{}/users'.format(server, port)

    response = requests.get(url, headers=headers)
    response = json.loads(response.text)

    if response['status'] == 'OK':
        print('')
        for user in response['users']:
            print('\t{}'.format(user['username']))
    else:
        print('\n** {} **'.format(response['message']))


def new_user(args):
    """ Create a new user, and save the relevant details to the config. """

    body = {
        'username'  : args[0],
        'first_name': args[1],
        'last_name' : args[2],
        'email'     : args[3]
    }

    config = load_config()
    url = 'http://{}:{}/users/'.format(config[CFG_SERVER], config[CFG_PORT])

    response = requests.post(url, data=json.dumps(body))
    response = json.loads(response.text)

    if response['status'] == 'OK':
        config[CFG_USER]    = response['user']['username']
        config[CFG_API_KEY] = response['user']['api_key']
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
        'newuser': new_user,
        'users'  : show_users
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

    # Before executing any other command, ensure a user is configured, ensure we have a valid
    # API key, and also an access token so we can be making API calls.
    ensure_user()
    ensure_api_key()
    ensure_access_token()

    CMD_DICT[COMMAND](sys.argv)
