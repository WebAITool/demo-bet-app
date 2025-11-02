from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel, EmailStr

class RegisterUserModel(BaseModel):
    login: str
    password: str
    email: EmailStr

class CheckCode(BaseModel):
    email: EmailStr
    code: int
    
class LoginUserModel(BaseModel):
    login: str
    password: str


router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(user: RegisterUserModel) -> Response:
    return Response()

@router.post("/check_code")
async def check_code(code: CheckCode) -> Response:
    return Response()

@router.get("/login")
async def login(user: LoginUserModel) -> Response:
    return Response()