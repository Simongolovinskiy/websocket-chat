import pytest

from app.services.commands.messages import CreateChatCommand
from app.services.mediator import Mediator
from app.infrastructure.repositories.messages import BaseChatRepository


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,
    mediator: Mediator
):
    chat = (await mediator.handle_command(CreateChatCommand(title="GIGAChat")))[0]
    assert chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type())
