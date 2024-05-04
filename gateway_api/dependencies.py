from typing import Annotated
import dramatiq
from fastapi import Depends
from sqlalchemy.orm import Session
import models
from gateway_api.entities import YoutubeWrappedTask
from database import get_db, get_kafka_producer
from entities import Bloger, Video, Playlist, Meetup

Database = Annotated[Session, Depends(get_db)]
Producer = Annotated[confluent_kafka.Producer, Depends(get_kafka_producer)]


def get_bloger_model(bloger_id: int, db: Database) -> models.Bloger | None:
	db_bloger = db.get(models.Bloger, bloger_id)
	return db_bloger


def get_video_model(video_id: int, db: Database) -> models.Video | None:
	db_video = db.get(models.Video, video_id)
	return db_video


def get_playlist_model(playlist_id: int, db: Database) -> models.Playlist | None:
	db_playlist = db.get(models.Playlist, playlist_id)
	return db_playlist


def get_meetup_by_id(meetup_id: int, db: Database) -> models.Meetup | None:
	return db.get(models.Meetup, meetup_id)


def get_background_task_by_id(task_id: int) -> YoutubeWrappedTask | None:
	task = dramatiq.Message.fetch(task_id)
	if task is None:
		return None
	return YoutubeWrappedTask(task_id, task.get_status())


class BlogerDependencyClass:
	def __call__(self, db_bloger: models.Bloger = Depends(get_bloger_model)) -> Bloger | None:
		return Bloger.model_validate(db_bloger)


class VideoDependencyClass:
	def __call__(self, db_video: models.Video = Depends(get_video_model)) -> Video | None:
		return Video.model_validate(db_video)


class PlaylistDependencyClass:
	def __call__(self, db_playlist: models.Playlist = Depends(get_playlist_model)) -> Playlist | None:
		return Playlist.model_validate(db_playlist)


class MeetupDependencyClass:
	def __call__(self, db_meetup: models.Meetup = Depends(get_meetup_by_id)) -> Meetup | None:
		return Meetup.model_validate(db_meetup)


BlogerDependency = Annotated[Bloger, Depends(BlogerDependencyClass())]
VideoDependency = Annotated[Video, Depends(VideoDependencyClass())]
PlaylistDependency = Annotated[Playlist, Depends(PlaylistDependencyClass())]
MeetupDependency = Annotated[Meetup, Depends(MeetupDependencyClass())]

ModelBlogerDependency = Annotated[models.Bloger, Depends(get_bloger_model)]
ModelVideoDependency = Annotated[models.Video, Depends(get_video_model)]
ModelPlaylistDependency = Annotated[models.Playlist, Depends(get_playlist_model)]
ModelMeetupDependency = Annotated[models.Meetup, Depends(get_meetup_by_id)]

BackgroundTaskStatusDependency = Annotated[YoutubeWrappedTask, Depends(get_background_task_by_id)]
