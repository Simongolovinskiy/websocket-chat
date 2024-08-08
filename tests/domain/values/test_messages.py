from datetime import datetime

import pytest

from app.domain.entities.messages import Chat, Message
from app.domain.events.messages import NewMessageReceivedEvent
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


def test_message_events():
    text = Text("Hello! My name is Alex!")
    message = Message(text=text)

    title = Title("Hello world")
    chat = Chat(title=title)

    chat.add_message(message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert len(events) == 1
    assert not pulled_events, pulled_events

    current_event = events[0]

    assert isinstance(current_event, NewMessageReceivedEvent)
    assert current_event.message_oid == message.oid
    assert current_event.chat_oid == chat.oid
    assert current_event.message_text == message.text.as_generic_type()
