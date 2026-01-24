import hashlib
import hmac
import time
from urllib.parse import parse_qsl
from fastapi import Request, HTTPException
from config import BOT_TOKEN


def verify_telegram_login(data: dict) -> dict:
    """Verify Telegram Login Widget authentication"""
    if "hash" not in data:
        raise HTTPException(status_code=403, detail="Missing hash")

    received_hash = data.pop("hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(data.items())
    )

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if calculated_hash != received_hash:
        raise HTTPException(status_code=403, detail="Invalid Telegram login")

    # Optional: auth freshness (5 min)
    auth_date = int(data.get("auth_date", 0))
    if time.time() - auth_date > 300:
        raise HTTPException(status_code=403, detail="Login expired")

    return data
