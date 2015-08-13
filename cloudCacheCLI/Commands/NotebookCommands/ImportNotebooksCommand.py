""" Show the user notebooks. """

from .. import CommandValidationError
from .NewNotebookCommand import NewNotebookCommand
from cloudCacheCLI.Utilities import get_table
import json

# --------------------------------------------------------------------------------------------------------------------

class ImportNotebooksCommand(object):

    def __init__(self, args, parent_app):
        self.args = args
        self.parent_app = parent_app
        self._validate_and_parse_args()
        self.action()


    def _validate_and_parse_args(self):
        """ Since the 'notebooks' command is argument-free, make sure no arguments were passed in. """
        if len(self.args) != 1:
            message = 'The `importnotebooks` command takes exactly 1 parameter: the target input file'
            raise CommandValidationError(message)

        self.input_file = self.args[0]


    def action(self):

        with open(self.input_file) as input_file:
            dict_from_file = json.load(input_file)

        for nb in dict_from_file['notebooks']:
            new_nb_cmd = NewNotebookCommand([nb['name']], self.parent_app)
            print(new_nb_cmd.results['notebook_id'])