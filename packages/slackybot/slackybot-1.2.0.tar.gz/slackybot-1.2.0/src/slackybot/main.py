from .messaging import Message
from .utilities.request_handler import Request
from .utilities.common import config
from . import exceptions
from time import time


class Slack:

    def __init__(self, token='', default_channel=''):
        if not token:
            raise exceptions.SlackInitializeError('Missing token')
        self._token = token
        self._messages = []
        self._default_channel = default_channel
        self._request = Request(self._token)

    def send_message(self, channel='', text=''):
        """Sends simple text message.

        Args:
            channel (string): Channel name.
            text (string): Text to be sent.

        Returns:
            Object: <Message>
        """

        self._request.post(
            url='post_message',
            data={
                'icon_url': config.data['default_icon'],
                'channel': channel if channel else self._default_channel,
                'text': text
            },
            exception=exceptions.MessageNotSend
        )
        slack_message = Message(self._token, channel, text, self._request.response)
        self._messages.append(slack_message)
        return slack_message

    def send_alert(self, channel='', title='Alert!', type='', values: dict = {}, mentions: tuple = ()):
        """Sends the alert message

        Args:
            channel (str, optional): Specify the channel where the alert has to be sent.
            title (str, optional): The alert title. Defaults to 'Alert!'.
            type (str, optional): One of the following types: "success", "warning", "fail".
            values (dict, optional): Fields in the alert message.
            mentions (tuple, optional): Slack nicknames.

        Returns:
            Object: <Message>
        """
        if type.lower() not in ['success', 'fail', 'warning']:
            raise exceptions.WrongAlertType
        self._request.post(
            url='post_message',
            data={
                'channel': channel if channel else self._default_channel,
                'icon_url': config.data['default_icon'],
                'attachments': [
                    {
                        'mrkdwn_in': ['text'],
                        'color': config.data['alert']['colors'].get(type, '#737373'),
                        'title': f"{config.data['alert']['icons'].get(type, ':black_circle:')} {title}",
                        'fields': [
                            {
                                'title': '',
                                'value': '',
                                'short': False
                            },
                            {
                                'title': '',
                                'value': '\n'.join([f'*{key}:* {value}' for key, value in values.items()]),
                                'short': False
                            },
                            {
                                'title': ':mega: Mentions' if mentions else '',
                                'value': ', '.join([f'<@{mention}>' for mention in mentions]) if mentions else '',
                                'short': False
                            },
                        ],
                        'footer': 'Alert',
                        'ts': time()
                    }
                ]
            },
            exception=exceptions.MessageNotSend
        )
        slack_message = Message(self._token, channel, '', self._request.response)
        self._messages.append(slack_message)
        return slack_message

    def get_messages(self):
        """Lists all sent messages.

        Returns:
            List: Message objects
        """
        return self._messages[:]
