from fastapi import FastAPI
from app.routes import auth_router, events_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(events_router)
