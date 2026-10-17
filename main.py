from fastapi import FastAPI

from database import engine, Base
from routers import artists, albums

Base.metadata.create_all(engine)

app = FastAPI(title="Music API")

app.include_router(artists.router)
app.include_router(albums.router)






