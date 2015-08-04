""" Create a new Notebook. """

from . import CommandValidationError, PostCommand

# ---------------------------------------------------------------------------------------------------------------------

class NewNotebookCommand(PostCommand):

    def __init__(self, args, parent_app):
        super(NewNotebookCommand, self).__init__(args, parent_app)
        self.url = '{}/notebooks'.format(self.base_url)
        self.body = {'notebook_name': self.notebook_name}
        self.action()


    def _validate_and_parse_args(self):
        """ Make sure 1 argument is passed to this command: notebook name. """

        if len(self.args) != 1:
            msg = 'The new notebook command takes exactly 1 parameter: the notebook name.'
            raise CommandValidationError(msg)

        self.notebook_name = self.args[0]