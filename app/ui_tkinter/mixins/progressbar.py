from tkinter.ttk import Progressbar

from ui_tkinter.const import STEPS_AMOUNT, AVERAGE_DOWNLOAD_TIME


__all__ = 'ProgressBarMixin',


class ProgressBarMixin:
    def _increment_progressbar(self) -> None:
        self._progressbar['value'] += 5
        self._window.update()  # noqa

    def _update_progressbar(self, ms: int) -> None:
        if self._progressbar.winfo_exists():
            self._increment_progressbar()
            if self._progressbar['value'] == 95:
                self._change_text_canvas(text='almost done...')  # noqa
                return
            func = self._update_progressbar
            self._window.after(ms, func, ms)  # noqa

    def _run_progressbar(self) -> None:
        self._progressbar['value'] = 0
        videos_amount = 1
        if self._selected_download_type.get() == 'playlist':  # noqa
            videos_amount = self._download_object.length  # noqa

        ms = int(videos_amount * AVERAGE_DOWNLOAD_TIME / STEPS_AMOUNT * 1000)

        self._update_progressbar(ms=ms)

    def _create_progressbar(self) -> None:
        self._progressbar = Progressbar(
            master=self._window, mode='determinate',  # noqa
            orient='horizontal', length=236
        )
        self._progressbar.grid(column=0, row=0, padx=(5, 0))
