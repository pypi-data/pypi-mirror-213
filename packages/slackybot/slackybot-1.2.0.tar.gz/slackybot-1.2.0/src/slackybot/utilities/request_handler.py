from . import common, config
import requests
import json


class Request:

    def __init__(self, token):
        self.response = {}
        self._token = None
        self._headers = {'Authorization': f'Bearer {token}'}

    def post(self, url, data={}, exception=None):
        """Sends the POST request

        Args:
            url (str): A key of the url in the config file.
            data (dict, optional): The request JSON payload. Defaults to {}.
            exception (exception): An exception - it is raised in case of request sending failure.
        """
        try:
            response = requests.post(
                config.data['urls'][url],
                json=data,
                headers=self._headers,
            ).json()
            if response['ok']:
                self.response = response
            else:
                raise common.get_exception(response)
        except KeyError as exp:
            raise Exception(f'Given url does not exist: {exp}')
        except (requests.ConnectionError, json.JSONDecodeError, requests.ConnectTimeout):
            raise exception if exception else Exception('Unknown error while sending request. Exception not provided.')
