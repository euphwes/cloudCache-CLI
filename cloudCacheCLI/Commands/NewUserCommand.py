""" Create a new user. """

import requests, json, sys

from cloudCacheCLI.Commands import BaseCommand
from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES

# -------------------------------------------------------------------------------------------------

class NewUserCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(NewUserCommand, self).__init__(args, parent_app)
        self.url = '{}/users/'.format(self.base_url)


    def _validate_args(self):
        """ Make sure the passed arguments are relevant to this command, and are also
        acceptably formatted. """

        if len(self.args) != 4:
            print('\nThe new user command takes 4 parameters: username, first name, last name, and email address.')
            sys.exit(0)

        self.username   = self.args[0]
        self.first_name = self.args[1]
        self.last_name  = self.args[2]
        self.email      = self.args[3]


    def action(self):
        """ Create a new user, and save the relevant details to the config. """

        body = {
            'username'  : self.username,
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'email'     : self.email
        }

        response = requests.post(self.url, data=json.dumps(body))
        results  = json.loads(response.text)

        if response:
            config = self.parent_app.load_config()
            if CFG_ACCESS_TOKEN in config:
                del config[CFG_ACCESS_TOKEN]
            config[CFG_USER]    = self.username
            config[CFG_API_KEY] = results['api_key']
            self.parent_app.save_config(config)

        else:
            print('\n** {} **'.format(results['message']))
