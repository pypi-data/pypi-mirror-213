from .utilities.request_handler import Request
from .utilities import config
from . import exceptions
import uuid


class SlackMessage:

    def __init__(self, token, channel, text, data):
        self.id = str(uuid.uuid4())[:13].replace('-', '')
        self._token = token
        self._ts = data['ts']
        self._channel = data['channel']
        self._deleted = False
        self._request = Request(self._token)

        self.channel = channel
        self.text = text

    def __srt__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'

    def update(self, text=''):
        """Updates the message.

        Args:
            text (string): New text. Old one will be replaced.

        Returns:
            None
        """
        self._request.post(
            url='update_message',
            data={'channel': self._channel, 'ts': self._ts, 'text': text},
            exception=exceptions.MessageNotUpdated
        )
        self.text = text

    def delete(self):
        """Deletes the message.

        Returns:
            None
        """
        if self._deleted:
            raise exceptions.MessageAlreadyDeleted

        self._request.post(
            url='delete_message',
            data={'channel': self._channel, 'ts': self._ts},
            exception=exceptions.MessageNotDeleted
        )
        self._deleted = True


class Message(SlackMessage):

    def __init__(self, token, channel, text, data):
        super().__init__(token, channel, text, data)
        self._replies = []

    def send_reply(self, text=''):
        """Sends reply in the message thread.

        Args:
            text (string): Text to be sent.

        Returns:
            Object: <Reply>

        """
        self._request.post(
            url='post_message',
            data={
                'icon_url': config.data['default_icon'],
                'channel': self.channel,
                'thread_ts': self._ts,
                'text': text
            },
            exception=exceptions.MessageNotSend
        )
        reply = Reply(self._token, self.channel, text, self._request.response)
        self._replies.append(reply)
        return reply

    def get_replies(self):
        """Lists all sent replies to the message thread.

        Returns:
            List: Reply objects
        """
        return self._replies[:]


class Reply(SlackMessage):
    pass
