import click
from docketanalyzer import utils
from docketanalyzer.registry import BaseRegistry, command_registry
from docketanalyzer import commands


@click.group()
def cli():
    pass


for name, command in command_registry._registry.items():
    cli.add_command(command, name)

