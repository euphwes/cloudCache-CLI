""" Show the user notebooks. """

import sys

from . import CommandValidationError, GetCommand
from cloudCacheCLI.Utilities import get_table

# --------------------------------------------------------------------------------------------------------------------

class ShowNotebooksCommand(GetCommand):

    def __init__(self, args, parent_app):
        super(ShowNotebooksCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks'.format(self.base_url)
        self.action()


    def _validate_and_parse_args(self):
        """ Since the 'notebooks' command is argument-free, make sure no arguments were passed in. """
        if len(self.args) > 0:
            raise CommandValidationError('The `notebooks` command takes no parameters.')


    def _on_action_success(self):
        """ Prints the list of the current user's notebooks to the console in a formatted table. """

        if len(self.results['notebooks']) == 0:
            print('\n' + get_table([['No notebooks exist for this user']], indent=2))

        else:
            table_headers = ['ID', 'Notebook Name']
            data = [[nb['id'], nb['name']] for nb in self.results['notebooks']]
            print('\n' + get_table(data, headers=table_headers, indent=2))