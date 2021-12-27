from tkinter import Tk, Label, Button, Entry
# from tkinter.ttk import Progressbar, Style

# from backend.handlers.data_handlers import get_playlist
# from backend.main import main

from ui_tkinter.const import MY_LABEL


class YouTupy:
    def __init__(self):
        self.window = self._get_window()
        self.label = self._get_label()
        self.button = self._get_button()
        self.user_input = self._get_user_input()
        # style = Style()
        # style.theme_use('default')
        # style.configure("black.Horizontal.TProgressbar", background='black')
        # bar = Progressbar(master=self.window, length=200, style='black.Horizontal.TProgressbar')
        # bar['value'] = main(user_input=self.user_input)
        # bar.grid(column=0, row=0)
        self.window.mainloop()

    def clicked(self) -> None:
        # print('validate', self._validate_input())
        if self._validate_input():
            self.label.configure(text=f'{self.user_input.get()} - trying to get playlist...')
        self._get_button()

    @staticmethod
    def _get_window() -> Tk:
        window = Tk()
        window.title('youtupy')
        window.geometry('800x600')
        return window

    def _get_button(self) -> Button:
        button = Button(master=self.window, text='Press me!', width='15', fg='red', command=self.clicked)
        button.grid(column=6, row=1)
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
        if not self.user_input.get().startswith('https://music.youtube.com/'):
            self.label.configure(text=f"Your link should starts with 'https://music.youtube.com/'")
            return False
        else:
            return True

    def _get_user_input(self) -> Entry:
        user_input = Entry(master=self.window, width=25)
        user_input.grid(column=5, row=2)
        user_input.focus()
        return user_input

        # 'https://music.youtube.com/watch?v=Cb5TOFmLJnM&feature=share'

    # def _main(self) -> None:
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
