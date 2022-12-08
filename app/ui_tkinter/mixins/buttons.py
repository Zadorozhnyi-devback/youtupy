from tkinter import Button


__all__ = 'ButtonsMixin',


class ButtonsMixin:
    def _get_download_button(self) -> Button:
        button = Button(
            master=self._window, text='download', width='10',  # noqa
            fg='red', command=lambda: self._clicked_run_youtupy()  # noqa
        )
        button.grid(column=6, row=5, sticky='W')
        return button

    def _get_destination_button(self) -> Button:
        button = Button(
            master=self._window, text='choose folder', width='12',  # noqa
            fg='red', command=self._clicked_choose_dir  # noqa
        )
        button.grid(column=0, row=11, sticky='W')

        self._get_curr_path_label()  # noqa
        return button
