from multiprocessing import Process
from tkinter import Tk, Label, Button, Entry
# from tkinter.ttk import Progressbar, Style


from backend.const import PLAYLIST_URL, DESTINATION_PATH
from backend.handlers.data_handlers import (
    get_playlist, get_dir_path, download_videos
)
from backend.validators import (
    validate_path_existing, validate_path_to_dir,
    validate_playlist_existing, validate_playlist_loaded
)
from ui_tkinter.const import (
    MY_LABEL, DIR_EXISTS, EMPTY_PLAYLIST, MY_FONT,
    YOUTUBE_MUSIC, NEED_YOUTUBE_MUSIC, WINDOW_SIZE, WINDOW_TITLE
)


class YouTupy:
    def __init__(self) -> None:
        self.window = self._get_window()
        self.label = self._get_label()
        self.download_button = self._get_download_button()
        self.playlist_url = self._get_input_playlist_url()
        self.destination_dir = self._get_input_destination_dir()
        # style = Style()
        # style.theme_use('default')
        # style.configure("black.Horizontal.TProgressbar", background='black')
        # bar = Progressbar(
        # master=self.window, length=200, style='black.Horizontal.TProgressbar'
        # )
        # bar['value'] = main(user_input=self.user_input)
        # bar.grid(column=0, row=0)
        self.window.mainloop()

    def _schedule_check(self, my_process: Process) -> None:
        """Planning to call 'check_if_done()' during one second"""
        self.window.after(1000, self._check_if_done, my_process)

    def _check_if_done(self, my_process: Process) -> None:
        # If thread is done display message and activate button
        if not my_process.is_alive():
            self.label.configure(text='done!')
            # Reset button
            self.download_button['state'] = 'normal'
        else:
            # If not, gonna check after 1 sec
            self._schedule_check(my_process)

    def _validate_args(self) -> bool:
        if not self.playlist_url.get().startswith(YOUTUBE_MUSIC):
            self.label.configure(text=NEED_YOUTUBE_MUSIC)
        if len(self.args) > 1:
            validate_path_existing(dir_path=self.args[DESTINATION_PATH])
            self.args[DESTINATION_PATH] = validate_path_to_dir(
                dir_path=self.args[DESTINATION_PATH]
            )
        if validate_playlist_existing(playlist_url=self.args[PLAYLIST_URL]):
            if validate_playlist_loaded(args=self.args):
                return True
            else:
                self.label.configure(text=f'{self.playlist.title}{DIR_EXISTS}')

        else:
            self.label.configure(text=EMPTY_PLAYLIST)

    def _main_process(self) -> None:
        self.args = [self.playlist_url.get(), self.destination_dir.get()]
        self.args = [arg for arg in self.args if arg]
        if self._validate_args():
            self.playlist = get_playlist(playlist_url=self.args[PLAYLIST_URL])
            dir_path = get_dir_path(
                playlist_title=self.playlist.title,
                path_to_playlists=(
                    self.args[DESTINATION_PATH] if len(self.args) > 1 else None
                )
            )
            my_process = Process(
                target=download_videos, args=(self.playlist, dir_path)
            )
            my_process.start()
            self._schedule_check(my_process=my_process)

    def _clicked_run_youtupy(self) -> None:
        self.label.configure(text=f'loading playlist...')
        self.download_button['state'] = 'disabled'
        self._main_process()

    @staticmethod
    def _get_window() -> Tk:
        window = Tk()
        window.title(WINDOW_TITLE)
        window.geometry(WINDOW_SIZE)
        return window

    def _get_download_button(self) -> Button:
        button = Button(
            master=self.window, text='press me!', width='15',
            fg='red', command=self._clicked_run_youtupy
        )
        button.grid(column=6, row=2)
        return button

    def _get_label(self) -> Label:
        label = Label(
            master=self.window,
            font=(MY_FONT, 20),
            text=MY_LABEL
        )
        label.grid(column=6, row=0)
        # label.pack()
        return label

    def _get_input_playlist_url(self) -> Entry:
        playlist_url = Entry(master=self.window, width=25)
        playlist_url.grid(column=5, row=2)
        playlist_url.focus()
        return playlist_url

    def _get_input_destination_dir(self) -> Entry:
        input_dir = Entry(master=self.window, width=25)
        input_dir.grid(column=5, row=4)
        return input_dir
