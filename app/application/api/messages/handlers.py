from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from punq import Container

from app.application.api.messages.filters import GetMessagesFilters
from app.application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
    CreateMessageRequestSchema,
    CreateMessageResponseSchema,
    ChatDetailSchema,
    GetMessagesQueryResponseSchema,
    MessageDetailSchema,
)
from app.application.api.schemas import ErrorSchema
from app.domain.exceptions.base import ApplicationException
from app.services.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
)
from app.services.init import init_container
from app.services.mediator import Mediator
from app.services.queries.messages import GetChatDetailQuery, GetMessagesQuery

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


@router.get(
    "/{chat_oid}/",
    status_code=status.HTTP_200_OK,
    description="getting current chat.",
    responses={
        status.HTTP_200_OK: {"model": ChatDetailSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def fetch_chat_with_messages_handler(
    chat_oid: str, container: Container = Depends(init_container)
) -> ChatDetailSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        chat = await mediator.handle_query(
            GetChatDetailQuery(chat_oid=chat_oid)
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": exception.message},
        )
    return ChatDetailSchema.from_entity(chat)


@router.get(
    "/{chat_oid}/messages/",
    status_code=status.HTTP_200_OK,
    description="getting all messages in current chat.",
    responses={
        status.HTTP_200_OK: {"model": GetMessagesQueryResponseSchema},
        status.HTTP_404_NOT_FOUND: {"model": ErrorSchema},
    },
)
async def fetch_chat_messages_handler(
    chat_oid: str,
    filters: GetMessagesFilters = Depends(),
    container: Container = Depends(init_container),
) -> GetMessagesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        messages, count = await mediator.handle_query(
            GetMessagesQuery(
                chat_oid=chat_oid, filters=filters.to_infrastructure()
            )
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": exception.message},
        )
    return GetMessagesQueryResponseSchema(
        count=count,
        limit=filters.limit,
        offset=filters.offset,
        messages=[
            MessageDetailSchema.from_entity(message) for message in messages
        ],
    )
