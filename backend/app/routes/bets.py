from typing import Annotated
from fastapi import APIRouter, Path
from fastapi.responses import Response
from pydantic import BaseModel


class BetUsersOut(BaseModel):
    login: str
    size: int


class CreateBetIn(BaseModel):
    event_id: int
    outcome_id: int
    size: int


class UserBetOut(BaseModel):
    event_name: str
    size: int
    outcome_name: str
    final_outcome_name: str | None


router = APIRouter(prefix="/bets")


@router.get("/{event_id}/{outcome_id}")
async def get_users_bets(
    event_id: Annotated[int, Path(ge=1)], outcome_id: Annotated[int, Path(ge=1)]
) -> list[BetUsersOut]:
    return [
        BetUsersOut(login="abba", size=2000000),
        BetUsersOut(login="amogus", size=18282),
    ]


@router.post("/my")
async def create_bet(bet: CreateBetIn) -> Response:
    return Response()


@router.get("/my")
async def get_my_bets() -> list[UserBetOut]:
    return [
        UserBetOut(
            event_name="Event 1",
            size=100,
            outcome_name="Very good",
            final_outcome_name=None,
        ),
        UserBetOut(
            event_name="Event 2",
            size=595,
            outcome_name="Very bad",
            final_outcome_name="Very bad",
        ),
    ]