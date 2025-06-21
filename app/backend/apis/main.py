from fastapi import APIRouter, Request
from models.customResponse import resp_200, resp_400, resp_500

router = APIRouter()


@router.get("/")
def api_version(request: Request):
    environment = request.app.state.settings.get("APP_ENV")
    version = request.app.state.settings.get("APP_API_VERSION")

    return resp_200(data={"environment": environment, "version": version}, message="success")
