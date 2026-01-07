from fastapi import FastAPI, Request
from telegram_auth import verify_telegram_login
from itsdangerous import URLSafeSerializer

app = FastAPI()

SESSION_SECRET = "CHANGE_THIS_SECRET"
serializer = URLSafeSerializer(SESSION_SECRET)


@app.post("/auth/telegram")
async def telegram_auth(request: Request):
    form = await request.form()
    data = dict(form)

    user = verify_telegram_login(data)

    # create signed session token
    session_token = serializer.dumps({
        "id": user["id"],
        "username": user.get("username"),
        "name": user.get("first_name")
    })

    return {
        "status": "ok",
        "session_token": session_token,
        "user": {
            "id": user["id"],
            "username": user.get("username"),
            "name": user.get("first_name")
        }
    }
