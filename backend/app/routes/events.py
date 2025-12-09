from fastapi import APIRouter, Path, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import Select, update, select
from datetime import datetime, timedelta
from typing import Annotated, Tuple
from app.utils import session_auth
from app.database import get_db_session
from app.models import Event, Outcome, User
from decimal import Decimal


class SmallOutcomeDto(BaseModel):
    name: str
    coefficient: Decimal


class FullOutcomeDto(BaseModel):
    outcome_id: int
    name: str
    coefficient: Decimal
    total_size: int | None


class SmallEventDto(BaseModel):
    event_id: int
    name: str
    ended_at: datetime
    outcomes: list[SmallOutcomeDto]


class FullEventDto(BaseModel):
    event_id: int
    name: str
    description: str
    ended_at: datetime
    outcomes: list[FullOutcomeDto]


class MyEventDto(BaseModel):
    event_id: int
    name: str
    ended_at: datetime
    final_outcome_name: str | None


class CreateEventDto(BaseModel):
    name: str
    description: str
    ended_at: datetime
    outcomes: list[SmallOutcomeDto]


class UpdateOutcomeDto(BaseModel):
    outcome_id: int
    coefficient: Decimal


class UpdateEventDto(BaseModel):
    final_outcome_id: int | None
    outcomes: list[UpdateOutcomeDto]


router = APIRouter(prefix="/events")


@router.get("/all")
async def get_all_events() -> list[SmallEventDto]:
    result = []

    with get_db_session() as db_session:
        stmt = select(Event)

        for event in db_session.execute(stmt).scalars().all():
            result.append(SmallEventDto(event_id=event.id, name=event.name,
                                        ended_at=event.ended_at, outcomes=[SmallOutcomeDto(name=outcome.name, coefficient=outcome.coefficient) for outcome in event.outcomes]))

    return result


@router.get("/{event_id}")
async def get_event(event_id: Annotated[int, Path()]) -> FullEventDto:
    with get_db_session() as db_session:
        event = db_session.get(Event, event_id)

        if event is None:
            raise HTTPException(404, "Can't find event!")

        return FullEventDto(
            event_id=event.id,
            name=event.name,
            description=event.description,
            ended_at=event.ended_at,
            outcomes=[FullOutcomeDto(
                outcome_id=outcome.id, name=outcome.name, coefficient=outcome.coefficient, total_size=None) for outcome in event.outcomes],
        )


@router.get("/my/all")
async def get_my_events(user_id: Annotated[int, Depends(session_auth)]) -> list[MyEventDto]:
    with get_db_session() as db_session:
        stmt = select(Event.id, Event.name,
                      Event.ended_at, Outcome.name).where(Event.author_id == user_id).join(Outcome, Event.final_outcome_id == Outcome.id, isouter=True)

        print(stmt)

        return [MyEventDto(event_id=id, name=name, ended_at=ended_at, final_outcome_name=final_outcome_name) for id, name, ended_at, final_outcome_name in db_session.execute(stmt).all()]


@router.post("/my")
async def create_event(user_id: Annotated[int, Depends(session_auth)], eventDto: CreateEventDto) -> Response:
    with get_db_session() as db_session:
        user = db_session.get(User, user_id)

        if user is None:
            raise HTTPException(401, "Can't find user!")

        if not user.can_create_events:
            raise HTTPException(403, "User can't create events!")

        new_event = Event(
            name=eventDto.name, description=eventDto.description, ended_at=eventDto.ended_at, author_id=user.id)

        db_session.add(new_event)
        db_session.commit()

        db_session.refresh(new_event)

        for outcomeDto in eventDto.outcomes:
            new_outcome = Outcome(
                name=outcomeDto.name, coefficient=outcomeDto.coefficient, event_id=new_event.id)

            db_session.add(new_outcome)

        db_session.commit()

    return Response()


@router.patch("/my/{event_id}")
async def update_event(user_id: Annotated[int, Depends(session_auth)],
                       event_id: Annotated[int, Path(allow_inf_nan=False, ge=1)],
                       event_dto: UpdateEventDto,
                       ) -> Response:

    with get_db_session() as db_session:
        event = db_session.get(Event, event_id)

        if event is None:
            raise HTTPException(404, "Can't find event!")

        if event.author_id != user_id:
            raise HTTPException(403, "User isn't author for event!")

        if event.final_outcome_id is not None:
            raise HTTPException(409, "Event already has final outcome!")

        if event_dto.final_outcome_id is not None:
            stmt = select().column(Outcome.id).where(Outcome.event_id == event_id)

            if not event_dto.final_outcome_id in db_session.execute(stmt).scalars():
                raise HTTPException(
                    400, "Final outcome isn't related to this event!")

            stmt = update(Event).where(Event.id == event_id).values(
                final_outcome_id=event_dto.final_outcome_id)

            try:
                affected_rows_count = db_session.execute(stmt).rowcount
            except:
                db_session.rollback()
                raise

            if affected_rows_count == 0:
                db_session.rollback()
                raise HTTPException(404, "Can't find event!")

            db_session.commit()
            return Response()

        if len(event_dto.outcomes) > 0 and datetime.now() > event.ended_at:  # TODO: add time to request
            db_session.rollback()
            raise HTTPException(400, "Time's up!")

        for outcome_dto in event_dto.outcomes:
            stmt = update(Outcome).where(Outcome.id == outcome_dto.outcome_id, Outcome.event_id == event_id).values(
                coefficient=outcome_dto.coefficient)
            try:
                affected_rows_count = db_session.execute(stmt).rowcount
            except:
                db_session.rollback()
                raise

            print("updated outcomes " + str(affected_rows_count))

            if affected_rows_count == 0:
                db_session.rollback()
                raise HTTPException(404, "Can't find outcome!")

        db_session.commit()

    return Response()
