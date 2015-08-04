""" Show the application users. """

from . import CommandValidationError
from cloudCacheCLI.Utilities import get_table
from cloudCacheCLI.Commands import BaseCommand

# ---------------------------------------------------------------------------------------------------------------------

class ShowUsersCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(ShowUsersCommand, self).__init__(args, parent_app)
        self.url = '{}/users'.format(self.base_url)
        self.action()


    def _validate_and_parse_args(self):
        """ As the 'users' command is argument-free, make sure no arguments were passed in. """

        if len(self.args) > 0:
            raise CommandValidationError('The `users` command takes no parameters.')


    def _on_action_success(self):
        """ Prints the list of users to the console in a formatted table. """

        table_headers = ['ID', 'Username']
        data = [[user['id'], user['username']] for user in self.results['users']]
        print('\n' + get_table(data, headers=table_headers, indent=2))
