import os
from multiprocessing import Process
from time import sleep

from pytube import YouTube, Playlist

from backend.handlers.for_data import (
    get_download_object,
    download_object,
    get_clean_title
)
from ui_tkinter.const import TYPE_TO_CLASS_TABLE


__all__ = 'DownloaderMixin',


class DownloaderMixin:
    def _main_download(self) -> None:
        download_type = self._selected_download_type.get()  # noqa
        if self._validate_args(download_type=download_type):  # noqa
            extension = self._selected_extension.get()  # noqa

            message = self._get_main_canvas_text(download_type, extension)
            self._change_text_canvas(text=message)  # noqa

            func = f'download_{download_type}'

            object_title = get_clean_title(title=self._download_object.title)
            path = self.get_or_create_path(object_title)

            self._download_button.grid_remove()  # noqa
            self._cancel_loading_button.grid()  # noqa

            self._main_process = Process(
                target=download_object,
                args=(self._download_object, path, extension, func)
            )
            self._main_process.start()
            print("main process started")
            self._create_progressbar()  # noqa
            self._progressbar.tkraise()  # noqa
            self._run_progressbar()  # noqa
            self._schedule_check(ms=1000)

    def _get_main_canvas_text(self, download_type: str, extension: str) -> str:
        if download_type == 'video':
            if extension == '.mp3':
                message = 'loading audio...'
            else:
                message = 'loading video...'

        else:
            message = f'loading playlist ({self._download_object.length})...'

        return message

    def get_or_create_path(self, object_title) -> str:
        path = (
            self._destination_path  # noqa
            if isinstance(self._download_object, YouTube)
            else f'{self._destination_path}/{object_title}'  # noqa
        )
        os.makedirs(path, exist_ok=True)
        return path

    def _create_main_process_vars(self, download_type: str) -> None:
        input_url = self._input_url.get()  # noqa
        class_name = TYPE_TO_CLASS_TABLE[download_type]
        self._download_object = get_download_object(
            class_name=class_name, url=input_url
        )
        self._download_class = (
            Playlist if download_type == 'playlist' else YouTube
        )

    def _schedule_check(
        self, ms: int, func_name: str = '_schedule_check'
    ) -> None:
        """
        Planning to call '_check_process_done()' after 'ms' * 1000 seconds
        """
        func = self._check_process_done
        self._window.after(ms, func, ms, func_name)  # noqa

    def _check_process_done(self, ms: int, func_name: str) -> None:
        if self._main_process.is_alive():
            getattr(self, func_name)(ms=ms, func_name=func_name)
        else:  # If thread is done display message, switch button, finish bar
            if self._progressbar.winfo_exists():  # noqa
                # костыль для добивания прогрессбара
                while self._progressbar['value'] < 100:  # noqa
                    self._increment_progressbar()  # noqa
                    sleep(0.2)
                self._progressbar.destroy()  # noqa
                self._change_text_canvas(text='done!')  # noqa
            else:
                self._change_text_canvas(text='canceled!')  # noqa

            self._switch_download_and_cancel_button()  # noqa
