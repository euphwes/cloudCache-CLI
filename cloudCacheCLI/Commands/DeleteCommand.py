""" The base command class which all other commands subclass. """

import requests

from . import BaseCommand
from distutils.util import strtobool

# -------------------------------------------------------------------------------------------------

class DeleteCommand(BaseCommand):
    """ The base command class for a command which makes an HTTP DELETE call. """

    def __init__(self, args, parent_app):
        """ Any subclass must create a self.url attribute so the action() call may evaluate successfully. """
        super(DeleteCommand, self).__init__(args, parent_app)


    def action(self):
        """ Evaluates this Command by performing its API call. The response object itself, and the json/dict contents
        of the response, are set as instance attributes so we can reference them later. """

        prompt = '\n{}\nEnter `yes` or `no` (or `y` or `n`): '.format(self.prompt)
        user_confirmation = bool(strtobool(input(prompt)))

        if user_confirmation:
            self.response = requests.delete(self.url, headers=self.headers)
            super(DeleteCommand, self).action()


    def _on_action_success(self):
        """ OVERRIDE - Do nothing, the delete action was successful. """
        print('\nSuccessfully deleted.')