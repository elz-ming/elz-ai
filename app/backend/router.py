from fastapi import APIRouter
from apis import main

router = APIRouter()

router.include_router(main.router, prefix="", tags=[""])
