from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from punq import Container

from app.application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema,
)
from app.application.api.schemas import ErrorSchema
from app.domain.exceptions.base import ApplicationException
from app.services.commands.messages import CreateChatCommand
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
):
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
