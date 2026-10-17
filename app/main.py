from fastapi import FastAPI

from app.database import engine, Base
from app.routers import albums
from app.routers import artists

Base.metadata.create_all(engine)

app = FastAPI(title="Music API")

app.include_router(artists.router)
app.include_router(albums.router)






