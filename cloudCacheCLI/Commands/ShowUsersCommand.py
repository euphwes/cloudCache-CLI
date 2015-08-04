""" Show the application users. """

import requests, json, sys

from cloudCacheCLI.Commands import BaseCommand
from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES

# -------------------------------------------------------------------------------------------------

class ShowUsersCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(ShowUsersCommand, self).__init__(args, parent_app)


    @property
    def url(self):
        """ Any subclass must implement this property. Return the API endpoint URL which this
        command uses, based on args and configuration. """
        return '{}/users'.format(self.base_url)


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

        if response.status_code == 200:
            headers = ['ID', 'Username']
            data = [[user['id'], user['username']] for user in results['users']]
            print('\n' + self.get_table(data, headers=headers, indent=2))

        else:
            print('\n** {} **'.format(results['message']))
