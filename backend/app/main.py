from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(bets_router)
app.include_router(user_router)
