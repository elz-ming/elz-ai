from fastapi import APIRouter, Request
import jwt
from datetime import datetime, timedelta, timezone
from models.customResponse import resp_200
from setting import Setting

config = Setting()

router = APIRouter()


@router.get("/")
def api_version(request: Request):
    environment = request.app.state.settings.get("APP_ENV")
    version = request.app.state.settings.get("APP_API_VERSION")

    return resp_200(data={"environment": environment, "version": version}, message="success")


@router.get("/dev/token")
def generate_token(request: Request):
    secret = config.get("JWT_SECRET")
    payload = {
        "sub": "user123",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(payload, secret, algorithm="HS256")

    return resp_200(data={"token": token}, message="success")
