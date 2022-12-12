import os
from multiprocessing import Process
from time import sleep

from pytube import YouTube, Playlist

from backend.handlers.audio import YoutubeAudioDownloader
from backend.handlers.for_data import (
    get_download_object,
    download_object,
    get_clean_title
)


__all__ = 'DownloaderMixin',


class DownloaderMixin:
    def _main_download(self) -> None:
        self._download_type = self._selected_download_type.get()  # noqa
        self._download_class = (
            Playlist if self._download_type == 'playlist' else YouTube
        )
        if self._validate_args():  # noqa
            text = self._get_main_canvas_loading_text()
            self._change_text_canvas(text=text)  # noqa

            self._switch_download_and_cancel_button()  # noqa

            func = f'download_{self._download_type}'

            load_path = self.get_load_path()

            self._main_process = Process(
                target=download_object,
                args=(
                    self._download_object,
                    load_path,
                    self._extension,
                    func
                )
            )
            self._main_process.start()
            print("main process started")
            self._create_progressbar()  # noqa
            self._progressbar.tkraise()  # noqa
            self._run_progressbar()  # noqa
            self._schedule_check(ms=1000)

    def get_load_path(self) -> str:
        """
        Return path: str where to load audio/video

            * For playlist including playlist dir
        """
        path = (
            self._download_path  # noqa
            if self._download_class is YouTube
            else f'{self._download_path}/{self._download_object_title}'  # noqa
        )
        os.makedirs(path, exist_ok=True)
        return path

    def _get_main_canvas_loading_text(self) -> str:
        if self._download_type == 'video':
            if self._extension == '.mp3':
                text = 'loading audio...'
            else:
                text = 'loading video...'

        else:
            text = f'loading playlist ({self._download_object.length})...'

        return text

    def _create_main_process_vars(self) -> None:
        self._extension = self._selected_extension.get()  # noqa
        self._download_object = get_download_object(
            cls=self._download_class,
            url=self._input_url.get()  # noqa
        )

        if self._download_type == 'playlist':
            object_title = get_clean_title(title=self._download_object.title)  # noqa
        else:
            mp3_loader = YoutubeAudioDownloader(
                urls=[self._download_object.watch_url],  # noqa
                download_path=self._download_path  # noqa
            )
            object_title = f'{mp3_loader.get_title()}{self._extension}'

        self._download_object_title = object_title
        self._download_object_path = (
            f'{self._download_path}/{self._download_object_title}'  # noqa
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
        else:
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
