from typing import List, Union

from pytube import Playlist, YouTube
import pytube

from backend.handlers.for_data import get_listdir, get_download_object
from backend.const import DOWNLOAD_TYPE, DESTINATION_PATH, INPUT_URL, EXTENSION
from ui_tkinter.const import (
    DOWNLOAD_CLASS_METHOD, TYPE_TO_CLASS_TABLE, TYPE_TO_METHOD_TABLE
)


def init_load_object_attempt(input_url: str, download_class: str) -> None:
    # just try to init object and call some its method to catch errors
    obj = getattr(pytube, download_class)(url=input_url)
    my_method = DOWNLOAD_CLASS_METHOD[download_class]
    getattr(obj, my_method)


def validate_object(
    load_object: Union[Playlist, YouTube], download_type: str
) -> bool:
    try:
        if not (getattr(load_object, TYPE_TO_METHOD_TABLE[download_type])):
            return False
        return True
    except KeyError:
        return False


def validate_already_loaded(args: List[str]) -> bool:
    loading_object = args[DOWNLOAD_TYPE]
    class_name = TYPE_TO_CLASS_TABLE[loading_object]
    url = args[INPUT_URL]
    path_to_object = args[DESTINATION_PATH]

    object_name = get_download_object(class_name=class_name, url=url).title
    without_object_name = -len(object_name)

    if loading_object != 'video':
        path_to_object = path_to_object[:without_object_name]
    else:
        object_name = f'{object_name}{args[EXTENSION]}'

    try:
        dir_files = get_listdir(path=path_to_object)
        if object_name in dir_files:
            return False
    except FileNotFoundError:
        pass
    return True
