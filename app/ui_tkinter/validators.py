from urllib.error import URLError

from pytube.exceptions import RegexMatchError, PytubeError

from backend.validators import (
    validate_object,
    validate_already_loaded,
    init_load_object_attempt
)
from ui_tkinter.const import (
    MAIN_CANVAS_TEXT,
    INVALID_URL_ERROR
)


__all__ = 'YouTupyValidator',


class YouTupyValidator:
    def _validate_args(self) -> bool:
        try:
            init_load_object_attempt(
                cls=self._download_class,  # noqa
                url=self._input_url.get(),  # noqa
            )
            self._create_main_process_vars()  # noqa
        except URLError:
            self._change_text_canvas('no Internet connection')  # noqa
            return False
        except (KeyError, RegexMatchError):
            self._change_text_canvas(  # noqa
                text=f'invalid link for {self._download_type}'  # noqa
            )
            return False
        except PytubeError:
            self._change_text_canvas('pytube error')  # noqa
            return False
        return getattr(self, f'_validate_{self._download_type}')()  # noqa

    def _validate_playlist(self) -> bool:
        # подвисаем здесь
        if validate_object(
            load_object=self._download_object,  # noqa
            download_type=self._download_type  # noqa
        ):
            if validate_already_loaded(
                path=self._download_path,  # noqa
                object_title=self._download_object_title  # noqa
            ):
                return True
            else:
                answer = self._object_exists_msg_box()  # noqa
                if answer is True:
                    return True
                else:
                    self._change_text_canvas(text=MAIN_CANVAS_TEXT)  # noqa

        else:
            self._change_text_canvas(text=INVALID_URL_ERROR)  # noqa

    def _validate_video(self) -> bool:
        if validate_already_loaded(
            path=self._download_path,  # noqa
            object_title=self._download_object_title  # noqa
        ):
            return True
        else:
            answer = self._object_exists_msg_box()  # noqa
            if answer is True:
                return True
            else:
                self._change_text_canvas(text=MAIN_CANVAS_TEXT)  # noqa
