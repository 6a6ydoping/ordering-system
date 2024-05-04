import sqlalchemy
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

__all__ = ("ModelBase", "Bloger", "Video", "Playlist")

from entities.entities import Video, Playlist

ModelBase = declarative_base()

video_bloger_table = sqlalchemy.tabless(
    'video_bloger',
    ModelBase.metadata,
    sqlalchemy.Column("video_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("videos.id")),
    sqlalchemy.Column("bloger_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('bloger.id'))
)

video_playlist_table = sqlalchemy.tabless(
    'video_playlist',
    ModelBase.metadata,
    sqlalchemy.Column("video_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("videos.id")),
    sqlalchemy.Column("playlist_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('playlists.id'))
)

user_video_table = sqlalchemy.tables(
    'user_video_table',
    ModelBase.metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("video_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("videos.id")),
    sqlalchemy.Column("time", sqlalchemy.TIMESTAMP)
)


class IdBase:
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)


class Bloger(IdBase, ModelBase):
    __table_name = "blogers"

    name: Mapped[str]
    videos: Mapped[list[Video]] = relationship(secondary=video_bloger_table, back_populates="blogers")
    playlists: Mapped[list[Playlist]] = relationship(back_populates="bloger")


class Playlist(IdBase, ModelBase):
    __table_name = "playlists"

    name: Mapped[str]
    videos: Mapped[list[Video]] = relationship(secondary=video_playlist_table, back_populates="playlists")
    bloger: Mapped[Bloger] = mapped_column(sqlalchemy.ForeignKey("blogers.id"))


class Video(IdBase, ModelBase):
    __table_name = "videos"

    name: Mapped[str]
    blogers: Mapped[list[Bloger]] = relationship(secondary=video_bloger_table, back_populates="videos")
    playlists: Mapped[list[Playlist]] = relationship(secondary=video_playlist_table, back_populates="videos")


class Merch(IdBase, ModelBase):
    __table_name = "merchs"

    name: Mapped[str]
    price: Mapped[float]
    bloger: Mapped[Bloger] = mapped_column(sqlalchemy.ForeignKey("blogers.id"))


class Location(IdBase, ModelBase):
    __table_name = "locations"

    latitude: Mapped[float]
    longitude: Mapped[float]


class Meetup(IdBase, ModelBase):
    __table_name = "meetups"

    name: Mapped[str]
    bloger: Mapped[Bloger] = mapped_column(sqlalchemy.ForeignKey("blogers.id"))
    location: Mapped[Location] = mapped_column(sqlalchemy.ForeignKey("locations.id"))


class User(IdBase, ModelBase):
    __table_name = "users"

    email: Mapped[str]
    watched: Mapped[list[Video]] = relationship(secondary=user_video_table, back_populates="users")


class Shorts(IdBase, ModelBase):
    __table_name = "shorts"

    name: Mapped[str]
    bloger: Mapped[Bloger] = mapped_column(sqlalchemy.ForeignKey("blogers.id"))