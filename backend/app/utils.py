from fastapi import Request, HTTPException
from http.cookies import SimpleCookie
from app.database import get_db_session
from app.models import Session


async def session_auth(request: Request) -> int:  # for dependency inj
    cookies_str = request.headers.get("Cookie")
    if cookies_str is None:
        raise HTTPException(status_code=401, detail="Cookies are missing!")

    cookies = SimpleCookie()
    cookies.load(cookies_str)
    session_id = int(cookies['sessionid'].value)
    with get_db_session() as db_session:
        session = db_session.get(Session, session_id)
        if session is None:
            raise HTTPException(status_code=401, detail="Invalid session id!")
        user_id = session.user_id

    return user_id
