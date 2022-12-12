from tkinter import messagebox

from backend.handlers.for_data import (
    remove_file,
    remove_dir
)


__all__ = 'PopupsMixin',


class PopupsMixin:
    def _object_exists_msg_box(self) -> bool:
        object_type = (
            'audio'
            if self._download_type == 'video' and self._extension == '.mp3'  # noqa
            else self._download_type  # noqa
        )

        extension_tip = (
            f'({self._extension})' if self._download_type == 'playlist' else ''  # noqa
        )

        answer = messagebox.askyesno(
            message=(
                f'override {object_type}?'
                f'\n\n{self._download_object_title} {extension_tip}'  # noqa
            )
        )
        if answer is True:
            if object_type in ('video', 'audio'):
                remove_file(path=self._download_object_path)  # noqa
            else:
                remove_dir(path=self._download_object_path)  # noqa

        self._input_url.focus_force()  # noqa
        return answer
