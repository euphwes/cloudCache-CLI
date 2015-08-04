""" Show the notes in the specified notebook. """

from . import CommandValidationError, GetCommand
from cloudCacheCLI.Utilities import get_table

# ---------------------------------------------------------------------------------------------------------------------

class ShowNotesCommand(GetCommand):

    def __init__(self, args, parent_app):
        super(ShowNotesCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks/{}/notes/'.format(self.base_url, self.notebook_id)
        self.action()


    def _validate_and_parse_args(self):
        """ Ensure only 1 argument is passed in, the notebook ID. """

        if len(self.args) != 1:
            raise CommandValidationError('The `notes` command takes exactly 1 parameter, the notebook ID.')

        self.notebook_id = self.args[0]


    def _on_action_success(self):
        """ Prints the list of notes to the console in a formatted table. """

        notes = self.results['notes']
        notebook = self.results['notebook']

        if len(notes) == 0:
            print('\n' + get_table([['This notebook does not have any notes yet.']], indent=2))
        else:
            print('\n' + get_table([[notebook]], indent=2))
            data = [[note['key'], note['value']] for note in notes]
            table_headers = ['Note name', 'Note contents']
            print(get_table(data, headers=table_headers, indent=6))
