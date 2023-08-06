from .. import exceptions

data = {
    'urls': {
        'slack_api': 'https://slack.com/api',
        'post_message': 'https://slack.com/api/chat.postMessage',
        'update_message': 'https://slack.com/api/chat.update',
        'delete_message': 'https://slack.com/api/chat.delete',
    },
    'error_exceptions': {
        'channel_not_found': exceptions.ChannelNotFound,
        'no_text': exceptions.MissingText,
        'message_not_found': exceptions.MessageNotFound,
    },
    'alert': {
        'colors': {
            'success': 'good',
            'warning': 'warning',
            'fail': 'danger',
        },
        'icons': {
            'success': ':white_check_mark:',
            'fail': ':x:',
            'warning': ':warning:',
        },
    },
    'default_icon': 'http://lorempixel.com/48/48',
}
