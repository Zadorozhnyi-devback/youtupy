from typing import Union, Type, TYPE_CHECKING

from backend.handlers.for_data import get_listdir
from ui_tkinter.const import TYPE_TO_METHOD_TABLE

if TYPE_CHECKING:
    from pytube import Playlist, YouTube


__all__ = (
    'init_load_object_attempt',
    'validate_object',
    'validate_already_loaded'
)


def init_load_object_attempt(
    cls: Type[Union['YouTube', 'Playlist']],
    url: str
) -> None:
    """ init object and call some its method to catch errors """
    obj = cls(url=url)
    getattr(obj, 'title')


def validate_object(
    load_object: Union['Playlist', 'YouTube'], download_type: str
) -> bool:
    try:
        return bool(getattr(load_object, TYPE_TO_METHOD_TABLE[download_type]))
    except KeyError:
        return False


def validate_already_loaded(path: str, object_title: str) -> bool:
    try:
        dir_files = get_listdir(path=path)
        if object_title in dir_files:
            return False
    except FileNotFoundError:
        pass
    return True
