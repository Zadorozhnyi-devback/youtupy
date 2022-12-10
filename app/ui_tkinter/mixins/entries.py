from tkinter import Entry


__all__ = 'EntriesMixin',


class EntriesMixin:
    def _get_input_url(self) -> Entry:
        input_url = Entry(master=self._window, width=26)  # noqa
        input_url.grid(column=0, row=5, sticky='WE', padx=10)
        input_url.focus()
        return input_url
