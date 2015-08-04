""" The base command class which all other commands subclass. """

from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_ACCESS_TOKEN

# -------------------------------------------------------------------------------------------------

class BaseCommand(object):
    """ The base command class. """

    def __init__(self, args, parent_app):
        self.args = args
        self.app = parent_app
        self._validate_args()

        config = self.app.config_manager.load_config()
        self.headers = {'access token': config[CFG_ACCESS_TOKEN]}


    def _validate_args(self):
        """ Any subclasses must implement this method. Validate the args passed into the
        constructor and verify they are appropriate for this command, and complete. """
        raise NotImplementedError()


    @property
    def base_url(self):
        """ Build and return the base URL for the API endpoints. """
        config = self.app.config_manager.load_config()
        return 'http://{}:{}'.format(config[CFG_SERVER], config[CFG_PORT])
