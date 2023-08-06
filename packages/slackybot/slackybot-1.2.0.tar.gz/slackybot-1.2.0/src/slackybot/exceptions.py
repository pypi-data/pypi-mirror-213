class SlackInitializeError(Exception):

    def __init__(self, message="Unable to initialize Slack object"):
        self.message = message
        super().__init__(self.message)


class Unknown(Exception):

    def __init__(self, message=""):
        self.message = f"Unknown exception ({message})"
        super().__init__(self.message)


class MessageNotSend(Exception):

    def __init__(self, message="The message has not been sent"):
        self.message = message
        super().__init__(self.message)


class MessageNotUpdated(Exception):

    def __init__(self, message="The message has not been updated"):
        self.message = message
        super().__init__(self.message)


class NotASlackMessage(Exception):

    def __init__(self, message="Given value is not a SlackMessage object"):
        self.message = message
        super().__init__(self.message)


class MessageNotFound(Exception):

    def __init__(self, message="The message has not been found"):
        self.message = message
        super().__init__(self.message)


class MessageAlreadyDeleted(Exception):

    def __init__(self, message="The message has been already deleted"):
        self.message = message
        super().__init__(self.message)


class MessageNotDeleted(Exception):

    def __init__(self, message="The message has not been deleted"):
        self.message = message
        super().__init__(self.message)


class ChannelNotFound(Exception):

    def __init__(self, message="Given channel not found"):
        self.message = message
        super().__init__(self.message)


class MissingText(Exception):

    def __init__(self, message="There is no text"):
        self.message = message
        super().__init__(self.message)


class WrongAlertType(Exception):

    def __init__(self, message="Wrong the alert type. Possible options: success, fail, warning"):
        self.message = message
        super().__init__(self.message)
