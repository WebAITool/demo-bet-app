from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

router = APIRouter(prefix="/user")


class UserInfo(BaseModel):
    login: str
    password: str


@router.get("/balance")
async def get_balance() -> Response:
    return Response(content="1000")


@router.get("/info")
async def get_info() -> UserInfo:
    return UserInfo(login="asdasdas", password="asdasd$#$#%55")


@router.post("/info")
async def set_info(info: UserInfo) -> Response:
    return Response()
