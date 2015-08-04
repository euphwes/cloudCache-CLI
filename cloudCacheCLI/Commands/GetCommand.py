""" The base command class which all other commands subclass. """

import requests
from . import BaseCommand

# -------------------------------------------------------------------------------------------------

class GetCommand(BaseCommand):
    """ The base command class for a command which makes an HTTP GET call. """

    def __init__(self, args, parent_app):
        """ Any subclass must create a self.url attribute so the action() call may evaluate successfully. """
        super(GetCommand, self).__init__(args, parent_app)


    def action(self):
        """ Evaluates this Command by performing its API call. The response object itself, and the json/dict contents
        of the response, are set as instance attributes so we can reference them later. """
        self.response = requests.get(self.url, headers=self.headers)
        super(GetCommand, self).action()