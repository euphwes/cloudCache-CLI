""" The base command class which all other commands subclass. """

import json

import requests

from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_ACCESS_TOKEN

# -------------------------------------------------------------------------------------------------

class BaseCommand(object):
    """ The base command class. """

    def __init__(self, args, parent_app):
        """ Any subclass must create a self.url attribute so the action() call may evaluate successfully. This is not
        necessary if the subclass overrides action() and doesn't need to make a web request. """
        self.args = args
        self.app = parent_app
        self._validate_and_parse_args()

        config = self.app.config_manager.load_config()
        self.headers = {'access token': config[CFG_ACCESS_TOKEN]}
        self.base_url = 'http://{}:{}'.format(config[CFG_SERVER], config[CFG_PORT])


    def action(self):
        """ Evaluates this Command by performing its API call. The response object itself, and the json/dict contents
        of the response, are set as instance attributes so we can reference them later. """
        self.response = requests.get(self.url, headers=self.headers)
        self.results = json.loads(self.response.text)

        # requests.response with a status_code of 200 evaluates as 'True' if checked as a bool
        self._on_action_success() if self.response else self._on_action_failure()


    def _on_action_failure(self):
        """ May be overridden. Defaults to just printing out the error message returned by the response. """
        print('')
        print(self.results['message'])


    def _validate_and_parse_args(self):
        """ Any subclasses must implement this method. Validate the args passed into the constructor and verify they
        are appropriate for this command, and complete. """
        raise NotImplementedError()


    def _on_action_success(self):
        """ Any subclasses must implement this method. Perform any actions which depend on the Command success. """
        raise NotImplementedError()