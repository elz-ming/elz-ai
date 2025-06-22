import jwt
from datetime import datetime, timezone
from setting import Setting

config = Setting()
JWT_SECRET = config.get("JWT_SECRET")


def decodeJWT(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        exp = decoded_token.get("exp")
        if exp is not None and datetime.now(timezone.utc).timestamp() > exp:
            return None  # expired token
        return decoded_token

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None
