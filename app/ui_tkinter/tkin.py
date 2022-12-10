import getpass

from ui_tkinter.const import MAIN_CANVAS_KWARGS, INPUT_CANVAS_KWARGS
from ui_tkinter.mixins import (
    ButtonsMixin,
    CacherMixin,
    ClickedMixin,
    DownloaderMixin,
    EntriesMixin,
    EventsMixin,
    LabelsMixin,
    PopupsMixin,
    ProgressBarMixin,
    RadioButtonsMixin,
    WindowsMixin
)
from ui_tkinter.validators import YouTupyValidator


__all__ = 'YouTupy',


class YouTupy(
    ButtonsMixin,
    CacherMixin,
    ClickedMixin,
    DownloaderMixin,
    EntriesMixin,
    EventsMixin,
    LabelsMixin,
    PopupsMixin,
    ProgressBarMixin,
    RadioButtonsMixin,
    WindowsMixin,
    YouTupyValidator
):

    def __init__(self, entry_point_path: str) -> None:
        self._entry_point_path = entry_point_path

        self._window = self._get_window()

        self._create_extension_radiobuttons()
        self._create_download_type_radiobuttons()

        self._main_canvas = self._get_canvas(kw=MAIN_CANVAS_KWARGS)
        self._input_canvas = self._get_canvas(kw=INPUT_CANVAS_KWARGS)

        self._download_button = self._get_download_button()

        self._input_url = self._get_input_url()

        self._destination_path = self._get_default_download_path()
        self._destination_button = self._get_destination_button()

        self._create_empty_strings(rows=[7])

        self._window.mainloop()

    def _get_default_download_path(self) -> str:
        cache = self._get_cache()

        path = (
            cache.get('download_path')
            or f'/Users/{getpass.getuser()}/downloads/youtupy'
        )

        return path
