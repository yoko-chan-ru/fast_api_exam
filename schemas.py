from pydantic import BaseModel, ConfigDict
from typing import List

class AlbumBase(BaseModel):
    title: str
    year: int


class AlbumCreate(AlbumBase):
    artist_id: int


class AlbumOut(AlbumBase):
    id: int
    artist_id: int

    model_config = ConfigDict(from_attributes=True)


class ArtistBase(BaseModel):
    name: str


class ArtistCreate(ArtistBase):
    pass


class ArtistOut(ArtistBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ArtistWithAlbums(ArtistOut):
    albums: List[AlbumOut] = []








