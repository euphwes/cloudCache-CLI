""" Show the application users. """

import json
import sys

import requests

from cloudCacheCLI.Utilities import get_table
from cloudCacheCLI.Commands import BaseCommand


# -------------------------------------------------------------------------------------------------

class ShowUsersCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(ShowUsersCommand, self).__init__(args, parent_app)
        self.url = '{}/users'.format(self.base_url)


    def _validate_args(self):
        """ Make sure the passed arguments are relevant to this command, and are also
        acceptably formatted. """

        if len(self.args) > 0:
            print('\nThe users command takes no parameters.')
            sys.exit(0)


    def action(self):
        """ Show all users. """

        response = requests.get(self.url, headers=self.headers)
        results  = json.loads(response.text)

        if response:
            headers = ['ID', 'Username']
            data = [[user['id'], user['username']] for user in results['users']]
            print('\n' + get_table(data, headers=headers, indent=2))

        else:
            print('\n** {} **'.format(results['message']))
