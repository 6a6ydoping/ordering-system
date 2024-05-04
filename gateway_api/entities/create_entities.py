from pydantic import BaseModel
from enum import Enum, auto


class CreateBloger(BaseModel):
    name: str


class CreateVideo(BaseModel):
    name: str
    bloger_name: str


class CreatePlaylist(BaseModel):
    name: str
    bloger_name: str


class CreateLocation(BaseModel):
    latitude: float
    longitude: float


class CreateMeetup(BaseModel):
    name: str
    location: CreateLocation


class User(BaseModel):
    name: str
    email: str


class YoutubeWrappedTask(BaseModel):
    id: int
    status: str

    def __init___(self, id: int, status: str):
        self.id = id
        self.status = status
