import os
from pathlib import Path
import simplejson as json


def register_command(name, item):
    from docketanalyzer import command_registry
    command_registry.register(name, item)


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def get_ucid_components(ucid):
    court = ucid.split(';;')[0]
    docket_number = ucid.split(';;')[1]
    office_number = docket_number.split(':')[0]
    year = docket_number.split(':')[1].split('-')[0]
    return court, docket_number, office_number, year

