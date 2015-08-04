""" Configure the application. """

from .BaseCommand import BaseCommand

# -------------------------------------------------------------------------------------------------

class ConfigAppCommand(BaseCommand):

    def __init__(self, args, config_file):
        super()


    def action(self):
        """ Configure the application with either the user, the server, or the port. """

        key, val = self.args[0], self.args[1]

        if key not in (CFG_USER, CFG_SERVER, CFG_PORT):
            print('\nThe configuration option "{}"" is not valid.'.format(key))
            print('You may only configure "{}", "{}", or "{}".'.format(CFG_USER, CFG_PORT, CFG_SERVER))
            sys.exit(0)

        config = load_config()
        config[key] = val

        # If we're changing the user, delete any access token and api key since those will be invalid
        if key == CFG_USER:
            for del_key in (CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES):
                if del_key in config:
                    del config[del_key]

        save_config(config)
