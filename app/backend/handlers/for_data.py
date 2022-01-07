import subprocess
from pathlib import Path
from typing import List
from urllib.error import URLError

from pytube import Playlist

from backend.const import VID_NAME


def get_playlist(playlist_url: str) -> Playlist:
    return Playlist(url=playlist_url)


def get_path_to_playlist(playlist_title: str, playlist_path: str) -> str:
    path = f'{playlist_path}/{playlist_title}'
    return path


def get_dir_mp4_files(path_to_playlist: str) -> List[Path]:
    videos = [file for file in Path(path_to_playlist).glob('**/*.mp4')]
    return videos


def convert_mp4_to_mp3(dir_videos: List[Path], path_to_playlist: str) -> None:
    for video in dir_videos:
        subprocess.call(
            [
                'ffmpeg', '-i', video,
                f"{path_to_playlist}/{video.name.split('.mp4')[VID_NAME]}.mp3"

            ]
        )


def remove_videos(dir_videos: List[Path]) -> None:
    for video in dir_videos:
        video.unlink()


def download_playlist_videos(
        playlist: Playlist, path_to_playlist: str
) -> None:
    for video in playlist.videos:
        video.streams.filter(
            only_audio=True
        ).get_audio_only().download(
            output_path=path_to_playlist
        )


def try_download_video(playlist: Playlist, path_to_playlist: str) -> bool:
    for _ in range(3):
        try:
            download_playlist_videos(
                playlist=playlist, path_to_playlist=path_to_playlist
            )
            return True
        except URLError:
            continue


def download_videos(playlist: Playlist, path_to_playlist: str) -> None:
    download_complete = try_download_video(
        playlist=playlist, path_to_playlist=path_to_playlist
    )
    if download_complete:
        dir_videos = get_dir_mp4_files(path_to_playlist=path_to_playlist)
        convert_mp4_to_mp3(
            dir_videos=dir_videos, path_to_playlist=path_to_playlist
        )
        remove_videos(dir_videos=dir_videos)
