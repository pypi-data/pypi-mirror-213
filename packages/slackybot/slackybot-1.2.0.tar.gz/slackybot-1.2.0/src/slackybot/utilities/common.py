from .. import exceptions
from . import config


def get_exception(output_data):
    return config.data['error_exceptions'].get(output_data['error'], exceptions.Unknown(output_data['error']))
