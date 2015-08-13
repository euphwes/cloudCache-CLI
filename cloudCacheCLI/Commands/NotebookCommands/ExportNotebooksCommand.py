""" Show the user notebooks. """

from .. import CommandValidationError
from ..BaseCommands import GetCommand
from cloudCacheCLI.Utilities import get_table
import json

# --------------------------------------------------------------------------------------------------------------------

class ExportNotebooksCommand(GetCommand):

    def __init__(self, args, parent_app):
        super(ExportNotebooksCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks'.format(self.base_url)
        self.action()


    def _validate_and_parse_args(self):
        """ Since the 'notebooks' command is argument-free, make sure no arguments were passed in. """
        if len(self.args) != 1:
            message = 'The `exportnotebooks` command takes exactly 1 parameter: the target output file'
            raise CommandValidationError(message)

        self.output_file = self.args[0]


    def _on_action_success(self):
        """ Prints the list of the current user's notebooks to the console in a formatted table. """

        if len(self.results['notebooks']) == 0:
            print('\n' + get_table([['No notebooks exist for this user']], indent=2))

        else:
            with open(self.output_file, 'w') as output_file:
                json.dump(self.results, output_file, indent=4, separators=(',', ': '))