""" Configure the application. """

from . import CommandValidationError, BaseCommand
from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES

# --------------------------------------------------------------------------------------------------------------------

class ConfigAppCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(ConfigAppCommand, self).__init__(args, parent_app)
        self.action()


    def _validate_and_parse_args(self):
        """ Make sure the passed arguments are relevant to this command, and are also
        acceptably formatted. """

        if len(self.args) != 2:
            msg  = 'The config command takes exactly 2 parameters.\n'
            msg += 'The first argument must be one of [server, port, user].\n'
            msg += 'The second argument must be the value that configuration option is to take.'
            raise CommandValidationError(msg)

        self.key, self.val = self.args[0], self.args[1]

        if self.key not in (CFG_USER, CFG_SERVER, CFG_PORT):
            msg  = 'The configuration option `{}` is not valid.\n'.format(self.key)
            msg += 'You may only configure `{}`, `{}`, or `{}`.'.format(CFG_USER, CFG_PORT, CFG_SERVER)
            raise CommandValidationError(msg)


    def _change_port_or_server(self):
        """ Change port or server in the configuration file. """
        config = self.app.config_manager.load_config()
        config[self.key] = self.val


    def _change_user(self):
        """ Attempt to change user in the configuration file. If the change fails (invalid username or password, or
         some other reason, fall back to the original user-related details in the config. """

        config_orig = self.app.config_manager.load_config()
        config_copy = self.app.config_manager.load_config()

        # Update the actual value for the selected key
        config_copy[self.key] = self.val

        # Delete any access token and api key since those will be invalid
        for del_key in (CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES):
            if del_key in config_copy:
                del config_copy[del_key]

        # Save the configuration with the new value. Re-check user, API key, and access token, since those were
        # potentially lost if the caller configured a new user
        try:
            self.app.config_manager.save_config(config_copy)
            self.app.config_manager.ensure_user()
            self.app.config_manager.ensure_api_key()
            self.app.config_manager.ensure_access_token()

        except Exception:
            print('\nUser change failed. Reverting back to original settings.')
            self.app.config_manager.save_config(config_orig)


    def action(self):
        """ OVERRIDE - Configure the application with a new value for either the user, the server, or the port. """
        self._change_user() if (self.key == CFG_USER) else self._change_port_or_server()