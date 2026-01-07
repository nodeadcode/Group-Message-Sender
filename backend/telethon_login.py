from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession

import os

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)


async def send_otp(api_id: int, api_hash: str, phone: str):
    """
    Step 1: Send OTP to user's Telegram
    """
    client = TelegramClient(
        StringSession(),
        api_id,
        api_hash
    )

    await client.connect()
    sent = await client.send_code_request(phone)

    return {
        "phone_code_hash": sent.phone_code_hash,
        "session": client.session.save()
    }


async def verify_otp(api_id: int, api_hash: str, phone: str,
                     otp: str, phone_code_hash: str,
                     session_string: str, user_id: int):
    """
    Step 2: Verify OTP & save session
    """
    client = TelegramClient(
        StringSession(session_string),
        api_id,
        api_hash
    )

    await client.connect()

    try:
        await client.sign_in(
            phone=phone,
            code=otp,
            phone_code_hash=phone_code_hash
        )
    except SessionPasswordNeededError:
        return {"error": "2FA enabled. Password login not supported in MVP."}

    # Save session file per user
    session_path = f"{SESSIONS_DIR}/{user_id}.session"
    client.session.save(session_path)

    await client.disconnect()

    return {
        "status": "ok",
        "session_file": session_path
    }
