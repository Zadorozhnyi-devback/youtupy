import subprocess
from pathlib import Path
from typing import List
from urllib.error import URLError

from pytube import Playlist

from backend.const import PATH_TO_PLAYLISTS, VIDEO_NAME


def get_playlist(playlist_url: str) -> Playlist:
    return Playlist(url=playlist_url)


def get_dir_path(playlist_title: str, path_to_playlists: str) -> str:
    if path_to_playlists is None:
        path_to_playlists = PATH_TO_PLAYLISTS
    path = f'{path_to_playlists}/{playlist_title}'
    return path


def get_dir_mp4_files(dir_path: str) -> List[Path]:
    videos = [file for file in Path(dir_path).glob('**/*.mp4')]
    return videos


def convert_mp4_to_mp3(dir_videos: List[Path], dir_path: str) -> None:
    for video in dir_videos:
        subprocess.call(
            [
                'ffmpeg', '-i', video,
                f"{dir_path}/{video.name.split('.mp4')[VIDEO_NAME]}.mp3"
            ]
        )


def remove_videos(dir_videos: List[Path], dir_path: str) -> None:
    for video in dir_videos:
        video_path = Path() / dir_path / video.name
        video_path.unlink()


def download_playlist_videos(playlist, output_path: str) -> None:
    for video in playlist.videos:
        video.streams.filter(
            only_audio=True
        ).get_audio_only().download(
            output_path=output_path
        )


def try_download_video(playlist: Playlist, output_path: str) -> bool:
    for _ in range(3):
        try:
            download_playlist_videos(
                playlist=playlist, output_path=output_path
            )
            return True
        except URLError:
            continue


def download_videos(playlist: Playlist, dir_path: str) -> None:
    download_complete = try_download_video(
        playlist=playlist, output_path=dir_path
    )
    if download_complete:
        dir_videos = get_dir_mp4_files(dir_path=dir_path)
        convert_mp4_to_mp3(dir_videos=dir_videos, dir_path=dir_path)
        remove_videos(dir_videos=dir_videos, dir_path=dir_path)
