import pytest

from datetime import datetime

from app.domain.entities.messages import Message, Chat
from app.domain.exceptions.messages import TitleTooLongException
from app.domain.values.messages import Text, Title


def test_create_message_success_short_text():
    text = Text("Hello! My name is Alex!")
    message = Message(text=text)
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_message_success_long_text():
    text = Text("Hello! " * 300)
    message = Message(text=text)
    assert message.text == text
    assert message.created_at.date() == datetime.today().date()


def test_create_chat_success():
    title = Title("Hello world")
    chat = Chat(title=title)
    assert chat.title == title
    assert not chat.messages
    assert chat.created_at.date() == datetime.today().date()


def test_create_chat_failure_with_long_title():
    with pytest.raises(TitleTooLongException):
        Title("Hello world" * 250)


def test_add_message_to_chat_success():
    text = Text("Hello! My name is Alex!")
    message = Message(text=text)

    title = Title("Hello world")
    chat = Chat(title=title)

    chat.add_message(message)

    assert chat.messages
    assert message in chat.messages
