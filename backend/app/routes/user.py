from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import select, update
from app.database import get_db_session
from app.models import User
from app.utils import session_auth

router = APIRouter(prefix="/user")


class UserInfoDto(BaseModel):
    login: str | None
    password: str | None


@router.get("/balance")
async def get_balance(user_id: Annotated[int, Depends(session_auth)]) -> Response:
    with get_db_session() as db_session:
        return Response(content=str(db_session.execute(select(User.balance).where(User.id == user_id)).scalar_one()))


@router.get("/info")
async def get_info(user_id: Annotated[int, Depends(session_auth)]) -> UserInfoDto:
    with get_db_session() as db_session:
        login, password = db_session.execute(
            select(User.login, User.password).where(User.id == user_id)).one()
        return UserInfoDto(login=login, password=password)


@router.post("/info")
async def set_info(info: UserInfoDto, user_id: Annotated[int, Depends(session_auth)]) -> Response:
    with get_db_session() as db_session:
        if info.login is not None and len(info.login) > 0:
            stmt = update(User).values(login=info.login)
            if db_session.execute(stmt).rowcount != 1:
                db_session.rollback()
                raise HTTPException(500, "Internal server error!")
            else:
                db_session.commit()

        if info.password is not None and len(info.password) > 0:
            stmt = update(User).values(password=info.password)
            if db_session.execute(stmt).rowcount != 1:
                db_session.rollback()
                raise HTTPException(500, "Internal server error!")
            else:
                db_session.commit()

    return Response()
