import os
from pathlib import Path
from typing import List, Union, Type
from urllib.error import URLError

from pytube import Playlist, YouTube

from backend.handlers.for_validation import (
    make_dirs, remove_old_dirs, chdir_if_path_not_default
)
from backend.const import PLAYLIST_PATH, PLAYLIST_URL, DEFAULT_PLAYLIST_PATH


def validate_path_existing(playlist_path: Path) -> None:
    try:
        chdir_if_path_not_default(playlist_path=playlist_path)
        os.listdir(playlist_path)
    except FileNotFoundError:
        make_dirs(playlist_path=playlist_path)
    except NotADirectoryError:
        remove_old_dirs(playlist_path=playlist_path)
        make_dirs(playlist_path=playlist_path)


def validate_internet_connection(
    input_url: str, needed_class: Type[Union[Playlist, YouTube]]
) -> bool:
    try:
        obj = getattr(needed_class, '__init__')
        setattr(obj, 'url', input_url)
        return True
    except URLError:
        return False


def validate_playlist_existing(playlist: Playlist) -> bool:
    try:
        if not playlist.videos:
            return False
        return True
    except KeyError:
        return False


def get_listdir(playlist_path: Path) -> List[str]:
    chdir_if_path_not_default(playlist_path=playlist_path)
    dirs = os.listdir(path=playlist_path)
    return dirs


def validate_playlist_loaded(args: List[Union[Path, str]]) -> bool:
    playlist = Playlist(url=args[PLAYLIST_URL])
    playlist_path = (
        args[PLAYLIST_PATH] if len(args) > 1 else DEFAULT_PLAYLIST_PATH
    )
    try:
        dirs = get_listdir(playlist_path=playlist_path)
        if playlist.title in dirs:
            return False
    except FileNotFoundError:
        make_dirs(playlist_path=playlist_path)
    return True
