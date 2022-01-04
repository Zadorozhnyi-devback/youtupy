import os
import subprocess
from typing import List

from pytube import Playlist

from backend.const import PATH_TO_PLAYLISTS, VIDEO_NAME


def get_playlist(playlist_url: str) -> Playlist:
    return Playlist(url=playlist_url)


def get_dir_path(playlist_title: str, path_to_playlists: str) -> str:
    if path_to_playlists is None:
        path_to_playlists = PATH_TO_PLAYLISTS
    path = f'{path_to_playlists}/{playlist_title}'
    return path


def download_playlist_videos(playlist, output_path: str) -> None:
    for video in playlist.videos:
        video.streams.filter(
            only_audio=True
        ).get_audio_only().download(
            output_path=output_path
        )


def get_dir_mp4_files(dir_path: str) -> List[str]:
    videos = [
        file for file in os.listdir(path=dir_path) if file.endswith('.mp4')
    ]
    return videos


def convert_mp4_to_mp3(dir_videos: List[str], dir_path: str) -> None:
    for video in dir_videos:
        subprocess.call(
            [
                'ffmpeg', '-i', f'{dir_path}/{video}',
                f"{dir_path}/{video.split('.mp4')[VIDEO_NAME]}.mp3"
            ]
        )


def remove_videos(dir_videos: List[str], dir_path: str) -> None:
    for video in dir_videos:
        os.remove(f'{dir_path}/{video}')
