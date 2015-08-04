""" The cloudCache CLI application module. """

import sys, json, requests, arrow, tabulate
from os.path import exists, dirname, realpath, join

from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES
from Commands import ConfigAppCommand, ShowUsersCommand

# -------------------------------------------------------------------------------------------------

class CloudCacheCliApp(object):

    def __init__(self, args):
        # discard the first argument, which is the script name
        self.args = args[1:]

        # Get the dir of this script, and append the config filename to that path, since we want the config
        # file to always be at the same location (next to the script), not in the working directory
        self.config_file = join(dirname(realpath(__file__)), '.ccconfig')

        self._ensure_config()

        # If no arguments are provided, just echo the current configuration and exit the script
        if len(self.args) == 0:
            self.echo_config()
            sys.exit(0)

        self._build_commands()

        # Before executing any command, ensure a user is configured, ensure we have a valid
        # API key, and also an access token so we can be making API calls.
        self.ensure_user()
        self.ensure_api_key()
        self.ensure_access_token()


    def _build_commands(self):
        """ Build the Command objects. """

        self.commands = dict()
        self.commands['config'] = ConfigAppCommand
        self.commands['users']  = ShowUsersCommand

        """
        CMD_DICT = {
            'newuser'    : new_user,
            'newnotebook': new_notebook,
            'notebooks'  : show_notebooks,
            'newnote'    : new_note,
            'notes'      : show_notes
        }
        """


    def get_table(self, data, headers=[], indent=0, table_format='fancy_grid'):
        """ Get an ascii table string for a given set of values (list of lists), and column headers.
        Optional indentation. Defer to tabulate.tabulate for most of the work. This is mostly a
        convenience function for indenting a table.

        Args:
            data: Any data which can be fed to tabulate, nominally list of lists.
            headers (list of string): A list of values to be used as column headers
            indent (int): The number of spaces to indent table by. Defaults to 0 (no indentation).
            table_format (string): The tablefmt argument of tabulate.tabulate. Defaults to fancy_grid.

        Returns:
            string: The formatted table of data
        """

        table  = tabulate.tabulate(data, headers=headers, tablefmt=table_format)
        indent = ' ' * indent

        return '\n'.join(indent + line for line in table.split('\n'))


    def load_config(self):
        """ Loads the config from the config file and returns it as a dict. """

        with open(self.config_file, 'r') as config_file:
            return json.load(config_file)


    def save_config(self, config):
        """ Save the config info from the supplied dict to the config file as JSON. """

        with open(self.config_file, 'w') as config_file:
            json.dump(config, config_file, indent=4, separators=(',', ': '))


    def _ensure_config(self):
        """ Ensures a config file exists. Write default server location and port. Don't touch anything
        if the config file already exists. """

        if not exists(self.config_file):
            config = {CFG_SERVER: 'localhost', CFG_PORT: '8888'}
            self.save_config(config)


    def echo_config(self):
        """ Echos the current configuration to the console. Right-justifies all the configuration
        keys to make it easier to read. """

        config  = self.load_config()
        headers = ['Configuration option', 'Value']
        data    = [[key, config[key]] for key in sorted(config.keys())]

        print('')
        print(self.get_table(data, headers=headers, indent=2))


    def ensure_user(self):
        """ Make sure the config file has a user setup. If it doesn't, tell the user how to configure
        this, and then exit the script. """

        if CFG_USER in self.load_config():
            return

        # If we get here, there isn't a user configured. Alert the user and tell them how to configure
        print('\nPlease configure an existing cloudCache user by running the following command:')
        print('cc config user [username] --> ex: cc config user euphwes')
        print('\nTo create and configure a new user, run the following command:')
        print('cc newuser [username] --> ex: cc newuser euphwes')
        sys.exit(0)


    def ensure_api_key(self):
        """ Make sure we have an API key for the configured user. If we don't, make the appropriate
        API call to get one. """

        config = self.load_config()

        if CFG_API_KEY in config:
            return

        # If we get here, we don't have an API key, so let's go get one
        url = '{}/users/{}'.format(self.base_url(), config[CFG_USER])

        response = requests.get(url)
        results  = json.loads(response.text)

        if response.status_code == 200:
            config[CFG_API_KEY] = results['user']['api_key']
            self.save_config(config)
        else:
            print('\n** {} **'.format(results['message']))
            sys.exit(0)


    def base_url(self):
        """ Build and return the base URL for the API endpoints. """
        config = self.load_config()
        return 'http://{}:{}'.format(config[CFG_SERVER], config[CFG_PORT])


    def ensure_access_token(self):
        """ Make sure the config file has an access token, which is not expired. If it's expired,
        delete it and obtain a new one. """

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
        url = '{}/access/{}/{}'.format(self.base_url(), config[CFG_USER], config[CFG_API_KEY])

        response = requests.get(url)
        results  = json.loads(response.text)

        if response.status_code == 200:
            config[CFG_ACCESS_TOKEN]  = results['access token']['access_token']
            config[CFG_TOKEN_EXPIRES] = results['access token']['expires_on']
            self.save_config(config)

        else:
            print('\n** {} **'.format(response['message']))
            sys.exit(0)


    def show_notebooks(args):
        """ Show all notebooks for this user. """

        config = load_config()

        url = '{}/notebooks'.format(base_url())
        headers = {'access token': config[CFG_ACCESS_TOKEN]}

        response = requests.get(url, headers=headers)
        results = json.loads(response.text)

        if response.status_code == 200:
            if len(results['notebooks']) == 0:
                print('\n' + get_table([['No notebooks exist for this user']], indent=2))
            else:
                headers = ['ID', 'Notebook Name']
                data = [[nb['id'], nb['name']] for nb in results['notebooks']]
                print('\n' + get_table(data, headers=headers, indent=2))
        else:
            print('\n** {} **'.format(results['message']))


    def show_notes(args):
        """ Show all notes for this user's notebook. """

        config = load_config()

        url = '{}/notebooks/{}/notes/'.format(base_url(), args[0])
        headers = {'access token': config[CFG_ACCESS_TOKEN]}

        response = requests.get(url, headers=headers)
        results = json.loads(response.text)

        if response.status_code == 200:
            if len(results['notes']) == 0:
                print('\n' + get_table([['This notebook does not have any notes yet.']], indent=2))
            else:
                print('\n' + get_table([[results['notebook']]], indent=2))
                data    = [[note['key'], note['value']] for note in results['notes']]
                headers = ['Note name', 'Note contents']
                print(get_table(data, headers=headers, indent=6))
        else:
            print('\n** {} **'.format(results['message']))


    def new_notebook(args):
        """ Create a new notebook. """

        config = load_config()

        headers = {'access token': config[CFG_ACCESS_TOKEN]}
        body    = {'notebook_name': args[0]}

        url = '{}/notebooks'.format(base_url())

        response = requests.post(url, headers=headers, data=json.dumps(body))

        if response.status_code != 200:
            print('\n** {} **'.format(json.loads(response.text)['message']))


    def new_note(args):
        """ Create a new note. """

        config = load_config()

        headers = {'access token': config[CFG_ACCESS_TOKEN]}
        body    = {
            'note_key'     : args[1],
            'note_value'   : args[2]
        }

        notebook = args[0]

        url = '{}/notebooks/{}/notes'.format(base_url(), notebook)

        response = requests.post(url, headers=headers, data=json.dumps(body))

        if response.status_code != 200:
            print('\n** {} **'.format(json.loads(response.text)['message']))


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
        results  = json.loads(response.text)

        if response.status_code == 200:
            config = load_config()
            if CFG_ACCESS_TOKEN in config:
                del config[CFG_ACCESS_TOKEN]
            config[CFG_USER]    = args[0]
            config[CFG_API_KEY] = results['api_key']
            save_config(config)

        else:
            print('\n** {} **'.format(results['message']))


    def action(self):
        """ Perform the selected command action. """

        try:
            command = self.args.pop(0)
            self.commands[command](self.args, self).action()

        except requests.exceptions.ConnectionError:
            print('\nUnable to connect to the cloudCache server.')
            print('Ensure your server host and port configuration is correct, and that the server is running.')

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    
    app = CloudCacheCliApp(sys.argv)
    app.action()
