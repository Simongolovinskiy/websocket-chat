from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from punq import Container

from app.application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
)
from app.application.api.schemas import ErrorSchema
from app.domain.exceptions.base import ApplicationException
from app.services.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from app.services.init import init_container
from app.services.mediator import Mediator

router = APIRouter(tags=["Chat"])


@router.post(
    "/",
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Creating a new unique chat instance, if exists status code will be 400",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
    schema: CreateChatRequestSchema,
    container: Container = Depends(init_container),
) -> CreateChatResponseSchema:
    """Creating new chat instance."""
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(
            CreateChatCommand(title=schema.title)
        )
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": e.message},
        )
    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    "/{chat_oid}/messages",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateMessageResponseSchema,
    description="Creating a new message in chat.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_message_handler(
    chat_oid: str,
    schema: CreateMessageRequestSchema,
    container: Container = Depends(init_container),
) -> CreateMessageResponseSchema:
    """Creating new message instance in existing chat."""
    mediator: Mediator = container.resolve(Mediator)
    try:
        message, *_ = await mediator.handle_command(
            CreateMessageCommand(text=schema.text, chat_oid=chat_oid)
        )

    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )
    return CreateMessageResponseSchema.from_entity(message)
