from tkinter import Tk, Label, Button, Entry
# from tkinter.ttk import Progressbar, Style

# from backend.handlers.data_handlers import get_playlist
from backend.main import main
# from backend.main import main
from ui_tkinter.const import MY_LABEL


class YouTupy:
    def __init__(self):
        self.window = self._get_window()
        self.label = self._get_label()
        self.access_button = self._get_access_button()
        self.playlist_url = self._get_input_playlist_url()
        self.destination_dir = self._get_input_destination_dir()
        # style = Style()
        # style.theme_use('default')
        # style.configure("black.Horizontal.TProgressbar", background='black')
        # bar = Progressbar(master=self.window, length=200, style='black.Horizontal.TProgressbar')
        # bar['value'] = main(user_input=self.user_input)
        # bar.grid(column=0, row=0)
        self.window.mainloop()

        # 'https://music.youtube.com/playlist?list=PLUydIkjRxOwgT1fEd5DBCxpV9zkg7wBVO&feature=share'

    def _main(self) -> None:
        args = [self.playlist_url.get(), self.destination_dir.get()]
        args = [arg for arg in args if arg]
        main(args=args)
        # print('args', args)
        # if self._validate_input(user_input=self.user_input):
        #     if validate_sys_args(sys_args=sys_args):
        #         playlist = get_playlist(playlist_url=sys_args[PLAYLIST_URL])
        #         dir_path = get_dir_path(
        #             playlist_title=playlist.title,
        #             path_to_playlists=sys_args[DESTINATION_PATH] if len(sys_args) > 1 else None
        #         )
        #         download_complete = validate_video_downloading(playlist=playlist, output_path=dir_path)
        #         if download_complete:
        #             dir_videos = get_dir_mp4_files(dir_path=dir_path)
        #             convert_mp4_to_mp3(dir_videos=dir_videos, dir_path=dir_path)
        #             remove_videos(dir_videos=dir_videos, dir_path=dir_path)
        #         print('Success, bro)')

    def clicked_run_youtupy(self) -> None:
        # print('validate', self._validate_input())
        if self._validate_input():
            self.label.configure(text=f'getting playlist...')
            print('AND')
            self._main()
            self.label.configure(text=f'done')
        self._get_access_button()

    @staticmethod
    def _get_window() -> Tk:
        window = Tk()
        window.title('youtupy')
        window.geometry('800x600')
        return window

    def _get_access_button(self) -> Button:
        button = Button(master=self.window, text='press me!', width='15', fg='red', command=self.clicked_run_youtupy)
        button.grid(column=6, row=2)
        return button

    def _get_label(self) -> Label:
        label = Label(
            master=self.window,
            font=('Arial Bold', 20),
            text=MY_LABEL
        )
        label.grid(column=6, row=0)
        return label

    def _validate_input(self) -> bool:
        # print('al', self.user_input)
        if not self.playlist_url.get().startswith('https://music.youtube.com/'):
            self.label.configure(text=f"your link should starts with 'https://music.youtube.com/'")
            return False
        else:
            return True

    def _get_input_playlist_url(self) -> Entry:
        playlist_url = Entry(master=self.window, width=25)
        playlist_url.grid(column=5, row=2)
        playlist_url.focus()
        return playlist_url

    def _get_input_destination_dir(self) -> Entry:
        input_dir = Entry(master=self.window, width=25)
        input_dir.grid(column=5, row=4)
        return input_dir
