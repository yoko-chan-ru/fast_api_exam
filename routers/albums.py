from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Album, Artist
from schemas import AlbumOut, AlbumCreate

router = APIRouter(prefix="/albums", tags=["albums"])

@router.get("/", response_model=list[AlbumOut])
def get_albums(db: Session = Depends(get_db)):
    return db.scalars(select(Album)).all()


@router.get("/{album_id}", response_model=AlbumOut)
def get_album(album_id: int, db: Session= Depends(get_db)):
    album=db.get(Album, album_id)
    if album is None:
        raise HTTPException(status_code=404, detail="Альбом не найден")
        
    return album


@router.post("/", response_model=AlbumOut, status_code=201)
def create_album(data: AlbumCreate, db: Session=Depends(get_db)):
    artist = db.get(Artist, data.artist_id)
    if artist is None:
        raise HTTPException(status_code=404, detail="Исполнитель не найден")
    
    album = Album(**data.model_dump())
    db.add(album)
    db.commit()
    db.refresh(album)
    return album










