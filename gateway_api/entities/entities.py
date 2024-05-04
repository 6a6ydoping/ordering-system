from pydantic import BaseModel


class IdBaseModel(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Video(IdBaseModel):
    name: str
    filename: str
    subtitles: str


class Bloger(IdBaseModel):
    name: str


class Playlist(IdBaseModel):
    videos: list[Video]
    blogers: Bloger


class Merch(IdBaseModel):
    name: str
    description: str
    price: float
    bloger: Bloger


class Location(IdBaseModel):
    latitude: float
    longitude: float


class Meetup(IdBaseModel):
    name: str
    location: Location
    bloger: Bloger


class User(IdBaseModel):
    name: str
    email: str