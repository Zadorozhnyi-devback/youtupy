from typing import List, Union

from pytube import Playlist
import pytube

from backend.handlers.for_data import get_listdir
from backend.const import PLAYLIST_PATH, PLAYLIST_URL
from ui_tkinter.const import DOWNLOAD_CLASS_METHOD


def init_load_object_attempt(input_url: str, download_class: str) -> None:
    obj = getattr(pytube, download_class)(url=input_url)
    my_method = DOWNLOAD_CLASS_METHOD[download_class]
    getattr(obj, my_method)


def validate_playlist_existing(playlist: Playlist) -> bool:
    try:
        if not playlist.videos:
            return False
        return True
    except KeyError:
        return False


def validate_playlist_loaded(args: List[Union[str, str]]) -> bool:
    # переделать, чтобы првоерял все
    playlist = Playlist(url=args[PLAYLIST_URL])
    playlist_path = args[PLAYLIST_PATH][:-len(playlist.title)]
    try:
        dir_files = get_listdir(path=playlist_path)
        if playlist.title in dir_files:
            return False
    except FileNotFoundError:
        pass
    return True
