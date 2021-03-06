""" Show the notes in the specified notebook. """

from .. import CommandValidationError
from ..BaseCommands import DeleteCommand

# ---------------------------------------------------------------------------------------------------------------------

class DeleteNotebookCommand(DeleteCommand):

    def __init__(self, args, parent_app):
        super(DeleteNotebookCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks/{}'.format(self.base_url, self.notebook_id)
        self.prompt = 'Are you sure you want to delete this notebook? All notes in this notebook will also be deleted.'
        self.action()


    def _validate_and_parse_args(self):
        """ Ensure only 1 argument is passed in, the notebook ID. """

        if len(self.args) != 1:
            raise CommandValidationError('The `deletenotebook` command takes exactly 1 parameter, the notebook ID.')

        self.notebook_id = self.args[0]