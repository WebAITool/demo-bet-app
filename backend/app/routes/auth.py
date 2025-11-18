from fastapi import APIRouter
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel, EmailStr
from app.models import User, Session, EmailCode
from app.database import get_db_session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from datetime import datetime, timedelta


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
# TODO: how to generate new codes?
async def register(user_reg_dto: UserRegistrationDto) -> Response:
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
            return JSONResponse(
                status_code=409, content={"message": "Email already in use!"}
            )
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
                                       check_code.email and EmailCode.code == check_code.code)
        email_code = session.execute(stmt).scalar()

        if email_code is None:
            return JSONResponse(
                {"message": "Can't find code for this email!"}, status_code=404
            )

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

        return Response(headers={"Set-Cookie": "sessionid=" + str(new_session.id)})


@router.get("/login")
async def login(user_login_dto: UserLoginDto) -> Response:
    stmt = select(User).where(
        User.login == user_login_dto.login and User.password == user_login_dto.password and User.is_confirmed)
    with get_db_session() as session:
        user = session.execute(stmt).scalar()

        if user is None:
            return JSONResponse({"message": "Invalid login or password!"}, status_code=404)
        
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

        return Response(headers={"Set-Cookie": "sessionid=" + str(new_session.id)})
