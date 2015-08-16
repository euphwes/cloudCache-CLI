""" The base command class which all other commands subclass. """

import json
import requests

from . import BaseCommand

# -------------------------------------------------------------------------------------------------

class PutCommand(BaseCommand):
    """ The base command class for a command which makes an HTTP PUT call. """

    def __init__(self, args, parent_app):
        """ Any subclass must create a self.url attribute so the action() call may evaluate successfully. They must
        also create a self.body attribute (dictionary) which is dumped to JSON for the body of the PUT. """
        super(PutCommand, self).__init__(args, parent_app)


    def action(self):
        """ Evaluates this Command by performing its API call. The response object itself, and the json/dict contents
        of the response, are set as instance attributes so we can reference them later. """

        kwargs = {'data': json.dumps(self.body)}
        if hasattr(self, 'headers'):
            kwargs['headers'] = self.headers

        self.response = requests.put(self.url, **kwargs)
        self.results  = json.loads(self.response.text)
        super(PutCommand, self).action()


    def _on_action_success(self):
        """ OVERRIDE - Do nothing, the PUT action was successful. """
        pass