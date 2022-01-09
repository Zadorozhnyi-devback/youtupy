import os
import subprocess
from pathlib import Path
from typing import List, Union
from urllib.error import URLError

from pytube import Playlist, YouTube
import pytube

from backend.const import VID_NAME, RETRY_AMOUNT


def get_download_object(class_name: str, url: str) -> Union[Playlist, YouTube]:
    obj = getattr(pytube, class_name)(url=url)
    return obj


def get_path_to_playlist(playlist_title: str, playlist_path: str) -> str:
    path = str(Path(f'{playlist_path}/{playlist_title}').resolve())
    return path


def get_dir_mp4_files(path_to_dir: str) -> List[Path]:
    videos = [file for file in Path(path_to_dir).glob('**/*.mp4')]
    return videos


def get_listdir(path: str) -> List[str]:
    dirs = os.listdir(path=path)
    return dirs


def convert_mp4_to_mp3(videos: List[Path], destination_path: str) -> None:
    for video in videos:
        subprocess.call(
            [
                'ffmpeg', '-i', video,
                f"{destination_path}/{video.name.split('.mp4')[VID_NAME]}.mp3"

            ]
        )


def remove_videos(dir_videos: List[Path]) -> None:
    for video in dir_videos:
        video.unlink()


def download_playlist(
    playlist: Playlist, path_to_playlist: str
) -> None:
    for video in playlist.videos:
        video.streams.filter(
            only_audio=True
        ).get_audio_only().download(
            output_path=path_to_playlist, filename=f'{video.title}.mp4'
        )


def download_video(video: YouTube, path: str) -> None:
    # сделать выпадашку с выбором качества видео
    video.streams.filter(
        file_extension='mp4',
    ).get_highest_resolution().download(
        output_path=path, filename=f'{video.title}.mp4'
    )


def try_download(
    process_func: str, args: List[Union[Playlist, YouTube]]
) -> bool:
    for _ in range(RETRY_AMOUNT):
        try:
            # didn't find another solution, so call func by its name like this
            eval(f"{process_func}(*args)")
            return True
        except URLError:
            continue


def get_needed_videos(
    download_type_object: Union[Playlist, YouTube], destination_path: str
) -> List[Path]:
    if isinstance(download_type_object, Playlist):
        videos = get_dir_mp4_files(path_to_dir=destination_path)
    # раскоментить когда каналы будут
    # elif isinstance(download_type_object, YouTube):
    else:
        videos = [
            video for video in
            Path(destination_path).glob(f'**/{download_type_object.title}.mp4')
            if video
        ]
    return videos


def check_and_download(
    download_type_object: Union[Playlist, YouTube],
    destination_path: str, selected_extension: str, process_func: str
) -> None:
    download_complete = try_download(
        process_func=process_func,
        args=[download_type_object, destination_path]
    )
    if download_complete and selected_extension == '.mp3':
        videos = get_needed_videos(
            download_type_object=download_type_object,
            destination_path=destination_path
        )
        convert_mp4_to_mp3(videos=videos, destination_path=destination_path)
        remove_videos(dir_videos=videos)
