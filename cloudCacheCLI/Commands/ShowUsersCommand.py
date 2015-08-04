""" Show the application users. """

import sys

from cloudCacheCLI.Utilities import get_table
from cloudCacheCLI.Commands import BaseCommand

# -------------------------------------------------------------------------------------------------

class ShowUsersCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(ShowUsersCommand, self).__init__(args, parent_app)
        self.url = '{}/users'.format(self.base_url)
        self.action()


    def _validate_and_parse_args(self):
        """ Make sure the passed arguments are relevant to this command, and are also
        acceptably formatted. """

        if len(self.args) > 0:
            print('\nThe users command takes no parameters.')
            sys.exit(0)


    def _on_action_success(self):
        """ Prints the list of users to the console in a formatted table. """
        table_headers = ['ID', 'Username']
        data = [[user['id'], user['username']] for user in self.results['users']]
        print('\n' + get_table(data, headers=table_headers, indent=2))
