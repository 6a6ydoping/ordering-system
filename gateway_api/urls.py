from fastapi import APIRouter

from entities import *
from background_task.settings import youtube_wrapped_background_task
from gateway_api.dependencies import Producer
import models
from dependencies import *

router = APIRouter(prefix="")


@router.post("/bloger/", tags=['blogers'])
def create_bloger(bloger: CreateBloger, db: Database) -> str:
    db.add(models.Bloger(bloger.model_dump()))
    return bloger.name


@router.get("/blogers/", tags=["blogers"])
def get_blogers(db: Database) -> list[Bloger]:
    db_blogers = db.query(models.Bloger).scalars()
    return list(map(Bloger.model_validate, db_blogers))


@router.delete("/blogers/", tags=["blogers"])
def delete_bloger(db: Database, bloger_id: int) -> bool:
    try:
        bloger = db.get(models.Bloger, id=bloger_id)
        db.delete(bloger)
        return True
    except:
        return False


@router.get("/blogers/", tags=["blogers"])
def get_bloger_by_id(bloger: BlogerDependency) -> Bloger | None:
    return bloger


@router.post('/videos/', tags=["videos"])
def create_video(video: CreateVideo, db: Database) -> bool:
    video_data = video.model_dump()
    db.add_video(video_data)
    return True


@router.get('/videos/', tags=["videos"])
def get_videos(db: Database) -> list[Video]:
    db_videos = db.query(models.Video).scalars()
    return list(map(Video.model_validate, db_videos))


@router.delete("/videos/", tags=["videos"])
def delete_video(video: VideoDependency) -> bool:
    video.delete()
    return True


@router.get("/videos/", tags=["videos"])
def get_video_by_id(video: VideoDependency) -> Video | None:
    return video


@router.post("/playlists/", tags=["playlists"])
def create_playlist(Playlist: CreatePlaylist, db: Database) -> bool:
    db.add(models.Playlist, Playlist.model_dump())
    return True


@router.delete("/playlists/", tags=["playlists"])
def delete_playlist(Playlist: PlaylistDependency) -> bool:
    Playlist.delete()
    return True


@router.get("/playlists/", tags=["playlists"])
def get_playlists(db: Database) -> list[Playlist]:
    db_playlists = db.query(models.Playlist).scalars()
    return list(map(Playlist.model_validate, db_playlists))


@router.get("/playlists/", tags=["playlists"])
def get_playlist_by_id(Playlist: PlaylistDependency) -> Playlist | None:
    return Playlist


@router.put("/meetups/", tags=["meetups"])
def create_meetup(meetup: CreateMeetup, db: Database) -> bool:
    db.add(models.Meetup, meetup.model_dump())
    return True


@router.get("/meetups/", tags=["meetups"])
def get_meetups(db: Database) -> list[Meetup]:
    db_meetups = db.query(models.Meetup).scalars()
    return list(map(Meetup.model_validate, db_meetups))


@router.get("/meetups/", tags=["meetups"])
def get_meetup_by_id(meetup: MeetupDependency) -> Meetup | None:
    return meetup


@router.delete("/meetups/", tags=["meetups"])
def delete_meetup(meetup: MeetupDependency) -> bool:
    meetup.delete()
    return True


@router.post("/videos/", tags=["videos"])
def watched(video: VideoDependency, producer: Producer):
    used_id = 0  # It would work
    producer.produce(topic="watched", value={"user_id": used_id, "video_id": video.id})


@router.get("/youtubeWrappedStatus/", tags=["youtubeWrappedStatus"])
def get_youtube_wrapped_status(task: BackgroundTaskStatusDependency):
    return task


@router.post("/youtubeWrapped/", tags=["youtubeWrapped"])
def youtube_wrapped():
    return {"task_id": youtube_wrapped_background_task.send().message_id }


@router.get("youtubeWrapped/", tags=["youtubeWrapped"])
def get_youtube_wrapped(task: BackgroundTaskStatusDependency):
    return task
