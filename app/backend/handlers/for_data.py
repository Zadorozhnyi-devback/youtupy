import os
import subprocess
import sys
from pathlib import Path
from typing import List, Union
from urllib.error import URLError

from pytube import Playlist, YouTube
import pytube

from backend.const import VID_NAME, RETRY_AMOUNT
from ui_tkinter.const import UNWISHED_NAME_PARTS


def get_download_object(class_name: str, url: str) -> Union[Playlist, YouTube]:
    obj = getattr(pytube, class_name)(url=url)
    return obj


def get_path_to_playlist(playlist_title: str, playlist_path: str) -> str:
    path = str(Path(f'{playlist_path}/{playlist_title}').resolve())
    return path


def get_dir_mp4_files(path_to_dir: str) -> List[Path]:
    videos = [file for file in Path(path_to_dir).glob('*.mp4')]
    return videos


def get_listdir(path: str) -> List[str]:
    dirs = os.listdir(path=path)
    return dirs


def convert_mp4_to_mp3(video_titles: List[str], destination_path: str) -> None:
    print('titles', video_titles)
    for video in video_titles:
        old_title = f'{destination_path}/{video}'
        new_title = f"{destination_path}/{video.split('.mp4')[VID_NAME]}.mp3"
        print('new', new_title)
        print('dest', destination_path)
        subprocess.call(['ffmpeg', '-i', old_title, new_title])


def remove_videos(dir_videos: List[str], destination_path: str) -> None:
    for video in dir_videos:
        path = f'{destination_path}/{video}'
        os.remove(path=path)


def get_clean_title(title: str) -> str:
    title_lower = title.lower()
    unwished = [part for part in UNWISHED_NAME_PARTS if part in title_lower]
    for part in unwished:
        index = title_lower.find(part)
        first_couple = title[:index]
        second_couple = title[index + len(part):]
        title = f'{first_couple.strip()}{second_couple.strip()}'
    return title


def download_playlist(playlist: Playlist, path_to_playlist: str) -> None:
    for video in playlist.videos:
        title = get_clean_title(title=video.title)
        video.streams.filter(
            only_audio=True
        ).get_audio_only().download(
            output_path=path_to_playlist, filename=f'{title}.mp4'
        )


def download_video(video: YouTube, path: str) -> None:
    # сделать выпадашку с выбором качества видео
    title = f'{get_clean_title(title=video.title)}.mp4'
    video.streams.filter(
        file_extension='mp4',
    ).get_highest_resolution().download(
        output_path=path, filename=title
    )


def try_download(
    process_func: str, args: List[Union[Playlist, YouTube]]
) -> bool:
    for _ in range(RETRY_AMOUNT):
        try:
            module_name = sys.modules[__name__]
            getattr(module_name, process_func)(*args)
            return True
        except URLError:
            continue


def get_needed_videos(
    download_type_object: Union[Playlist, YouTube], destination_path: str
) -> List[Path]:
    if isinstance(download_type_object, Playlist):
        videos = get_dir_mp4_files(path_to_dir=destination_path)
    else:
        object_title = get_clean_title(
            title=f'{download_type_object.title}.mp4'
        )
        videos = [
            video for video in
            Path(destination_path).glob(object_title)
            if video
        ]
    print('videossss', videos)
    return videos


def check_and_download(
    download_type_object: Union[Playlist, YouTube],
    path: str, selected_extension: str, process_func: str
) -> None:
    download_complete = try_download(
        process_func=process_func,
        args=[download_type_object, path]
    )
    if download_complete and selected_extension == '.mp3':
        videos = get_needed_videos(
            download_type_object=download_type_object,
            destination_path=path
        )
        video_titles = [
            get_clean_title(title=video.name) for video in videos
        ]
        convert_mp4_to_mp3(video_titles=video_titles, destination_path=path)
        remove_videos(dir_videos=video_titles, destination_path=path)
