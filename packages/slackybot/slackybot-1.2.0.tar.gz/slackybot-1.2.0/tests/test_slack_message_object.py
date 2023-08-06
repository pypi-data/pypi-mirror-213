from src.slackybot import Slack
from src.slackybot import exceptions

from dotenv import load_dotenv
import pytest
import os

load_dotenv()


def test_update_message():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    message = slack.send_message(channel='tests', text='Unit test message')
    message.update('Updated Unit test message')


def test_update_message_empty_text():
    with pytest.raises(exceptions.MissingText):
        slack = Slack(token=os.getenv('SLACK_TOKEN'))
        message = slack.send_message(channel='tests', text='Unit test message')
        message.update()


def test_delete_message():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    message = slack.send_message(channel='tests', text='Unit test message')
    message.delete()


def test_delete_message_already_deleted():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    message = slack.send_message(channel='tests', text='Unit test message')
    message.delete()
    with pytest.raises(exceptions.MessageAlreadyDeleted):
        message.delete()


def test_send_reply_and_list_replies():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    message = slack.send_message(channel='tests', text='Unit test message')
    message.send_reply('Test Reply')
    assert message.get_replies()


def test_update_reply():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    message = slack.send_message(channel='tests', text='Unit test message')
    reply = message.send_reply('Test Reply')
    reply.update('Test Reply updated')


def test_delete_reply():
    slack = Slack(token=os.getenv('SLACK_TOKEN'))
    message = slack.send_message(channel='tests', text='Unit test message')
    reply = message.send_reply('Test Reply')
    reply.delete()
