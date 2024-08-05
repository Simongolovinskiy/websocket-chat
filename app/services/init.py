from app.infrastructure.repositories.messages import MemoryChatRepository, BaseChatRepository
from app.services.commands.messages import CreateChatCommand, CreateChatCommandHandler
from app.services.mediator import Mediator


def init_mediator(mediator: Mediator, chat_repository: BaseChatRepository) -> None:
    mediator.register_command(
        CreateChatCommand,
        [CreateChatCommandHandler(chat_repository=chat_repository)]
    )