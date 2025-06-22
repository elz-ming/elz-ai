from fastapi import HTTPException, Request
from starlette.status import HTTP_403_FORBIDDEN
from setting import Setting

config = Setting()


class APIKeyValidator:
    def __init__(self):
        # Get API key from environment
        api_key = config.get("API_KEY")
        app_env = config.get("APP_ENV")

        # 🚨 In production, fail if the key is still default
        if app_env == "prod" and api_key == "default-secret-key":
            raise RuntimeError(
                "Missing or default API_KEY in production environment!")

        # ✅ Allow multiple keys if needed in the future
        self.allowed_keys = {api_key}

    async def __call__(self, request: Request):
        api_key = request.headers.get("x-api-key")

        if not api_key or api_key not in self.allowed_keys:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid or missing API key"
            )

        # ✅ Future billing: you could log usage per key here
        request.state.api_key = api_key
        return api_key
