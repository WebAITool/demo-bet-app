from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel, EmailStr
from app.models import User, Session, EmailCode
from app.database import get_db_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from datetime import datetime, timedelta
from http.cookies import SimpleCookie


class UserRegistrationDto(BaseModel):
    login: str
    password: str
    email: EmailStr


class CheckCodeDto(BaseModel):
    email: EmailStr
    code: int


class UserLoginDto(BaseModel):
    login: str
    password: str


router = APIRouter(prefix="/auth")


@router.post("/register")
async def register(user_reg_dto: UserRegistrationDto) -> Response:
    # TODO: how to generate new codes for existing user?
    new_user = User(
        login=user_reg_dto.login,
        password=user_reg_dto.password,
        can_create_events=False,
        email=user_reg_dto.email,
        is_confirmed=False
    )

    new_email_code = EmailCode(
        email=user_reg_dto.email, code=1234, expires_at=datetime.now() + timedelta(days=7))

    with get_db_session() as session:
        try:
            session.add(new_user)
            session.add(new_email_code)
            session.flush()
        except IntegrityError:
            session.rollback()
            raise HTTPException(
                status_code=409, detail="Email already in use!")
        except:
            session.rollback()
            raise
        else:
            session.commit()

    return Response()


@router.post("/check_code")
async def check_code(check_code: CheckCodeDto) -> Response:
    with get_db_session() as session:
        stmt = select(EmailCode).where(EmailCode.email ==
                                       check_code.email, EmailCode.code == check_code.code)
        email_code = session.execute(stmt).scalar()

        if email_code is None:
            raise HTTPException(404, "Can't find code for this email!")

        stmt = select(User).where(User.email == email_code.email)
        user = session.execute(stmt).scalar_one()

        try:
            session.delete(email_code)
            session.flush()
        except:
            session.rollback()
            raise
        else:
            session.commit()

        new_session = Session(
            user_id=user.id, expires_at=datetime.now() + timedelta(days=30))

        try:
            session.add(new_session)
            session.execute(update(User), [{
                "id": user.id, "is_confirmed": True
            }])
            session.flush()
        except:
            session.rollback()
            raise
        else:
            session.commit()

        session.refresh(new_session)
        response = Response()
        response.set_cookie("sessionid", str(new_session.id))
        return response


@router.post("/login")
async def login(user_login_dto: UserLoginDto) -> Response:
    stmt = select(User).where(
        User.login == user_login_dto.login, User.password == user_login_dto.password, User.is_confirmed)
    with get_db_session() as session:
        user = session.execute(stmt).scalar()

        if user is None:
            raise HTTPException(404, "Invalid login or password!")

        new_session = Session(
            user_id=user.id, expires_at=datetime.now() + timedelta(days=30))

        try:
            session.add(new_session)
            session.flush()
        except:
            session.rollback()
            raise
        else:
            session.commit()

        session.refresh(new_session)
        response = Response()
        response.set_cookie("sessionid", str(new_session.id))
        return response
