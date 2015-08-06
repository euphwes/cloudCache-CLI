""" Create a new user. """

from getpass import getpass

from . import CommandValidationError, PostCommand
from cloudCacheCLI import CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES

# ---------------------------------------------------------------------------------------------------------------------

class NewUserCommand(PostCommand):

    def __init__(self, args, parent_app):
        super(NewUserCommand, self).__init__(args, parent_app)
        self.url = '{}/users/'.format(self.base_url)

        self.prompt_password()

        self.body = {
            'username'  : self.username,
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'email'     : self.email,
            'password'  : self.password
        }

        self.action()


    def prompt_password(self):
        """ Prompts the user for password, twice, and compares them to make sure they're the same. If they are, keep
        track of the password so we can use it later when making the API call. If they are not, raise a validation error
        so we stop the process. """

        print('')
        pass1 = getpass()
        pass2 = getpass('Confirm password: ')

        if pass1 != pass2:
            raise CommandValidationError('Passwords do not match!')

        self.password = pass1


    def _validate_and_parse_args(self):
        """ Make sure 4 arguments are passed to this command: username, first name, last name, and email addreess. """

        if len(self.args) != 4:
            msg = 'The new user command takes 4 parameters: username, first name, last name, and email address.'
            raise CommandValidationError(msg)

        self.username   = self.args[0]
        self.first_name = self.args[1]
        self.last_name  = self.args[2]
        self.email      = self.args[3]


    def _on_action_success(self):
        """ Save the newly-created user details to the application config. """

        config = self.app.config_manager.load_config()

        for key in (CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES):
            if key in config:
                del config[key]

        config[CFG_USER] = self.username
        config[CFG_API_KEY] = self.results['api_key']
        self.app.config_manager.save_config(config)