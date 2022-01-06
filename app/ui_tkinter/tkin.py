from multiprocessing import Process
from tkinter import Tk, Label, Button, Entry, ttk, Frame, filedialog
# from tkinter.ttk import Progressbar, Style
from tkinter.ttk import Style
from typing import List

from backend.const import PLAYLIST_URL, DESTINATION_PATH, DEFAULT_DIR_PATH
from backend.handlers.data_handlers import (
    get_playlist, get_dir_path, download_videos
)
from backend.validators import (
    validate_path_existing, validate_playlist_loaded,
    validate_playlist_existing
)
from ui_tkinter.const import (
    MY_LABEL, DIR_EXISTS, EMPTY_PLAYLIST, MY_FONT,
    YOUTUBE_MUSIC, NEED_YOUTUBE_MUSIC, WINDOW_SIZE, WINDOW_TITLE
)
from ui_tkinter.handlers import _progressbar_process


class YouTupy:
    def __init__(self) -> None:
        self._window = self._get_window()
        self._label = self._get_label()
        self._download_button = self._get_download_button()
        self._playlist_url = self._get_playlist_url()
        self._destination_button = self._get_destination_button()
        self._destination_dir = DEFAULT_DIR_PATH
        self._window.mainloop()

    def _clicked_choose_dir(self):
        self._window.directory = filedialog.askdirectory()
        self._destination_dir = self._window.directory

    def _get_destination_button(self) -> Button:
        button = Button(
            master=self._window, text='choose folder', width='15',
            fg='red', command=self._clicked_choose_dir
        )
        button.grid(column=1, row=3)
        return button

    def _run_progressbar(self) -> None:
        playlist_length = self._playlist.length
        self._progressbar['value'] = 0
        ms = playlist_length * 15 // 20 * 1000
        process = Process(
            target=_progressbar_process, args=(playlist_length,)
        )
        process.start()
        self._update_progressbar(ms, process)

    def _update_progressbar(
        self, ms: int, process: Process,
        func_name: str = '_update_progressbar'
    ) -> None:
        if self._progressbar['value'] == 95:
            process.terminate()
            self._label.configure(text='almost done...')
            return
        self._progressbar['value'] += 5
        func = self._check_process_done
        self._window.after(ms, func, ms, process, func_name)

    def _create_progressbar(self) -> None:
        style = Style()
        style.theme_use('default')
        style.configure("black.Horizontal.TProgressbar", background='black')
        progress_frame = Frame(self._window)
        progress_frame.grid(
            column=1, row=0, columnspan=2, padx=10, pady=20
        )
        self._progressbar = ttk.Progressbar(
            master=progress_frame, mode="determinate", orient='horizontal',
            length=200, style='black.Horizontal.TProgressbar'
        )
        self._progressbar.grid(
            column=1, row=0, columnspan=2, padx=10, pady=20
        )
        blank = Frame(progress_frame)
        blank.grid(
            column=1, row=0, columnspan=2, padx=10, pady=20, sticky='nsew'
        )

    def _schedule_check(
        self, ms: int, process: Process, func_name: str = '_schedule_check'
    ) -> None:
        """
        Planning to call
            '_check_process_done()'
            or some func
            during 'ms' // 1000 seconds
        """
        func = self._check_process_done
        self._window.after(ms, func, ms, process, func_name)

    def _check_process_done(
            self, ms: int, process: Process, func_name: str
    ) -> None:
        # If thread is done display message and activate button
        if not process.is_alive():
            self._label.configure(text='done!')
            # Reset button
            self._download_button['state'] = 'normal'
            # Hide bar
            self._progressbar.lower()
        else:
            # If not, gonna check after ms * 1000 sec
            getattr(self, func_name)(
                ms=ms, process=process, func_name=func_name
            )

    def _validate_args(self) -> bool:
        if not self._playlist_url.get().startswith(YOUTUBE_MUSIC):
            self._label.configure(text=NEED_YOUTUBE_MUSIC)
        if len(self._args) > 1:
            validate_path_existing(dir_path=self._args[DESTINATION_PATH])
        if validate_playlist_existing(playlist_url=self._args[PLAYLIST_URL]):
            if validate_playlist_loaded(args=self._args):
                return True
            else:
                self._label.configure(
                    text=f'{self._playlist.title}{DIR_EXISTS}'
                )

        else:
            self._label.configure(text=EMPTY_PLAYLIST)

    def _get_args(self) -> List[str]:
        args = [self._playlist_url.get(), self._destination_dir]
        args = [arg for arg in args if arg]
        return args

    def _main_process(self) -> None:
        self._args = self._get_args()
        self._playlist = get_playlist(playlist_url=self._args[PLAYLIST_URL])
        if not self._validate_args():
            self._download_button['state'] = 'normal'
        else:
            dir_path = get_dir_path(
                playlist_title=self._playlist.title,
                path_to_playlists=(
                    self._args[DESTINATION_PATH]
                    if len(self._args) > 1 else None
                )
            )
            self._create_progressbar()
            main_process = Process(
                target=download_videos, args=(self._playlist, dir_path)
            )
            main_process.start()

            self._progressbar.tkraise()
            self._run_progressbar()
            self._schedule_check(ms=1000, process=main_process)

    def _clicked_run_youtupy(self) -> None:
        self._label.configure(text=f'loading playlist...')
        self._download_button['state'] = 'disabled'
        self._main_process()

    @staticmethod
    def _get_window() -> Tk:
        window = Tk()
        window.title(WINDOW_TITLE)
        window.geometry(WINDOW_SIZE)
        return window

    def _get_download_button(self) -> Button:
        button = Button(
            master=self._window, text='press me!', width='15',
            fg='red', command=self._clicked_run_youtupy
        )
        button.grid(column=6, row=2)
        return button

    def _get_label(self) -> Label:
        label = Label(
            master=self._window,
            font=(MY_FONT, 20),
            text=MY_LABEL
        )
        label.grid(column=6, row=0)
        # label.pack()
        return label

    def _get_playlist_url(self) -> Entry:
        playlist_url = Entry(master=self._window, width=30)
        playlist_url.grid(column=1, row=2)
        playlist_url.focus()
        return playlist_url
