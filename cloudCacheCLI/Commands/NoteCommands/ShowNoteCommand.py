""" Show the notes in the specified notebook. """

import arrow

from .. import CommandValidationError
from ..BaseCommands import GetCommand
from cloudCacheCLI.Utilities import get_table

# ---------------------------------------------------------------------------------------------------------------------

class ShowNoteCommand(GetCommand):

    def __init__(self, args, parent_app):
        super(ShowNoteCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks/{}/notes/{}'.format(self.base_url, self.notebook_id, self.note_id)
        self.action()


    def _validate_and_parse_args(self):
        """ Ensure 2 arguments are passed in, the notebook ID and note ID. """

        if len(self.args) != 2:
            message = 'The `note` command takes exactly 2 parameters, the notebook ID and the note ID.'
            raise CommandValidationError(message)

        self.notebook_id = self.args[1]
        self.note_id = self.args[0]


    def _on_action_success(self):
        """ Prints the list of notes to the console in a formatted table. """

        id = self.results['id']
        key = self.results['key']
        val = self.results['value']

        created_on = arrow.get(self.results['created_on']).to('local').format('MM-DD-YY, hh:mm:ss A')
        last_updated = arrow.get(self.results['last_updated']).to('local').format('MM-DD-YY, hh:mm:ss A')

        head = ['ID', 'Note name', 'Note contents', 'Created on', 'Last updated']
        vals = [id, key, val, created_on, last_updated]

        print('\n' + get_table(zip(head, vals), indent=2))
