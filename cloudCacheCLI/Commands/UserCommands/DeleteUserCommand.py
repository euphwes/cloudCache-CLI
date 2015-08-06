""" Show the notes in the specified notebook. """

from distutils.util import strtobool
import json
from getpass import getpass

import requests

from ..BaseCommands import DeleteCommand
from .. import CommandValidationError

# ---------------------------------------------------------------------------------------------------------------------

class DeleteUserCommand(DeleteCommand):

    def __init__(self, args, parent_app):
        super(DeleteUserCommand, self).__init__(args, parent_app)
        self.url = '{}/users/{}'.format(self.base_url, self.username)
        self.prompt = 'Are you sure you want to delete this user? All their notebooks and notes will be lost.'
        self.action()


    def action(self):
        """ Evaluates this Command by performing its API call. The response object itself, and the json/dict contents
        of the response, are set as instance attributes so we can reference them later. """

        prompt = '\n{}\nEnter `yes` or `no` (or `y` or `n`): '.format(self.prompt)
        user_confirmation = bool(strtobool(input(prompt)))

        if user_confirmation:
            body = {'password' :getpass('\nPassword: ')}
            self.response = requests.delete(self.url, headers=self.headers, data=json.dumps(body))
            super(DeleteCommand, self).action()


    def _validate_and_parse_args(self):
        """ Ensure only 1 argument is passed in, the username. """

        if len(self.args) != 1:
            raise CommandValidationError('The `deleteuser` command takes exactly 1 parameter, the username.')

        self.username = self.args[0]