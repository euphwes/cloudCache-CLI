""" Show the user notebooks. """

import json
import sys

import requests

from cloudCacheCLI.Commands import BaseCommand
from cloudCacheCLI.Utilities import get_table

# -------------------------------------------------------------------------------------------------

class ShowNotebooksCommand(BaseCommand):

    def __init__(self, args, parent_app):
        super(ShowNotebooksCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks'.format(self.base_url)


    def _validate_args(self):
        """ Make sure the passed arguments are relevant to this command, and are also
        acceptably formatted. """

        if len(self.args) > 0:
            print('\nThe notebooks command takes no parameters.')
            sys.exit(0)


    def action(self):
        """ Show all notebooks for this user. """

        response = requests.get(self.url, headers=self.headers)
        results  = json.loads(response.text)

        if response:
            if len(results['notebooks']) == 0:
                print('\n' + get_table([['No notebooks exist for this user']], indent=2))
            else:
                headers = ['ID', 'Notebook Name']
                data = [[nb['id'], nb['name']] for nb in results['notebooks']]
                print('\n' + get_table(data, headers=headers, indent=2))

        else:
            print('\n** {} **'.format(results['message']))
