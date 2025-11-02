from fastapi import FastAPI
from app.routes import *


app = FastAPI()
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(bets_router)
app.include_router(user_router)
