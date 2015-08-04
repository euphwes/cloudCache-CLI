""" The base command class which all other commands subclass. """

import sys, json, requests, arrow, tabulate
from cloudCacheCLI import CFG_SERVER, CFG_PORT, CFG_USER, CFG_API_KEY, CFG_ACCESS_TOKEN, CFG_TOKEN_EXPIRES

# -------------------------------------------------------------------------------------------------

class BaseCommand(object):
    """ The base command class. """

    def __init__(self, args, parent_app):
        self.args = args
        self.parent_app = parent_app
        self._validate_args()

        config = self.parent_app.load_config()
        self.headers = {'access token': config[CFG_ACCESS_TOKEN]}


    def _validate_args(self):
        """ Any subclasses must implement this method. Validate the args passed into the
        constructor and verify they are appropriate for this command, and complete. """
        raise NotImplementedError()


    @property
    def base_url(self):
        """ Build and return the base URL for the API endpoints. """
        config = self.parent_app.load_config()
        return 'http://{}:{}'.format(config[CFG_SERVER], config[CFG_PORT])


    def get_table(self, data, headers=[], indent=0, table_format='fancy_grid'):
        """ Get an ascii table string for a given set of values (list of lists), and column headers.
        Optional indentation. Defer to tabulate.tabulate for most of the work. This is mostly a
        convenience function for indenting a table.

        Args:
            data: Any data which can be fed to tabulate, nominally list of lists.
            headers (list of string): A list of values to be used as column headers
            indent (int): The number of spaces to indent table by. Defaults to 0 (no indentation).
            table_format (string): The tablefmt argument of tabulate.tabulate. Defaults to fancy_grid.

        Returns:
            string: The formatted table of data
        """

        table  = tabulate.tabulate(data, headers=headers, tablefmt=table_format)
        indent = ' ' * indent

        return '\n'.join(indent + line for line in table.split('\n'))
