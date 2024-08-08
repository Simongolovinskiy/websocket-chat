from app.domain.entities.messages import Chat, Message


def convert_message_to_document(message: Message) -> dict:
    return dict(
        oid=message.oid,
        text=message.text.as_generic_type(),
        created_at=message.created_at,
    )


def convert_entity_to_document(chat: Chat) -> dict:
    return dict(
        oid=chat.oid,
        title=chat.title.as_generic_type(),
        created_at=chat.created_at,
        messages=[
            convert_message_to_document(message) for message in chat.messages
        ],
    )
