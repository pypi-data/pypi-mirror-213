# Slackybot
This Python package helps you with sending messages to Slack. It offers an object-oriented approach - every message or reply in a thread is an object, so they can be easily managed.

## Getting started
### Installation
```commandline
python -m pip install slackybot
```
Add following token scopes to your Slack bot:  
`channels:join` `channels:read` `chat:write` `chat:write.customize` `chat:write.public`

### Simple usage
Import and initialize the slack object
```python
from slackybot import Slack

slack = Slack(token='XXX')
```
As a best practice, it is better to pass the token using an environment variable (e.g. `.env` file)

To send a message you have to use the Slack object method. It takes two arguments: `channel` and `text` they are both strings. 
```python
slack.send_message(channel='channel-name', text='Sample text')
```
The above method returns the `Message` object.

To update a message you may use the Message method `.update()`. It takes one argument: `text` as a string.
```python
message = slack.send_message(channel='', text='')
message.update(text='New text')
```

To send a reply in the message thread simply use `.send_reply()` method. It takes one argument: `text` as a string.
```python
message = slack.send_message(channel='', text='')
message.send_reply(text='Reply message in the thread')
```
The above method returns the `Reply` object.

Both objects `Message` and `Reply` can be deleted by using `.delete()` method on them. Those objects can be listed using:
* `.get_messages()` on the Slack object
* `.get_replies()` on the Message object