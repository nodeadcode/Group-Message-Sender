from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession
from fastapi import HTTPException
import os

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)


# ==============================
# STEP 1: SEND OTP
# ==============================
async def send_otp(api_id: int, api_hash: str, phone: str):
    """
    Send OTP to user's Telegram
    """

    client = TelegramClient(
        StringSession(),
        api_id,
        api_hash
    )

    await client.connect()

    try:
        sent = await client.send_code_request(phone)
    except Exception as e:
        await client.disconnect()
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "phone_code_hash": sent.phone_code_hash,
        "session_string": client.session.save()
    }


# ==============================
# STEP 2: VERIFY OTP
# ==============================
async def verify_otp(
    api_id: int,
    api_hash: str,
    phone: str,
    otp: str,
    phone_code_hash: str,
    session_string: str
):
    """
    Verify OTP & return session
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
        raise HTTPException(
            status_code=401,
            detail="2FA enabled. Password required."
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    session = client.session.save()
    me = await client.get_me()

    return {
        "user_id": me.id,
        "username": me.username,
        "first_name": me.first_name,
        "session": session
    }


# ==============================
# STEP 3: VERIFY PASSWORD (2FA)
# ==============================
async def verify_password(
    api_id: int,
    api_hash: str,
    phone: str,
    password: str,
    phone_code_hash: str,
    session_string: str
):
    """
    Verify 2FA password & return session
    """

    client = TelegramClient(
        StringSession(session_string),
        api_id,
        api_hash
    )

    await client.connect()

    try:
        await client.sign_in(password=password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    session = client.session.save()
    me = await client.get_me()

    return {
        "user_id": me.id,
        "username": me.username,
        "first_name": me.first_name,
        "session": session
    }
