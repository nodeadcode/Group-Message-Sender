from telethon import TelegramClient
from telethon.errors import (
    UserNotParticipantError,
    ChatWriteForbiddenError
)
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import Channel, Chat


async def verify_groups(
    session_file: str,
    api_id: int,
    api_hash: str,
    group_links: list
):
    """
    Verifies up to 5 Telegram groups (public + private)
    User must already be a member
    """

    if len(group_links) > 5:
        return {"error": "Maximum 5 groups allowed"}

    client = TelegramClient(session_file, api_id, api_hash)
    await client.connect()

    verified_groups = []
    failed_groups = []

    for link in group_links:
        try:
            entity = await client.get_entity(link)

            # Public or private channel/group
            if isinstance(entity, (Channel, Chat)):
                # Check membership (channels)
                if isinstance(entity, Channel):
                    try:
                        await client(GetParticipantRequest(
                            channel=entity,
                            participant='me'
                        ))
                    except UserNotParticipantError:
                        raise Exception("Not a member of this group")

                # Test write permission (safe dummy check)
                try:
                    await client.send_message(entity, " ")
                    await client.delete_messages(entity, await client.get_messages(entity, limit=1))
                except ChatWriteForbiddenError:
                    raise Exception("You cannot send messages in this group")

                verified_groups.append({
                    "id": entity.id,
                    "title": entity.title,
                    "type": "private" if entity.private else "public"
                })

        except Exception as e:
            failed_groups.append({
                "link": link,
                "reason": str(e)
            })

    await client.disconnect()

    return {
        "verified": verified_groups,
        "failed": failed_groups
    }
