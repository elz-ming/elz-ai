from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN
from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Invalid authentication scheme"
                )

            if not self.verify_jwt(request=request, jwtoken=credentials.credentials):
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Invalid token or expired token"
                )

            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Missing authorization token."
            )

    def verify_jwt(self, request: Request, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)

        except:
            payload = None

        if payload:
            isTokenValid = True

            # request.app.state.current_user_id = payload["user_claims"]["userId"]

        return isTokenValid
