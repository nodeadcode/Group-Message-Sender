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

# ==============================
# STEP 4: GET SAVED MESSAGES (AUTOMATION)
# ==============================
async def get_saved_messages(
    api_id: int,
    api_hash: str,
    session_file: str,
    limit: int = 10
):
    """
    Fetch messages from user's 'Saved Messages' (me)
    Top to bottom (oldest to newest logic handled in app)
    """
    # Use FileSession if path provided, else StringSession
    if os.path.exists(session_file):
        client = TelegramClient(session_file, api_id, api_hash)
    else:
        # Fallback if session_file is actually a string string
        client = TelegramClient(StringSession(session_file), api_id, api_hash)

    await client.connect()
    
    if not await client.is_user_authorized():
        await client.disconnect()
        raise HTTPException(status_code=401, detail="Session invalid or expired")

    messages = []
    try:
        # Get 'Saved Messages' (peer='me')
        # Using reverse=True to get oldest first if needed, 
        # but let's just get recent ones for now and sort in logic
        async for message in client.iter_messages('me', limit=limit):
            if message.text: # Only text for now, can expand to media
             messages.append({
                 "id": message.id,
                 "text": message.text,
                 "date": message.date.isoformat(),
                 "media": bool(message.media)
             })
             
    except Exception as e:
        await client.disconnect()
        raise HTTPException(status_code=400, detail=str(e))

    await client.disconnect()
    return messages
