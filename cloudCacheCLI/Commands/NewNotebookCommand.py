""" Create a new Notebook. """

import json

import requests

from . import CommandValidationError, BaseCommand
from cloudCacheCLI import CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES

# ---------------------------------------------------------------------------------------------------------------------

class NewNotebookCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(NewNotebookCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks'.format(self.base_url)
        self.action()


    def _validate_and_parse_args(self):
        """ Make sure 1 argument is passed to this command: notebook name. """

        if len(self.args) != 1:
            msg = 'The new notebook command takes exactly 1 parameter: the notebook name.'
            raise CommandValidationError(msg)

        self.notebook_name = self.args[0]


    def _on_action_success(self):
        """ OVERRIDE - Do nothing, the notebook was created successfully. """
        pass


    def action(self):
        """ OVERRIDE - Create a new notebook. """

        body = {'notebook_name': self.notebook_name}
        self.response = requests.post(self.url, headers=self.headers, data=json.dumps(body))
        self.results = json.loads(self.response.text)

        self._on_action_success() if self.response else self._on_action_failure()