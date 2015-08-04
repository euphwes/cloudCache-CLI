""" Configure the application. """

import sys

from cloudCacheCLI.Commands import BaseCommand
from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES

# -------------------------------------------------------------------------------------------------

class ConfigAppCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(ConfigAppCommand, self).__init__(args, parent_app)


    def _validate_args(self):
        """ Make sure the passed arguments are relevant to this command, and are also
        acceptably formatted. """

        if len(self.args) > 2:
            print('\nThe config command only takes 2 parameters.')
            sys.exit(0)

        self.key, self.val = self.args[0], self.args[1]

        if self.key not in (CFG_USER, CFG_SERVER, CFG_PORT):
            print('\nThe configuration option "{}"" is not valid.'.format(self.key))
            print('You may only configure "{}", "{}", or "{}".'.format(CFG_USER, CFG_PORT, CFG_SERVER))
            sys.exit(0)


    def action(self):
        """ Configure the application with either the user, the server, or the port. """

        config = self.app.config_manager.load_config()
        config[self.key] = self.val

        # If we're changing the user, delete any access token and api key since those will be invalid
        if self.key == CFG_USER:
            for del_key in (CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES):
                if del_key in config:
                    del config[del_key]

        self.app.config_manager.save_config(config)
        self.app.config_manager.ensure_user()
        self.app.config_manager.ensure_api_key()
        self.app.config_manager.ensure_access_token()
