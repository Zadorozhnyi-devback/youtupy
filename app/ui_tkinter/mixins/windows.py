from tkinter import Tk, PhotoImage
from tkinter.ttk import Style

from ui_tkinter.const import WINDOW_TITLE, WINDOW_SIZE


__all__ = 'WindowsMixin',


class WindowsMixin:
    def _get_window(self) -> Tk:
        window = Tk()

        # binds
        window.bind('<Escape>', lambda _: self._closer(_))  # noqa
        # window.bind('<Enter>', lambda _: self._clicked_run_youtupy())

        self._set_exit_cross_signal(frame=window)  # noqa

        style = Style(master=window)
        style.theme_use('aqua')

        icon = f'{self._entry_point_path}/static/jordan.png'  # noqa
        window.iconphoto(True, PhotoImage(file=icon))
        window.title(WINDOW_TITLE)
        window.geometry(WINDOW_SIZE)
        return window
