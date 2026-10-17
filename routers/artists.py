from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Artist
from schemas import ArtistOut, ArtistWithAlbums, ArtistCreate

router = APIRouter(prefix="/artists", tags=["artists"])

@router.get("/", response_model=list[ArtistOut])
def get_artists(db: Session = Depends(get_db)):
    return db.scalars(select(Artist)).all()


@router.post("/", response_model=ArtistOut, status_code=201) 
def create_artist(data: ArtistCreate, db: Session = Depends(get_db)):
    artist = Artist(**data.model_dump())
    db.add(artist)
    db.commit()
    db.refresh(artist)
    return artist


@router.get("/{artist_id}/albums", response_model=ArtistWithAlbums)
def get_artist_albums(artist_id: int, db: Session = Depends(get_db)):
    artist = db.get(Artist, artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    return artist










