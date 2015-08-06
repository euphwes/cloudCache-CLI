
class CommandValidationError(Exception):
    """ An exception which is raised when a Command object fails validation. Probably due to invalid arguments. """
    pass

from .ConfigAppCommand import ConfigAppCommand