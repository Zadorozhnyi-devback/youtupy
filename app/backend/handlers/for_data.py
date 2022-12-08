import os
import shutil
import sys
from pathlib import Path
from typing import List, Union
from urllib.error import URLError

from pytube import Playlist, YouTube
from pytube.exceptions import AgeRestrictedError
import pytube

from backend.handlers.audio import YoutubeAudioDownloader
from ui_tkinter.const import UNWISHED_NAME_PARTS


__all__ = (
    'get_download_object',
    'get_path_to_playlist',
    'clean_na_from_mp3',
    'get_clean_title',
    'download_object',
    'download_video',
    'download_playlist',
    'get_listdir',
    'remove_dir',
    'remove_file'
)


def get_download_object(class_name: str, url: str) -> Union[Playlist, YouTube]:
    obj = getattr(pytube, class_name)(url=url)
    return obj


def get_path_to_playlist(playlist_title: str, playlist_path: str) -> str:
    path = str(Path(f'{playlist_path}/{playlist_title}').resolve())
    return path


def clean_na_from_mp3(path: str) -> None:
    files = [
        str(file) for file in
        Path(path).glob('*.mp3')
        if str(file).split('.mp3')[0].endswith(' - NA')
    ]
    for f in files:
        extension = f.rsplit('.')[-1]
        file_name = f.rsplit(' - NA')[0]
        os.rename(f, f'{file_name}.{extension}')


def get_clean_title(title: str) -> str:
    title_lower = title.lower()
    unwished = [
        part.lower() for part
        in UNWISHED_NAME_PARTS
        if part.lower() in title_lower
    ]
    for part in unwished:
        index = title_lower.find(part)
        first_couple = title[:index]
        second_couple = title[index + len(part):]
        title = f'{first_couple.strip()}{second_couple.strip()}'
    title = title.replace('/', ' ')  # to prevent name like 7/11
    return title


def download_object(
    download_type_object: Union[Playlist, YouTube],
    path: str, selected_extension: str, process_func: str
) -> None:
    print('steady, go!')

    module_name = sys.modules[__name__]
    args = [download_type_object, path, selected_extension]
    getattr(module_name, process_func)(*args)

    clean_na_from_mp3(path)

    print('complete')


def download_video(
    video: YouTube,
    path: str,
    selected_extension: str
) -> None:
    if selected_extension == '.mp3':
        loader = YoutubeAudioDownloader(
            urls=[video.watch_url],
            download_path=path
        )
        loader.run()
    else:
        # сделать выпадашку с выбором качества видео
        title = f'{get_clean_title(title=video.title)}.mp4'
        video.streams.filter(
            file_extension='mp4',
        ).get_highest_resolution().download(
            output_path=path, filename=title
        )


def download_playlist(
    playlist: Playlist,
    path_to_playlist: str,
    selected_extension: str
) -> None:
    if selected_extension == '.mp3':
        loader = YoutubeAudioDownloader(
            urls=list(playlist.video_urls),
            download_path=path_to_playlist
        )
        loader.run()
    else:
        not_loaded = list()
        for video in playlist.videos:
            try:
                download_video(
                    video=video,
                    path=path_to_playlist,
                    selected_extension=selected_extension
                )
            except URLError:
                not_loaded.append(video)
                continue
            except (AgeRestrictedError, KeyError):
                continue
        for video in not_loaded:
            try:
                download_video(
                    video=video,
                    path=path_to_playlist,
                    selected_extension=selected_extension
                )
            except URLError:
                continue


def get_listdir(path: str) -> List[str]:
    dirs = os.listdir(path=path)
    return dirs


def remove_dir(path: str) -> None:
    shutil.rmtree(path=path)


def remove_file(path: str) -> None:
    os.remove(path=path)
