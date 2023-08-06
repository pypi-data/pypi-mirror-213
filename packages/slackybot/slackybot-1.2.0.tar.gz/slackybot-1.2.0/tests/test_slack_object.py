from src.slackybot import Slack
from src.slackybot import exceptions

from dotenv import load_dotenv
import uuid
import pytest
import os

load_dotenv()


def test_initialize_slack_object():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    assert slack


def test_initialize_slack_object_without_token():
    with pytest.raises(exceptions.SlackInitializeError):
        slack = Slack()
        slack.send_message(channel='tests', text='Unit test message')


def test_send_message():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    slack.send_message(channel='tests', text='Unit test message')
    assert slack.get_messages()


def test_send_message_wrong_channel():
    with pytest.raises(exceptions.ChannelNotFound):
        slack = Slack(token=os.getenv('SLACK_TOKEN'))
        slack.send_message(channel=str(uuid.uuid4()), text='Unit test message')


def test_send_message_missing_channel():
    with pytest.raises(exceptions.ChannelNotFound):
        slack = Slack(token=os.getenv('SLACK_TOKEN'))
        slack.send_message(text='Unit test message')


def test_send_message_with_default_channel():
    slack = Slack(token=os.getenv('SLACK_TOKEN'), default_channel='tests')
    slack.send_message(text='Unit test message default channel')


def test_send_message_empty_text():
    with pytest.raises(exceptions.MissingText):
        slack = Slack(token=os.getenv('SLACK_TOKEN'))
        slack.send_message(channel='tests')


def test_send_alert_success():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    slack.send_alert(
        channel='tests',
        title='The alert title',
        type='success',
        values={
            'Field one': '`OK`',
            'Field two': 123456789,
            'Field three': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        },
        mentions=('michalm138',)
    )


def test_send_alert_wrong_type():
    with pytest.raises(exceptions.WrongAlertType):
        slack = Slack(token=os.getenv('SLACK_TOKEN'))
        slack.send_alert(
            channel='tests',
            title='The alert title',
            type='wrong_type',
            values={
                'Field one': '`OK`',
                'Field two': 123456789,
                'Field three': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
            }
        )


def test_delete_alert():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    msg = slack.send_alert(
        channel='tests',
        title='The alert title',
        type='warning',
        values={
            'Field one': '`OK`',
            'Field two': 123456789,
            'Field three': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        }
    )
    msg.delete()


def test_send_alert_without_values():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    slack.send_alert(
        channel='tests',
        title='The alert title',
        type='warning',
    )


def test_send_alert_reply():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    msg = slack.send_alert(
        channel='tests',
        title='The alert title',
        type='fail',
        values={
            'Field one': '`OK`',
            'Field two': 123456789,
            'Field three': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        }
    )
    reply = msg.send_reply('Reply in the thread')
    reply.delete()
    msg.delete()
