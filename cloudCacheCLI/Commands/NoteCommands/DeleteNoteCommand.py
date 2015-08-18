""" Show the notes in the specified notebook. """

from .. import CommandValidationError
from ..BaseCommands import DeleteCommand

# ---------------------------------------------------------------------------------------------------------------------

class DeleteNoteCommand(DeleteCommand):

    def __init__(self, args, parent_app):
        super(DeleteNoteCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks/{}/notes/{}'.format(self.base_url, self.notebook_id, self.note_id)
        self.prompt = 'Are you sure you want to delete this note? This action is irreversible.'
        self.action()


    def _validate_and_parse_args(self):
        """ Ensure only 1 argument is passed in, the notebook ID. """

        if len(self.args) != 2:
            message = 'The `deletenote` command takes exactly 2 parameters, the notebook ID and the note ID.'
            raise CommandValidationError(message)

        self.notebook_id = self.args[0]
        self.note_id = self.args[1]