from tkinter import messagebox

from pytube import YouTube

from backend.handlers.for_data import (
    get_clean_title,
    remove_file,
    remove_dir
)


__all__ = 'PopupsMixin',


class PopupsMixin:
    def _object_exists_msg_box(self) -> bool:
        object_type = self._selected_download_type.get()  # noqa
        load_object = self._download_object  # noqa
        object_name = get_clean_title(title=load_object.title)
        extension = self._selected_extension.get()  # noqa
        extension = (
            extension if object_type == 'video' else f' ({extension})'
        )
        object_type = (
            'audio' if object_type == 'video' and extension == '.mp3'
            else object_type
        )
        path = self._destination_path  # noqa
        path = (
            f'{path}/{object_name}{extension}'
            if isinstance(load_object, YouTube)
            else f'{path}/{object_name}'
        )
        answer = messagebox.askyesno(
            message=f'override {object_type}?\n\n{object_name}{extension}'
        )
        if answer:
            if object_type in ('video', 'audio'):
                remove_file(path=path)
            else:
                remove_dir(path=path)

        self._input_url.focus_force()  # noqa
        return answer
