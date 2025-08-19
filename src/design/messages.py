import abc
import enum
from dataclasses import dataclass
from typing import Callable


class MessageType(enum.Enum):
    TELEGRAM = enum.auto()
    MATTERMOST = enum.auto()
    SLACK = enum.auto()


@dataclass
class JsonMessage:
    message_type: MessageType
    payload: str


@dataclass
class ParsedMessage:
    """There is no need to describe anything here."""


class FactoryClasses(abc.ABC):
    @abc.abstractmethod
    def parse(self):
        pass


class ParserFactory:
    def __init__(self, message: JsonMessage):
        self.message = message

    def set_parser(self):
        def get_parser(message_type: MessageType):
            raw_subclasses = FactoryClasses.__subclasses__()
            classes: dict[str, Callable[..., object]] = {c.__name__: c for c in raw_subclasses}
            message_type = str(message_type._name_).title() + 'Message'
            message_class = classes.get(message_type, None)
            if message_class is not None:
                return message_class
            raise NotFoundError

        return get_parser(self.message.message_type)


class TelegramMessage(FactoryClasses):
    def parse(self):
        pass


class MattermostMessage(FactoryClasses):
    def parse(self):
        pass


class SlackMessage(FactoryClasses):
    def parse(self):
        pass


class NotFoundError(ValueError):
    pass
