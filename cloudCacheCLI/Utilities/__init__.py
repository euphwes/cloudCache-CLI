
import tabulate

def get_table(data, headers=(), indent=0, table_format='fancy_grid'):
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

    table  = tabulate.tabulate(data, headers=headers, numalign='left', tablefmt=table_format)
    indent = ' ' * indent

    return '\n'.join(indent + line for line in table.split('\n'))