from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Path, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from app.database import get_db_session
from app.models import Bet, Event, Outcome, User
from app.utils import session_auth
from sqlalchemy import select, update


class BetRecordDto(BaseModel):
    login: str
    size: int


class CreateBetDto(BaseModel):
    event_id: int
    outcome_id: int
    size: int


class UserBetDto(BaseModel):
    event_name: str
    size: int
    outcome_name: str
    final_outcome_name: str | None


router = APIRouter(prefix="/bets")


@router.get("/{event_id}/{outcome_id}")
async def get_users_bets(
    event_id: Annotated[int, Path()], outcome_id: Annotated[int, Path()]
) -> list[BetRecordDto]:
    with get_db_session() as db_session:
        stmt = select(User.login, Bet.size) \
            .where(Bet.event_id == event_id, Bet.outcome_id == outcome_id) \
            .join(User, User.id == Bet.user_id)

        return [BetRecordDto(login=login, size=size) for login, size in db_session.execute(stmt).all()]


@router.post("/my")
async def create_bet(dto: CreateBetDto, user_id: Annotated[int, Depends(session_auth)]) -> Response:
    with get_db_session() as db_session:
        event = db_session.get(Event, dto.event_id)

        if event is None:
            raise HTTPException(404, "Can't find event!")

        if datetime.now() > event.ended_at:
            raise HTTPException(403, "Bets time is up!")

        for outcome in event.outcomes:
            if outcome.id == dto.outcome_id:
                current_coef = outcome.coefficient
                break
        else:
            raise HTTPException(409, "Outcome isn't related to event!")

        stmt = select(User.balance).where(User.id == user_id)
        balance = db_session.execute(stmt).scalar_one()

        if dto.size > balance:
            raise HTTPException(409, "Not enough credits!")

        bet = Bet(event_id=dto.event_id, outcome_id=dto.outcome_id,
                  size=dto.size, user_id=user_id, coefficient=current_coef)
        stmt = update(User).values(
            balance=balance - dto.size).where(User.id == user_id)

        try:
            db_session.add(bet)
            db_session.execute(stmt)
            db_session.flush()
        except:
            db_session.rollback()
            raise
        else:
            db_session.commit()

    return Response()


@router.get("/my")
# TODO: add creation time for bets sorting
async def get_my_bets(user_id: Annotated[int, Depends(session_auth)]) -> list[UserBetDto]:
    result = []
    with get_db_session() as db_session:
        for bet in db_session.execute(select(Bet).where(Bet.user_id == user_id)).scalars().all():
            result.append(UserBetDto(
                event_name=bet.event.name,
                size=bet.size,
                outcome_name=bet.outcome.name,
                final_outcome_name=bet.event.final_outcome.name if bet.event.final_outcome is not None else None))

    return result
