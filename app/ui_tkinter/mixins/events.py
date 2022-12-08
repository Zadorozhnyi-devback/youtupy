from tkinter import Event


__all__ = 'EventsMixin',


class EventsMixin:
    def _closer(self, _: Event) -> None:
        self._window.destroy()  # noqa
