from urllib.error import URLError

from pytube.exceptions import RegexMatchError

from backend.handlers.for_data import (
    get_clean_title,
    get_path_to_playlist
)
from backend.validators import (
    validate_object,
    validate_already_loaded,
    init_load_object_attempt
)
from ui_tkinter.const import (
    MAIN_CANVAS_TEXT,
    EMPTY_PLAYLIST,
    TYPE_TO_CLASS_TABLE
)


__all__ = 'YouTupyValidator',


class YouTupyValidator:
    def _validate_playlist(self) -> bool:
        # подвисаем здесь
        download_type = self._selected_download_type.get()  # noqa
        if validate_object(
            load_object=self._download_object,  # noqa
            download_type=download_type
        ):
            object_title = self._download_object.title  # noqa
            object_title = get_clean_title(title=object_title)
            path = get_path_to_playlist(
                playlist_title=object_title,
                playlist_path=self._destination_path  # noqa
            )
            extension = self._selected_extension.get()  # noqa
            if validate_already_loaded(
                [self._input_url.get(), path, download_type, extension]  # noqa
            ):
                return True
            else:
                answer = self._object_exists_msg_box()  # noqa
                if answer is True:
                    return True
                else:
                    self._change_text_canvas(text=MAIN_CANVAS_TEXT)  # noqa

        else:
            self._change_text_canvas(text=EMPTY_PLAYLIST)  # noqa

    def _validate_video(self) -> bool:
        path = self._destination_path  # noqa
        download_type = self._selected_download_type.get()  # noqa
        extension = self._selected_extension.get()  # noqa
        if validate_already_loaded(
            [self._input_url.get(), path, download_type, extension]  # noqa
        ):
            return True
        else:
            answer = self._object_exists_msg_box()  # noqa
            if answer is True:
                return True
            else:
                self._change_text_canvas(text=MAIN_CANVAS_TEXT)  # noqa

    def _validate_args(self, download_type: str) -> bool:
        try:
            init_load_object_attempt(
                input_url=self._input_url.get(),  # noqa
                download_class=(
                    TYPE_TO_CLASS_TABLE[self._selected_download_type.get()]  # noqa
                )
            )
            self._create_main_process_vars(download_type=download_type)  # noqa
        except (KeyError, URLError, RegexMatchError):
            self._change_text_canvas(  # noqa
                text=f'invalid link for {self._selected_download_type.get()}'  # noqa
            )
            return False
        return (
            getattr(self, f'_validate_{self._selected_download_type.get()}')()  # noqa
        )
