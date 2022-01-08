import getpass
import os
from multiprocessing import Process
from time import sleep
from tkinter import (
    Tk, Label, Button, Entry, Frame, filedialog, messagebox, PhotoImage,
    StringVar, Canvas
)
from tkinter.ttk import Style, Progressbar, Radiobutton
from typing import List, Dict, Union

from backend.const import DEFAULT_PLAYLIST_PATH
from backend.handlers.for_data import (
    get_playlist, get_path_to_playlist, download_videos
)
from backend.handlers.for_validation import remove_playlist_dir
from backend.validators import (
    validate_path_existing, validate_playlist_loaded,
    validate_playlist_existing, validate_internet_connection
)
from ui_tkinter.const import (
    MAIN_CANVAS_TEXT, EMPTY_PLAYLIST, MY_FONT, STEPS_AMOUNT, CURR_PATH,
    WINDOW_SIZE, WINDOW_TITLE, MAIN_CANVAS_KWARGS, INPUT_CANVAS_KWARGS,
    LIST_EXISTS_MSG_BOX_MSG, LIST_EXISTS_MSG_BOX_TITLE, NO_INTERNET,
    AVERAGE_DOWNLOAD_N_CONVERT_TIME, AVERAGE_DOWNLOAD_TIME
)


class YouTupy:
    def __init__(self) -> None:
        self._window = self._get_window()
        self._create_extension_radiobuttons()
        self._main_canvas = self._get_canvas(kw=MAIN_CANVAS_KWARGS)
        self._input_canvas = self._get_canvas(kw=INPUT_CANVAS_KWARGS)
        self._download_button = self._get_download_button()
        self._playlist_url = self._get_playlist_url()
        self._playlist = get_playlist(playlist_url=self._playlist_url.get())
        self._playlist_path = DEFAULT_PLAYLIST_PATH
        self._destination_button = self._get_destination_button()
        self._create_empty_strings(rows=[7])
        self._window.mainloop()

    def _create_empty_strings(self, rows: List[int]) -> None:
        for row in rows:
            empty_string = Label(master=self._window, text='')
            empty_string.grid(column=0, row=row)

    def _create_extension_radiobuttons(self) -> None:
        frame = Frame(master=self._window)
        frame.grid(column=0, row=6, sticky='W')
        # default
        self._selected_extension = StringVar(master=None, value='.mp4')
        radiobutton_mp3 = Radiobutton(
            master=frame, text='mp3', value='.mp3',
            variable=self._selected_extension
        )
        radiobutton_mp4 = Radiobutton(
            master=frame, text='mp4', value='.mp4',
            variable=self._selected_extension
        )
        radiobutton_mp3.grid(column=0, row=0)
        radiobutton_mp4.grid(column=1, row=0)

    def _playlist_exists_msg_box(self) -> bool:
        answer = messagebox.askyesno(
            title=LIST_EXISTS_MSG_BOX_TITLE,
            message=LIST_EXISTS_MSG_BOX_MSG)
        if answer:
            remove_playlist_dir(
                playlist_path=self._playlist_path,
                playlist_title=self._playlist.title
            )
            return True

    def _clicked_choose_dir(self) -> None:
        self._window.directory = filedialog.askdirectory(
            # gonna work on mac, have to check for windows and linux
            initialdir=f'/Users/{getpass.getuser()}/'
        )
        if self._window.directory:
            self._playlist_path = self._window.directory
        self._curr_path_label.configure(
            text=f'{CURR_PATH}{self._playlist_path}'
        )

    def _get_curr_path_label(self) -> None:
        self._curr_path_label = Label(
            master=self._window,
            font=(MY_FONT, 14),
            text=f'{CURR_PATH}{self._playlist_path}'
        )
        self._curr_path_label.grid(
            column=0, row=10, sticky='W', columnspan=100
        )

    def _get_destination_button(self) -> Button:
        button = Button(
            master=self._window, text='choose folder', width='12',
            fg='red', command=self._clicked_choose_dir
        )
        button.grid(column=0, row=11, sticky='W')

        self._get_curr_path_label()
        return button

    def _increment_progressbar(self) -> None:
        self._progressbar['value'] += 5
        self._window.update()

    def _update_progressbar(self, ms: int, main_process: Process) -> None:
        if main_process.is_alive():
            self._increment_progressbar()
            func = self._update_progressbar
            if self._progressbar['value'] == 95:
                self._change_text_canvas(text='almost done...')
                return
            self._window.after(ms, func, ms, main_process)

    def _run_progressbar(self, main_process: Process) -> None:
        self._progressbar['value'] = 0
        playlist_length = self._playlist.length
        # math to get progressbar step time in ms
        average_time_for_video = (
            AVERAGE_DOWNLOAD_N_CONVERT_TIME
            if self._selected_extension.get() == '.mp3'
            else AVERAGE_DOWNLOAD_TIME
        )
        ms = int(
            playlist_length * average_time_for_video / STEPS_AMOUNT * 1000
        )
        self._update_progressbar(ms=ms, main_process=main_process)

    def _create_progressbar(self) -> None:
        self._progressbar = Progressbar(
            master=self._window, mode='determinate',
            orient='horizontal', length=265
        )
        self._progressbar.grid(
            column=0, row=0
        )

    def _schedule_check(
        self, ms: int, process: Process, func_name: str = '_schedule_check'
    ) -> None:
        """
        Planning to call '_check_process_done()' after 'ms' * 1000 seconds
        """
        func = self._check_process_done
        self._window.after(ms, func, ms, process, func_name)

    def _check_process_done(
        self, ms: int, process: Process, func_name: str
    ) -> None:
        # If thread is done display message, activate button, finish pb
        if process.is_alive():
            getattr(self, func_name)(
                ms=ms, process=process, func_name=func_name
            )
        else:
            # костыль для добивания прогрессбара
            while self._progressbar['value'] < 100:
                self._increment_progressbar()
                sleep(0.2)
            self._progressbar.destroy()
            self._change_text_canvas(text='done!')
            self._download_button['state'] = 'normal'

    def _validate_args(self) -> bool:
        if not validate_internet_connection(playlist=self._playlist):
            self._change_text_canvas(text=NO_INTERNET)
            return False
        validate_path_existing(playlist_path=self._playlist_path)
        if validate_playlist_existing(playlist=self._playlist):
            if validate_playlist_loaded(
                    [self._playlist_url.get(), self._playlist_path]
            ):
                return True
            else:
                if self._playlist_exists_msg_box():
                    return True
                else:
                    self._change_text_canvas(text=MAIN_CANVAS_TEXT)

        else:
            self._change_text_canvas(text=EMPTY_PLAYLIST)

    def _main_process(self) -> None:
        self._playlist = get_playlist(playlist_url=self._playlist_url.get())
        if self._validate_args():
            self._download_button['state'] = 'disabled'
            self._change_text_canvas(text='loading playlist...')
            path_to_playlist = get_path_to_playlist(
                playlist_title=self._playlist.title,
                playlist_path=self._playlist_path
            )
            self._create_progressbar()
            main_process = Process(
                target=download_videos,
                args=(
                    self._playlist, path_to_playlist,
                    self._selected_extension.get()
                )
            )
            main_process.start()

            self._progressbar.tkraise()
            self._run_progressbar(main_process=main_process)
            self._schedule_check(ms=1000, process=main_process)

    def _clicked_run_youtupy(self) -> None:
        self._main_process()

    @staticmethod
    def _get_window() -> Tk:
        window = Tk()
        style = Style(master=window)
        style.theme_use('aqua')
        icon = f'{os.getcwd()}/static/jordan.png'
        window.iconphoto(True, PhotoImage(file=icon))
        window.title(WINDOW_TITLE)
        window.geometry(WINDOW_SIZE)
        return window

    def _get_download_button(self) -> Button:
        button = Button(
            master=self._window, text='download', width='10',
            fg='red', command=self._clicked_run_youtupy
        )
        button.grid(column=6, row=5, sticky='W')
        return button

    def _change_text_canvas(self, text: str) -> None:
        # first set coords to default
        self._main_canvas.coords(self._main_text_id, 5, 5)
        self._main_canvas.itemconfig(
            tagOrId=self._main_text_id, text=text
        )

    def _get_canvas(self, kw: Dict[str, Union[str, int]]) -> Canvas:
        canvas = Canvas(master=self._window)
        canvas.grid(column=kw['column'], row=kw['row'], sticky='W')
        setattr(
            self, kw['text_id'],
            canvas.create_text(
                5, kw['padding_top'], text=kw['text'],
                font=(MY_FONT, kw['font_size']), anchor='nw'
            )
        )
        bbox = canvas.bbox(getattr(self, kw['text_id']))
        # size without padding on y bottom and long width
        canvas.configure(height=bbox[3], width=bbox[2] + kw['long'])
        return canvas

    def _get_playlist_url(self) -> Entry:
        playlist_url = Entry(master=self._window, width=30)
        playlist_url.grid(column=0, row=5, sticky='WE')
        playlist_url.focus()
        return playlist_url
