from tkinter import Frame, StringVar
from tkinter.ttk import Radiobutton


__all__ = 'RadioButtonsMixin',


class RadioButtonsMixin:
    def _create_extension_radiobuttons(self) -> None:
        self._radio_frame = Frame(master=self._window)  # noqa
        self._radio_frame.grid(column=0, row=3, padx=(10, 1))
        # default
        self._selected_extension = StringVar(master=self._window, value='.mp3')  # noqa
        radiobutton_mp3 = Radiobutton(
            master=self._radio_frame, text='mp3', value='.mp3',
            variable=self._selected_extension
        )
        radiobutton_mp4 = Radiobutton(
            master=self._radio_frame, text='mp4', value='.mp4',
            variable=self._selected_extension
        )
        radiobutton_mp3.grid(column=0, row=0)
        radiobutton_mp4.grid(column=1, row=0)

    def _create_download_type_radiobuttons(self) -> None:
        self._selected_download_type = StringVar(
            master=self._window, value='playlist'  # noqa
        )
        radiobutton_playlist = Radiobutton(
            master=self._radio_frame, text='playlist', value='playlist',
            variable=self._selected_download_type
        )
        radiobutton_video = Radiobutton(
            master=self._radio_frame, text='video', value='video',
            variable=self._selected_download_type
        )
        radiobutton_playlist.grid(column=2, row=0, padx=(10, 0))
        radiobutton_video.grid(column=3, row=0)
