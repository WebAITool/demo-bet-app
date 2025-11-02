from fastapi import APIRouter, Path
from fastapi.responses import Response
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Annotated


class SmallOutcomeInfo(BaseModel):
    name: str
    coefficient: float


class FullOutcomeOut(BaseModel):
    id: int
    name: str
    coefficient: float
    total_size: int | None


class SmallEventOut(BaseModel):
    event_id: int
    name: str
    ended_at: datetime
    outcomes: list[SmallOutcomeInfo]


class FullEventOut(BaseModel):
    event_id: int
    name: str
    description: str
    ended_at: datetime
    outcomes: list[FullOutcomeOut]


class MyEventOut(BaseModel):
    event_id: int
    name: str
    ended_at: datetime
    final_outcome_name: str


class CreateEventIn(BaseModel):
    name: str
    description: str
    ended_at: datetime
    outcomes: list[SmallOutcomeInfo]


class UpdateOutcomeIn(BaseModel):
    outcome_id: int
    coefficient: float


class EventUpdateIn(BaseModel):
    final_outcome_id: int | None
    outcomes: list[UpdateOutcomeIn]


router = APIRouter(prefix="/events")
my_events_router = APIRouter(prefix="/my")


@router.get("/all")
async def get_all_events() -> list[SmallEventOut]:
    return [
        SmallEventOut(
            event_id=1,
            name="Name",
            ended_at=datetime.now() + timedelta(days=10),
            outcomes=[
                SmallOutcomeInfo(name="Vse horosho", coefficient=1.5),
                SmallOutcomeInfo(name="Vse ploho", coefficient=0.8),
            ],
        )
    ]


@router.get("/{event_id}")
async def get_event(event_id: Annotated[int, Path()]) -> FullEventOut:
    return FullEventOut(
        event_id=event_id,
        name="Abba",
        description="Long text",
        ended_at=datetime.now() + timedelta(days=10),
        outcomes=[
            FullOutcomeOut(name="Vse horosho", coefficient=1.5, id=1, total_size=None),
            FullOutcomeOut(name="Vse ploho", coefficient=0.8, id=2, total_size=None),
        ],
    )


@my_events_router.get("/all")
async def get_my_events() -> list[MyEventOut]:
    return [
        MyEventOut(
            event_id=3,
            name="Third event",
            ended_at=datetime.now(),
            final_outcome_name="Vse very good",
        ),
        MyEventOut(
            event_id=4,
            name="Forth event",
            ended_at=datetime.now() - timedelta(days=5),
            final_outcome_name="Vse very bad",
        ),
    ]


@my_events_router.post("")
async def create_event(event: CreateEventIn) -> Response:
    return Response()


@my_events_router.patch("/{event_id}")
async def update_event(
    event_id: Annotated[int, Path(allow_inf_nan=False, ge=1)], event_update: EventUpdateIn
) -> Response:
    return Response()

router.include_router(my_events_router)