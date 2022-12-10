from tkinter import Entry


__all__ = 'EntriesMixin',


class EntriesMixin:
    def _get_input_url(self) -> Entry:
        input_url = Entry(master=self._window, width=30)  # noqa
        input_url.grid(column=0, row=5, sticky='WE')
        input_url.focus()
        return input_url
