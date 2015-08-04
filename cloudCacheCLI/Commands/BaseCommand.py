""" The base command class which all other commands subclass. """

import sys, json, requests, arrow
from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES

# -------------------------------------------------------------------------------------------------

class BaseCommand(object):
    """ The base command class. """

    def __init__(self, args, parent_app):
        self.args = args
        self.parent_app = parent_app
        self._validate_args()


    def _validate_args(self):
        """ Any subclasses must implement this method. Validate the args passed into the
        constructor and verify they are appropriate for this command, and complete. """
        raise NotImplementedError()


    @property
    def url(self):
        """ Any subclass must implement this property. Return the API endpoint URL which this
        command uses, based on args and configuration. """
        raise NotImplementedError()


    @property
    def base_url(self):
        """ Build and return the base URL for the API endpoints. """
        config = self.parent_app.load_config()
        return 'http://{}:{}'.format(config[CFG_SERVER], config[CFG_PORT])
