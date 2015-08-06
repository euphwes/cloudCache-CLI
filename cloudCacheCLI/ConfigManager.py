""" The configuration manager class. """

import json
import sys
from os.path import exists
from getpass import getpass

import arrow

import requests

from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES
from cloudCacheCLI.Utilities import get_table

# ---------------------------------------------------------------------------------------------------------------------

class ConfigManager(object):
    """ Manages the cloucCache CLI application configuration. """

    def __init__(self, config_path):
        self.config_file = config_path
        self._ensure_config()

        config = self.load_config()
        self.base_url = 'http://{}:{}'.format(config[CFG_SERVER], config[CFG_PORT])


    def ensure_user(self):
        """ Make sure the config file has a user setup. If it doesn't, tell the user how to configure
        this, and then exit the script. """

        if CFG_USER in self.load_config():
            return

        # If we get here, there isn't a user configured. Alert the user and tell them how to configure
        print('\nPlease configure an existing cloudCache user by running the following command:')
        print('cc config user [username] --> ex: cc config user euphwes')
        print('\nTo create and configure a new user, run the following command:')
        print('cc newuser [username] [first name] [last name] [email] --> ex: cc newuser euphwes Wes Evans euphwes@gmail.com')
        sys.exit(0)


    def ensure_access_token(self):
        """ Make sure the config file has an access token, which is not expired. If it's expired, delete it and obtain
        a new one. """

        config = self.load_config()

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
                self.save_config(config)

        # If we get here, either the token doesn't exist, or was expired and deleted. Get a new one
        url = '{}/access/{}/{}'.format(self.base_url, config[CFG_USER], config[CFG_API_KEY])

        response = requests.get(url)
        results  = json.loads(response.text)

        if response:
            config[CFG_ACCESS_TOKEN]  = results['access token']['access_token']
            config[CFG_TOKEN_EXPIRES] = results['access token']['expires_on']
            self.save_config(config)

        else:
            # Probably because the user configured doesn't exist. Don't bother trying to continue on, just exit
            print('\n' + response['message'])
            sys.exit(0)


    def ensure_api_key(self):
        """ Make sure we have an API key for the configured user. If we don't, make the appropriate
        API call to get one. """

        config = self.load_config()

        if CFG_API_KEY in config:
            return

        # If we get here, we don't have an API key, so let's go get one
        url = '{}/users/{}'.format(self.base_url, config[CFG_USER])

        response = requests.get(url, data=json.dumps({'password': getpass('\nPassword: ')}))
        results  = json.loads(response.text)

        if response:
            config[CFG_API_KEY] = results['user']['api_key']
            self.save_config(config)
        else:
            # Probably because the user configured doesn't exist, or password is wrong
            print('\n' + results['message'])
            raise Exception()


    def _ensure_config(self):
        """ Ensures a config file exists. Write default server location and port. Don't touch anything
        if the config file already exists. """
        if not exists(self.config_file):
            config = {CFG_SERVER: 'localhost', CFG_PORT: '8888'}
            self.save_config(config)


    def load_config(self):
        """ Loads the config from the config file and returns it as a dict. """
        with open(self.config_file, 'r') as config_file:
            return json.load(config_file)


    def save_config(self, config):
        """ Save the config info from the supplied dict to the config file as JSON. """
        with open(self.config_file, 'w') as config_file:
            json.dump(config, config_file, indent=4, separators=(',', ': '))


    def echo_config(self):
        """ Echos the current configuration to the console. Right-justifies all the configuration
        keys to make it easier to read. """

        config  = self.load_config()
        headers = ['Configuration option', 'Value']
        data    = [[key, config[key]] for key in sorted(config.keys())]

        print('')
        print(get_table(data, headers=headers, indent=2))