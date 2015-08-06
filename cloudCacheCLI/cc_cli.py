""" The cloudCache CLI application module. """

import sys
from os.path import dirname, realpath, join

from requests.exceptions import ConnectionError

from ConfigManager import ConfigManager
from Commands import CommandValidationError, ConfigAppCommand
from Commands.UserCommands import NewUserCommand, ShowUsersCommand, DeleteUserCommand
from Commands.NotebookCommands import DeleteNotebookCommand, NewNotebookCommand, ShowNotebooksCommand
from Commands.NoteCommands import DeleteNoteCommand, ShowNotesCommand, NewNoteCommand, ShowNoteCommand

# -------------------------------------------------------------------------------------------------

class CloudCacheCliApp(object):

    commands = {
        'config': ConfigAppCommand,
        'users': ShowUsersCommand,
        'notebooks': ShowNotebooksCommand,
        'newuser': NewUserCommand,
        'notes': ShowNotesCommand,
        'newnotebook': NewNotebookCommand,
        'newnote': NewNoteCommand,
        'note': ShowNoteCommand,
        'deletenote': DeleteNoteCommand,
        'deletenotebook': DeleteNotebookCommand,
        'deleteuser': DeleteUserCommand
    }

    def __init__(self, args):
        # discard the first argument, which is the script name
        self.args = args[1:]
        self.config_manager = ConfigManager(join(dirname(realpath(__file__)), '.ccconfig'))

        # If no arguments are provided, just echo the current configuration and exit the script
        if len(self.args) == 0:
            self.config_manager.echo_config()
            sys.exit(0)

        try:
            user_command = self.args.pop(0)
            self.command = self.commands[user_command]
        except KeyError:
            print('\n`{}` is not a valid cloudCache command.'.format(user_command))
            return
            # TODO display help

        should_skip_ensure_steps = (self.command is ConfigAppCommand or self.command is NewUserCommand)
        if not should_skip_ensure_steps:
            # Before executing any command other than config or newuser, ensure a user is configured, ensure we have a
            # valid API key, and also an access token so we can be making API calls.
            self.config_manager.ensure_user()
            self.config_manager.ensure_api_key()
            self.config_manager.ensure_access_token()

        # Execute command now
        self.action()


    def action(self):
        """ Perform the selected command action. """
        try:
            self.command(self.args, self)

        except ConnectionError:
            msg  = '\nUnable to connect to the cloudCache server.'
            msg += '\nEnsure your server host and port configuration is correct, and that the server is running.'
            print(msg)

        except CommandValidationError as error:
            print('\n{}'.format(error))

# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app = CloudCacheCliApp(sys.argv)
