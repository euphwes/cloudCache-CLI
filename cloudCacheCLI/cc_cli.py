""" The cloudCache CLI application module. """

import sys
import json
from os.path import dirname, realpath, join

import requests

from cloudCacheCLI import CFG_ACCESS_TOKEN
from Commands import CommandValidationError, ConfigAppCommand, ShowUsersCommand, ShowNotebooksCommand, NewUserCommand
from ConfigManager import ConfigManager

# -------------------------------------------------------------------------------------------------

class CloudCacheCliApp(object):

    def __init__(self, args):
        # discard the first argument, which is the script name
        self.args = args[1:]
        self._build_commands()

        self.config_manager = ConfigManager(join(dirname(realpath(__file__)), '.ccconfig'))

        # if the command is config or newuser, do this before doing any 'ensure_x' steps in the config manager
        if len(self.args) > 0 and self.args[0] in ['newuser', 'config']:
            self.action()
            return

        # If no arguments are provided, just echo the current configuration and exit the script
        if len(self.args) == 0:
            self.config_manager.echo_config()
            sys.exit(0)

        # Before executing any command (other than config or newuser), ensure a user is configured, ensure we have a
        # valid API key, and also an access token so we can be making API calls.
        self.config_manager.ensure_user()
        self.config_manager.ensure_api_key()
        self.config_manager.ensure_access_token()

        # Execute any other command now
        self.action()


    def _build_commands(self):
        """ Build the Command objects. """

        self.commands = {
            'config'   : ConfigAppCommand,
            'users'    : ShowUsersCommand,
            'notebooks': ShowNotebooksCommand,
            'newuser'  : NewUserCommand
        }

        """
        CMD_DICT = {
            'newnotebook': new_notebook,
            'notebooks'  : show_notebooks,
            'newnote'    : new_note,
            'notes'      : show_notes
        }
        """



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


    def action(self):
        """ Perform the selected command action. """

        try:
            command = self.args.pop(0)
            self.commands[command](self.args, self)

        except requests.exceptions.ConnectionError:
            msg  = '\nUnable to connect to the cloudCache server.'
            msg += '\nEnsure your server host and port configuration is correct, and that the server is running.'
            print(msg)

        except CommandValidationError as error:
            print('\n{}'.format(error))

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = CloudCacheCliApp(sys.argv)
