import getpass
import os
from multiprocessing import Process
from pathlib import Path
from time import sleep
from tkinter import (
    Tk, Label, Button, Entry, Frame, filedialog, messagebox, PhotoImage,
    StringVar, Canvas, Event
)
from tkinter.ttk import Style, Progressbar, Radiobutton
from typing import List, Dict, Union
from urllib.error import URLError

from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError

from backend.const import DEFAULT_DOWNLOAD_PATH
from backend.handlers.for_data import (
    get_path_to_playlist, download_object, get_download_object,
    get_clean_title
)
from backend.handlers.for_validation import remove_dir, remove_file
from backend.validators import (
    validate_object, init_load_object_attempt, validate_already_loaded
)
from ui_tkinter.const import (
    MAIN_CANVAS_TEXT, EMPTY_PLAYLIST, MY_FONT, STEPS_AMOUNT, CURR_PATH,
    WINDOW_SIZE, WINDOW_TITLE, MAIN_CANVAS_KWARGS, INPUT_CANVAS_KWARGS,
    TYPE_TO_CLASS_TABLE, AVERAGE_DOWNLOAD_TIME
)


class YouTupy:
    def __init__(self) -> None:
        self._window = self._get_window()
        self._create_extension_radiobuttons()
        self._create_download_type_radiobuttons()
        self._main_canvas = self._get_canvas(kw=MAIN_CANVAS_KWARGS)
        self._input_canvas = self._get_canvas(kw=INPUT_CANVAS_KWARGS)
        self._download_button = self._get_download_button()
        self._input_url = self._get_input_url()
        self._destination_path = str(Path(DEFAULT_DOWNLOAD_PATH).resolve())
        self._destination_button = self._get_destination_button()
        self._create_empty_strings(rows=[7])
        self._window.mainloop()

    def _create_empty_strings(self, rows: List[int]) -> None:
        for row in rows:
            empty_string = Label(master=self._window, text='')
            empty_string.grid(column=0, row=row)

    def _create_extension_radiobuttons(self) -> None:
        self._radio_frame = Frame(master=self._window)
        self._radio_frame.grid(column=0, row=6, sticky='W')
        # default
        self._selected_extension = StringVar(master=self._window, value='.mp3')
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
            master=self._window, value='playlist'
        )
        radiobutton_playlist = Radiobutton(
            master=self._radio_frame, text='playlist', value='playlist',
            variable=self._selected_download_type
        )
        radiobutton_video = Radiobutton(
            master=self._radio_frame, text='video', value='video',
            variable=self._selected_download_type
        )
        radiobutton_playlist.grid(column=3, row=0, padx=(10, 0))
        radiobutton_video.grid(column=4, row=0)

    def _object_exists_msg_box(self) -> bool:
        object_type = self._selected_download_type.get()
        load_object = self._download_object
        object_name = get_clean_title(title=load_object.title)
        extension = self._selected_extension.get()
        extension = (
            extension if object_type == 'video' else f' ({extension})'
        )
        object_type = (
            'audio' if object_type == 'video' and extension == '.mp3'
            else object_type
        )
        path = self._destination_path
        path = (
            f'{path}/{object_name}{extension}'
            if isinstance(load_object, YouTube)
            else f'{path}/{object_name}'
        )
        answer = messagebox.askyesno(
            message=f'override {object_type}?\n\n{object_name}{extension}'
        )
        self._input_url.focus()
        if answer:
            if object_type in ('video', 'audio'):
                remove_file(path=path)
            else:
                remove_dir(path=path)
            return True

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
        videos_amount = 1
        if self._selected_download_type.get() == 'playlist':
            videos_amount = self._download_object.length

        ms = int(videos_amount * AVERAGE_DOWNLOAD_TIME / STEPS_AMOUNT * 1000)

        self._update_progressbar(ms=ms, main_process=main_process)

    def _create_progressbar(self) -> None:
        self._progressbar = Progressbar(
            master=self._window, mode='determinate',
            orient='horizontal', length=265
        )
        self._progressbar.grid(column=0, row=0)

    def _validate_playlist(self) -> bool:
        # подвисаем здесь
        download_type = self._selected_download_type.get()
        if validate_object(
            load_object=self._download_object,
            download_type=download_type
        ):
            object_title = self._download_object.title
            object_title = get_clean_title(title=object_title)
            path = get_path_to_playlist(
                playlist_title=object_title,
                playlist_path=self._destination_path
            )
            extension = self._selected_extension.get()
            if validate_already_loaded(
                [self._input_url.get(), path, download_type, extension]
            ):
                return True
            else:
                answer = self._object_exists_msg_box()
                if answer is True:
                    return True
                else:
                    self._change_text_canvas(text=MAIN_CANVAS_TEXT)

        else:
            self._change_text_canvas(text=EMPTY_PLAYLIST)

    def _validate_video(self) -> bool:
        path = self._destination_path
        download_type = self._selected_download_type.get()
        extension = self._selected_extension.get()
        if validate_already_loaded(
            [self._input_url.get(), path, download_type, extension]
        ):
            return True
        else:
            answer = self._object_exists_msg_box()
            if answer is True:
                return True
            else:
                self._change_text_canvas(text=MAIN_CANVAS_TEXT)

    def _validate_args(self, download_type: str) -> bool:
        try:
            init_load_object_attempt(
                input_url=self._input_url.get(),
                download_class=(
                    TYPE_TO_CLASS_TABLE[self._selected_download_type.get()]
                )
            )
            self._create_main_process_vars(download_type=download_type)
        except (KeyError, URLError, RegexMatchError):
            self._change_text_canvas(
                text=f'invalid link for {self._selected_download_type.get()}'
            )
            return False
        return (
            getattr(self, f'_validate_{self._selected_download_type.get()}')()
        )

    def _create_main_process_vars(self, download_type: str):
        input_url = self._input_url.get()
        class_name = TYPE_TO_CLASS_TABLE[download_type]
        self._download_object = get_download_object(
            class_name=class_name, url=input_url
        )
        self._download_class = (
            Playlist if download_type == 'playlist' else YouTube
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

    def _get_download_button(self) -> Button:
        button = Button(
            master=self._window, text='download', width='10',
            fg='red', command=lambda: self._clicked_run_youtupy()
        )
        button.grid(column=6, row=5, sticky='W')
        return button

    def _clicked_run_youtupy(self) -> None:
        print('clicked!')
        self._main_download()

    def _main_download(self) -> None:
        download_type = self._selected_download_type.get()
        if self._validate_args(download_type=download_type):
            alias = download_type
            extension = self._selected_extension.get()
            if download_type == 'video' and extension == '.mp3':
                alias = 'audio'
            self._change_text_canvas(text=f'loading {alias}...')
            self._download_button['state'] = 'disabled'

            func = f'download_{download_type}'
            object_title = self._download_object.title
            object_title = get_clean_title(title=object_title)
            path = self.get_or_create_path(object_title)

            main_process = Process(
                target=download_object,
                args=(self._download_object, path, extension, func)
            )
            main_process.start()
            print("main process started")
            self._create_progressbar()
            self._progressbar.tkraise()
            self._run_progressbar(main_process=main_process)
            self._schedule_check(ms=1000, process=main_process)

    def get_or_create_path(self, object_title) -> str:
        path = (
            self._destination_path
            if isinstance(self._download_object, YouTube)
            else f'{self._destination_path}/{object_title}'
        )
        os.makedirs(path, exist_ok=True)
        return path

    def _get_curr_path_label(self) -> None:
        self._curr_path_label = Label(
            master=self._window,
            font=(MY_FONT, 14),
            text=f'{CURR_PATH}: {self._destination_path}'
        )
        self._curr_path_label.grid(
            column=0, row=10, sticky='W', columnspan=100
        )

    def _clicked_choose_dir(self) -> None:
        directory = filedialog.askdirectory(
            # gonna work on mac, have to check for windows and linux
            # initialdir=os.path.normpath("C://") try on Windows
            parent=self._window,
            initialdir=f'/Users/{getpass.getuser()}/'
        )
        if directory:
            self._destination_path = (str(Path(directory).resolve()))
        self._curr_path_label.configure(
            text=f'{CURR_PATH}: {self._destination_path}'
        )

    def _get_destination_button(self) -> Button:
        button = Button(
            master=self._window, text='choose folder', width='12',
            fg='red', command=self._clicked_choose_dir
        )
        button.grid(column=0, row=11, sticky='W')

        self._get_curr_path_label()
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

    def _get_input_url(self) -> Entry:
        input_url = Entry(master=self._window, width=30)
        input_url.grid(column=0, row=5, sticky='WE')
        input_url.focus()
        return input_url

    def _closer(self, _: Event) -> None:
        self._window.destroy()

    def _get_window(self) -> Tk:
        window = Tk()

        # binds
        window.bind('<Escape>', lambda _: self._closer(_))
        # window.bind('<Enter>', lambda _: self._clicked_run_youtupy())

        style = Style(master=window)
        style.theme_use('aqua')
        icon = f'{os.getcwd()}/static/jordan.png'
        window.iconphoto(True, PhotoImage(file=icon))
        window.title(WINDOW_TITLE)
        window.geometry(WINDOW_SIZE)
        return window
