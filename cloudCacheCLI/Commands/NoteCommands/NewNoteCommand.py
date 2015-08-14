""" Create a new Note in a notebook. """

from .. import CommandValidationError
from ..BaseCommands import PutCommand

# ---------------------------------------------------------------------------------------------------------------------

class NewNoteCommand(PutCommand):

    def __init__(self, args, parent_app):
        super(NewNoteCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks/{}/notes'.format(self.base_url, self.notebook_id)
        self.body = {
            'note_key'  : self.note_key,
            'note_value': self.note_value
        }
        self.action()


    def _validate_and_parse_args(self):
        """ Make sure 1 argument is passed to this command: notebook name. """

        if len(self.args) != 3:
            msg = 'The new note command takes exactly 3 parameter: the notebook ID, the note key, and the note value.'
            raise CommandValidationError(msg)

        self.notebook_id = self.args[0]
        self.note_key = self.args[1]
        self.note_value = self.args[2]
