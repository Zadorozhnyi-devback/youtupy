import getpass
import os
from multiprocessing import Process
from time import sleep
from tkinter import (
    Tk, Label, Button, Entry, Frame, filedialog, messagebox, PhotoImage,
    StringVar, Canvas
)
from tkinter.ttk import Style, Progressbar, Radiobutton

from backend.const import DEFAULT_PLAYLIST_PATH
from backend.handlers.for_data import (
    get_playlist, get_path_to_playlist, download_videos
)
from backend.handlers.for_validation import remove_playlist_dir
from backend.validators import (
    validate_path_existing, validate_playlist_loaded,
    validate_playlist_existing
)
from ui_tkinter.const import (
    WELCOME_TO_YOUTUPY, EMPTY_PLAYLIST, MY_FONT,
    WINDOW_SIZE, WINDOW_TITLE,
    STEPS_AMOUNT, AVERAGE_TIME_FOR_VIDEO, CURR_PATH
)


class YouTupy:
    def __init__(self) -> None:
        self._window = self._get_window()
        self._create_extension_radiobuttons()
        self._main_canvas = self._get_main_canvas()
        self._download_button = self._get_download_button()
        self._playlist_url = self._get_playlist_url()
        self._playlist_path = DEFAULT_PLAYLIST_PATH
        self._destination_button = self._get_destination_button()

        self._empty_string = Label(master=self._window, text='')
        self._empty_string.grid(column=0, row=3)

        self._window.mainloop()

    def _create_extension_radiobuttons(self):
        frame = Frame(master=self._window)
        frame.grid(column=0, row=6, sticky='W')
        self._selected_extension = StringVar(master=None, value='.mp3')
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
            title='playlist exists!',
            message='override playlist?')
        if answer:
            remove_playlist_dir(
                playlist_path=self._playlist_path,
                playlist_title=self._playlist.title
            )
            return True

    def _clicked_choose_dir(self):
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
            column=0, row=4, sticky='W', columnspan=100
        )

    def _get_destination_button(self) -> Button:
        button = Button(
            master=self._window, text='choose folder', width='12',
            fg='red', command=self._clicked_choose_dir
        )
        button.grid(column=0, row=5, sticky='W')

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
        ms = playlist_length * AVERAGE_TIME_FOR_VIDEO // STEPS_AMOUNT * 1000
        self._update_progressbar(ms=ms, main_process=main_process)

    def _create_progressbar(self) -> None:
        # progress_frame = Frame(self._window)
        # progress_frame.grid(
        #     column=0, row=0, padx=0, pady=10
        # )
        self._progressbar = Progressbar(
            master=self._window, mode='determinate', orient='horizontal',
            length=250
        )
        self._progressbar.grid(
            column=0, row=0, padx=0, pady=10
        )
        # blank = Frame(progress_frame)
        # blank.grid(
        #     column=0, row=0, padx=0, pady=10, sticky='nsew'
        # )

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
        # If thread is done display message and activate button
        if not process.is_alive():
            # костыль для добивания прогрессбара
            while self._progressbar['value'] < 100:
                self._increment_progressbar()
                sleep(0.2)
            self._progressbar.destroy()
            self._change_text_canvas(text='done!')
            # Reset button
            self._download_button['state'] = 'normal'
            # Hide bar
        else:
            # If not, gonna check after ms * 1000 sec
            getattr(self, func_name)(
                ms=ms, process=process, func_name=func_name
            )

    def _validate_args(self) -> bool:
        playlist_url = self._playlist_url.get()
        validate_path_existing(playlist_path=self._playlist_path)
        if validate_playlist_existing(playlist_url=playlist_url):
            if validate_playlist_loaded(
                    [playlist_url, self._playlist_path]
            ):
                return True
            else:
                if self._playlist_exists_msg_box():
                    return True
                else:
                    self._change_text_canvas(text=WELCOME_TO_YOUTUPY)

        else:
            self._change_text_canvas(text=EMPTY_PLAYLIST)

    def _main_process(self) -> None:
        self._playlist = get_playlist(playlist_url=self._playlist_url.get())
        if self._validate_args():
            self._change_text_canvas(text='loading playlist...')
            self._download_button['state'] = 'disabled'
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
        my_path = f'{os.getcwd()}/static/jordan.png'
        window.iconphoto(True, PhotoImage(file=my_path))
        window.title(WINDOW_TITLE)
        window.geometry(WINDOW_SIZE)
        return window

    def _get_download_button(self) -> Button:
        button = Button(
            master=self._window, text='download', width='10',
            fg='red', command=self._clicked_run_youtupy
        )
        button.grid(column=6, row=2, sticky='W')
        return button

    def _change_text_canvas(self, text: str) -> None:
        # first set coords to default
        self._main_canvas.coords(self._canvas_text_id, 5, 5)
        self._main_canvas.itemconfig(tagOrId=self._canvas_text_id, text=text)

    def _get_main_canvas(self) -> Canvas:
        canvas = Canvas(master=self._window)
        canvas.grid(column=6, row=0)
        # text padding left=5, top=-23
        self._canvas_text_id = canvas.create_text(
            5, -23, font=(MY_FONT, 24), text=WELCOME_TO_YOUTUPY, anchor='nw'
        )
        bbox = canvas.bbox(self._canvas_text_id)
        # size without padding on y bottom and long width
        canvas.configure(width=bbox[2] + 200, height=bbox[3] - 26)
        return canvas

    def _get_playlist_url(self) -> Entry:
        playlist_url = Entry(master=self._window, width=30)
        playlist_url.grid(column=0, row=2)
        playlist_url.focus()
        return playlist_url
