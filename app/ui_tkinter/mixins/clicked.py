import getpass
import os
from pathlib import Path
from tkinter import filedialog, messagebox

from backend.handlers.for_data import remove_dir, remove_file
from ui_tkinter.const import CURR_PATH


__all__ = 'ClickedMixin',


class ClickedMixin:
    def _clicked_run_youtupy(self) -> None:
        print('clicked!')
        self._main_download()  # noqa

    def _clicked_cancel_loading(self) -> None:
        answer = messagebox.askyesno(message='cancel loading?')
        if answer is True:
            self._main_process.terminate()  # noqa
            self._progressbar.destroy()  # noqa

            if os.path.isdir(self._download_object_path):  # noqa
                remove_dir(path=self._download_object_path)  # noqa
            else:
                remove_file(path=self._download_object_path)  # noqa

    def _clicked_choose_dir(self) -> None:
        directory = filedialog.askdirectory(
            # gonna work on mac, have to check for windows and linux
            # initialdir=os.path.normpath("C://") try on Windows
            parent=self._window,  # noqa
            initialdir=f'/Users/{getpass.getuser()}/'
        )
        if directory:
            self._download_path = str(Path(directory).resolve())

            self._add_path_in_cache(self._download_path)  # noqa

        self._curr_path_label.configure(  # noqa
            text=f'{CURR_PATH}: {self._download_path}'
        )
