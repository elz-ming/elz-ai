from fastapi import APIRouter, Depends
from apis import main, ingest
from auth.auth_bearer import JWTBearer

router = APIRouter()

# Main routes (e.g. health check, version info)
router.include_router(main.router, prefix="", tags=[
                      "Main"], include_in_schema=True)

# Ingest-related routes (e.g. upload, label, tag chunks)
router.include_router(ingest.router, prefix="/ingest",
                      tags=["Ingest"], dependencies=[Depends(JWTBearer())], include_in_schema=True)
