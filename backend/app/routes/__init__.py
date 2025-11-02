from .auth import router as auth_router
from .events import router as events_router
from .bets import router as bets_router

__all__ = ["auth_router", "events_router", "bets_router"]
