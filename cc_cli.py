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

RESP_OK     = 'OK'
RESP_ERR    = 'Error'
RESP_STATUS = 'status'

# -------------------------------------------------------------------------------------------------

def base_url():
    """ Build and return the base URL for the API endpoints. """

    config = load_config()
    server = config[CFG_SERVER]
    port   = config[CFG_PORT]
    return 'http://{}:{}'.format(server, port)


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
    url = '{}/users/{}'.format(base_url(), config[CFG_USER])

    response = requests.get(url)
    response = json.loads(response.text)

    if response[RESP_STATUS] == RESP_OK:
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
            # token exists, and is still valid, so we can use it
            return
        else:
            # token exists, but is expired, so delete it
            for key in (CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES):
                if key in config:
                    del config[key]
            save_config(config)

    # If we get here, either the token doesn't exist, or was expired and deleted. Get a new one
    url = '{}/access/{}/{}'.format(base_url(), config[CFG_USER], config[CFG_API_KEY])

    response = requests.get(url)
    response = json.loads(response.text)

    if response[RESP_STATUS] == RESP_OK:
        config[CFG_ACCESS_TOKEN]  = response['access token']['access_token']
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
        print('You may only configure "{}", "{}", or "{}".'.format(CFG_USER, CFG_PORT, CFG_SERVER))
        sys.exit(0)

    config = load_config()
    config[key] = val

    # If we're changing the user, delete any access token and api key since those will be invalid
    if key == CFG_USER:
        for del_key in (CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES):
            if del_key in config:
                del config[del_key]

    save_config(config)


def show_users(args):
    """ Show all users. """

    config = load_config()

    url = '{}/users'.format(base_url())

    headers = {'access token': config[CFG_ACCESS_TOKEN]}

    response = requests.get(url, headers=headers)
    response = json.loads(response.text)

    if response[RESP_STATUS] == RESP_OK:
        print('')
        for user in response['users']:
            print('\t{}'.format(user['username']))
    else:
        print('\n** {} **'.format(response['message']))


def new_notebook(args):
    """ Create a new notebook. """

    config = load_config()

    headers = {'access token': config[CFG_ACCESS_TOKEN]}
    body    = {'notebook_name': args[0]}

    url = '{}/users/{}/notebooks'.format(base_url(), config[CFG_USER])

    response = requests.post(url, headers=headers, data=json.dumps(body))
    response = json.loads(response.text)

    if response[RESP_STATUS] == RESP_ERR:
        print('\n** {} **'.format(response['message']))


def new_user(args):
    """ Create a new user, and save the relevant details to the config. """

    body = {
        'username'  : args[0],
        'first_name': args[1],
        'last_name' : args[2],
        'email'     : args[3]
    }

    url = '{}/users/'.format(base_url())

    response = requests.post(url, data=json.dumps(body))
    response = json.loads(response.text)

    config = load_config()
    if response[RESP_STATUS] == RESP_OK:
        del config[CFG_ACCESS_TOKEN]
        config[CFG_USER]    = response['user']['username']
        config[CFG_API_KEY] = response['user']['api_key']
        save_config(config)
    else:
        print('\n** {} **'.format(response['message']))


def echo_config():
    """ Echos the current configuration to the console. Right-justifies all the configuration
    keys to make it easier to read. """

    config = load_config()
    max_key_length = max(len(key) for key in config.keys())

    print('\ncloudCache CLI current configuration:\n')
    for config_key in sorted(config.keys()):
        config_val = config[config_key]
        print('\t{}: {}'.format(config_key.rjust(max_key_length), config_val))

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    sys.argv.pop(0)  # discard the first argument, which is the script name

    CMD_DICT = {
        'config'     : config_app,
        'newuser'    : new_user,
        'users'      : show_users,
        'newnotebook': new_notebook,
    }

    # Before executing any command, ensure a user is configured, ensure we have a valid API key,
    # and also an access token so we can be making API calls.
    ensure_config()
    ensure_user()
    ensure_api_key()
    ensure_access_token()

    # If no arguments are provided, just echo the current configuration and exit the script
    if not sys.argv:
        echo_config()
        sys.exit(0)

    # Pop the first item in the argument stack to get the command, and then pass the remaining
    # arguments to that command to execute it
    COMMAND = sys.argv.pop(0)
    CMD_DICT[COMMAND](sys.argv)
