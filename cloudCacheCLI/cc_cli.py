""" The cloudCache CLI application module. """

import sys
import json
from os.path import dirname, realpath, join

import requests

from ConfigManager import ConfigManager
from cloudCacheCLI import CFG_ACCESS_TOKEN
from Commands import CommandValidationError, ConfigAppCommand, ShowUsersCommand, ShowNotebooksCommand, NewUserCommand,\
    ShowNotesCommand, NewNotebookCommand

# -------------------------------------------------------------------------------------------------

class CloudCacheCliApp(object):

    def __init__(self, args):
        # discard the first argument, which is the script name
        self.args = args[1:]
        self.config_manager = ConfigManager(join(dirname(realpath(__file__)), '.ccconfig'))

        # If no arguments are provided, just echo the current configuration and exit the script
        if len(self.args) == 0:
            self.config_manager.echo_config()
            sys.exit(0)

        self._build_commands()
        self.command = self.commands[self.args.pop(0)]

        if not (self.command is ConfigAppCommand or self.command is NewUserCommand):
            # Before executing any command other than config or newuser, ensure a user is configured, ensure we have a
            # valid API key, and also an access token so we can be making API calls.
            self.config_manager.ensure_user()
            self.config_manager.ensure_api_key()
            self.config_manager.ensure_access_token()

        # Execute command now
        self.action()


    def _build_commands(self):
        """ Build the Command objects. """

        self.commands = {
            'config'     : ConfigAppCommand,
            'users'      : ShowUsersCommand,
            'notebooks'  : ShowNotebooksCommand,
            'newuser'    : NewUserCommand,
            'notes'      : ShowNotesCommand,
            'newnotebook': NewNotebookCommand
        }

        """
        CMD_DICT = {
            'notebooks'  : show_notebooks,
            'newnote'    : new_note,
        }
        """

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
            self.command(self.args, self)

        except requests.exceptions.ConnectionError:
            msg  = '\nUnable to connect to the cloudCache server.'
            msg += '\nEnsure your server host and port configuration is correct, and that the server is running.'
            print(msg)

        except CommandValidationError as error:
            print('\n{}'.format(error))

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = CloudCacheCliApp(sys.argv)
