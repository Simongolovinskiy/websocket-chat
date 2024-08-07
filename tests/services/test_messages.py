import pytest

from faker import Faker

from app.domain.entities.messages import Chat
from app.domain.values.messages import Title
from app.services.commands.messages import CreateChatCommand
from app.services.exceptions.messages import ChatWithThatTitleAlreadyExistsException
from app.services.mediator import Mediator
from app.infrastructure.repositories.messages import BaseChatRepository


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker
):
    chat = (await mediator.handle_command(CreateChatCommand(title=faker.text())))[0]
    assert await chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type())


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker
):
    title_text = faker.text()
    chat = Chat(Title(title_text))
    await chat_repository.add_chat(chat)
    assert chat in chat_repository._saved_chats

    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        (await mediator.handle_command(CreateChatCommand(title=title_text)))
    assert len(chat_repository._saved_chats) == 1
