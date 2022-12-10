from tkinter import Event, messagebox, Tk

__all__ = 'EventsMixin',


class EventsMixin:
    def _closer(self, _: Event) -> None:
        answer = messagebox.askyesno(message=f'close youtupy?')
        if answer is True:
            self._window.destroy()  # noqa
        else:
            self._input_url.focus_force()  # noqa

    def _set_exit_cross_signal(self, frame: Tk) -> None:
        frame.protocol('WM_DELETE_WINDOW', lambda: self._closer(Event()))
