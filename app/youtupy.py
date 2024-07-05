import pytube
import os

from ui_tkinter.tkin import YouTupy

if __name__ == "__main__":
    # fixing bug
    pytube.innertube._default_clients['ANDROID'] = (
        pytube.innertube._default_clients['WEB']
    )

    entry_point_path = os.path.dirname(os.path.realpath(__file__))
    YouTupy(entry_point_path=entry_point_path)
