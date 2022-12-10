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

    def _get_cancel_loading_button(self) -> Button:
        button = Button(
            master=self._window, text='cancel', width='10',  # noqa
            fg='red', command=lambda: self._clicked_cancel_loading()  # noqa
        )
        button.grid(column=6, row=5, sticky='W')
        return button

    def _get_destination_button(self) -> Button:
        button = Button(
            master=self._window, text='choose folder', width='12',  # noqa
            fg='red', command=self._clicked_choose_dir  # noqa
        )
        button.grid(column=0, row=11, padx=10, sticky='W')

        self._get_curr_path_label()  # noqa
        return button

    def _switch_download_and_cancel_button(self) -> None:
        if self._download_button.grid_info():  # noqa
            self._download_button.grid_remove()  # noqa
            self._cancel_loading_button.grid()  # noqa
        else:
            self._cancel_loading_button.grid_remove()  # noqa
            self._download_button.grid()  # noqa
