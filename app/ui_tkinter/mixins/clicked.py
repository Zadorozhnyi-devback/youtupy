import getpass
import os.path
from pathlib import Path
import shutil
from tkinter import filedialog, messagebox

from backend.handlers.for_data import get_clean_title
from ui_tkinter.const import CURR_PATH


__all__ = 'ClickedMixin',


class ClickedMixin:
    def _clicked_run_youtupy(self) -> None:
        print('clicked!')
        self._main_download()  # noqa

    def _clicked_cancel_loading(self) -> None:
        answer = messagebox.askyesno(message='cancel loading?')
        if answer:
            self._main_process.terminate()  # noqa
            self._progressbar.destroy()  # noqa

            object_title = get_clean_title(title=self._download_object.title)  # noqa
            path = self.get_or_create_path(object_title)  # noqa

            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    def _clicked_choose_dir(self) -> None:
        directory = filedialog.askdirectory(
            # gonna work on mac, have to check for windows and linux
            # initialdir=os.path.normpath("C://") try on Windows
            parent=self._window,  # noqa
            initialdir=f'/Users/{getpass.getuser()}/'
        )
        if directory:
            full_path = str(Path(directory).resolve())
            self._destination_path = full_path

            self._add_path_in_cache(full_path)  # noqa

        self._curr_path_label.configure(  # noqa
            text=f'{CURR_PATH}: {self._destination_path}'
        )
