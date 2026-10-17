from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Artist(Base):
    __tablename__ ="artists"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)

    albums=relationship("Album", back_populates="artist")


class Album(Base):
    __tablename__="albums"

    id=Column(Integer, primary_key=True, index=True)
    title=Column(String, nullable=False)
    year=Column(Integer)
    artist_id=Column(Integer, ForeignKey("artists.id"), nullable=False)

    artist=relationship("Artist", back_populates="albums")










