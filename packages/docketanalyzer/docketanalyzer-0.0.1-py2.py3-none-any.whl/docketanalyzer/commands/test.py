import click
from docketanalyzer import utils


@click.command()
def test():
    """This is a test."""
    print('This is a test.')


utils.register_command('test', test)

