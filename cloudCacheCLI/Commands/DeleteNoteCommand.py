""" Show the notes in the specified notebook. """

from . import CommandValidationError, DeleteCommand

# ---------------------------------------------------------------------------------------------------------------------

class DeleteNoteCommand(DeleteCommand):

    def __init__(self, args, parent_app):
        super(DeleteNoteCommand, self).__init__(args, parent_app)
        self.url = '{}/notes/{}'.format(self.base_url, self.note_id)
        self.action()


    def _validate_and_parse_args(self):
        """ Ensure only 1 argument is passed in, the notebook ID. """

        if len(self.args) != 1:
            raise CommandValidationError('The `deletenote` command takes exactly 1 parameter, the note ID.')

        self.note_id = self.args[0]