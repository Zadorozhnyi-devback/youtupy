import concurrent
import platform
import os
import subprocess

from yt_dlp import YoutubeDL


__all__ = 'YoutubeAudioDownloader',


class Color:
    """ Color codes """
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'


class YoutubeAudioDownloader:

    def __init__(self, *args, **kwargs):
        self.ffmpeg_path = self.get_ffmpeg_path('/usr/local/bin/ffmpeg')
        self.download_path = self.get_download_path(kwargs)
        self.limit = self.get_limit(kwargs)

        self.opts = self.get_opts()

        self.urls = kwargs.get('urls', [])

        self.status = list()

    @staticmethod
    def get_download_path(kwargs: dict) -> str:
        path = kwargs.get('download_path')
        if path and os.path.exists(path):
            return path

    @staticmethod
    def get_limit(kwargs: dict) -> int:
        """ Return downloads limit at a time """
        limit = kwargs.get('limit', 0)
        limit = limit if limit and isinstance(limit, int) else 2
        return limit

    def get_opts(self) -> dict:
        """ Return youtube-dl options """
        yt_dlp_options = {
            'quiet': True,
            'format': 'bestaudio/best',
            'ffmpeg_location': self.ffmpeg_path,
            'keepvideo': False,
            'outtmpl': f'{self.download_path}/%(title)s - %(artist)s.webm',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320'
            }],

            # OPTIONAL options
            'noplaylist': True,
            'noprogress': True,
        }
        return yt_dlp_options

    def run(self):
        # printing download status on terminal
        for url in self.urls:
            self.status.append(f"{Color.OKCYAN}[starting]{Color.ENDC}\t {url}")

        ''' start download every YouTube URLS passed from command line '''
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.limit
        ) as executor:
            executor.map(self.download, self.urls)

    @staticmethod
    def clear():
        """ Clear terminal """
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:
            subprocess.call(['clear && printf "\e[3J"'], shell=True)

    @staticmethod
    def get_ffmpeg_path(path: str = '') -> str:
        """ Set ffmpeg binary location (-f, --ffmpeg) """
        # if, ffmpeg path is passed from command line arguments
        if path:
            # if, passed path exists
            if (
                os.path.exists(path)
                and (path.split('/')[-1] in ['ffmpeg', 'ffmpeg.exe'])
            ):
                return path
            # else, the passed ffmpeg path is invalid, exits program
            else:
                print(
                    f"{Color.ERROR}ffmpeg at `{path}`"
                    f" NOT FOUND{Color.ENDC}"
                )
                exit(0)

        # else if, use the ffmpeg which is already installed
        # by some Operating System's package manager
        elif os.path.exists('/usr/bin/ffmpeg'):
            return '/usr/bin/ffmpeg'

        # else if, use the ffmpeg binaries present with this project
        elif os.path.exists(f'{os.path.abspath(os.getcwd())}/ffmpeg'):
            if platform.system() == 'Windows':
                return f'{os.path.abspath(os.getcwd())}/ffmpeg/windows/ffmpeg.exe'
            elif platform.system() == 'Darwin':
                return f'{os.path.abspath(os.getcwd())}/ffmpeg/darwin/ffmpeg'
            elif platform.system() == 'Linux':
                return f'{os.path.abspath(os.getcwd())}/ffmpeg/linux/ffmpeg'

        # else, if using "ytmp3-dl-base" release version
        # which does not contains ffmpeg binaries,
        # neither a ffmpeg binary location path
        # is passed nor ffmpeg is installed
        else:
            print(
                f"{Color.ERROR}ffmpeg NOT FOUND.{Color.ENDC}"
                '\n'    f"If you are using {Color.OKCYAN}'ytmp3-dl-base'{Color.ENDC} version,"
                '\n'    f"unless valid 'ffmpeg' binary location path is passed during execution (-f /path/to/ffmpeg)"
                '\n'    f"this program will not run, as this version does not comes with ffmpeg and its required tools & binaries."
                '\n'    f"You have to install them seperately for your operating system."
                '\n'    f"https://ffmpeg.org/download.html"

                '\n\n'  f"You can always use {Color.OKCYAN}'ytmp3-dl-essentials'{Color.ENDC} version for every needs and hassel free setup,"
                '\n'    f"although this comes with extra packages giving it more overall download size."
                '\n'    f"Check out the release version for your specific OS here : https://github.com/poseidon-code/ytmp3-dl/releases"
                '\n'    f"and download your essentials version."

                '\n\n'  f"As an alternative you can always download the source code and use the script directly."
                '\n'    f"Download the source code from here : https://github.com/poseidon-code/ytmp3-dl/archive/refs/heads/main.zip"

                '\n\n'  f"Check out the README.md for more detailed explainations."
                '\n'    f"https://github.com/poseidon-code/ytmp3-dl"
            )
            exit(0)

    @staticmethod
    def usage():
        """ Show help of ytmp3-dl (-h, --help) """
        print(
            f"{Color.ERROR}yt{Color.WARNING}mp3-dl {Color.OKGREEN}v3.0 {Color.OKCYAN}~poseidon-code{Color.ENDC}"
            '\n'    f"Python script for multi-threaded download of audio from any YouTube video/audio link provided during the runtime,"
            '\n'    f"and converts it to .mp3 format of high quality. It is a wrapper over yt-dlp Python library."
            '\n'    f"Check out the project on Github : https://github.com/poseidon-code/ytmp3-dl"
        )

        print(
            '\n'    f"[OPTIONS]                     [USAGE]"
            '\n'    f"-d, --dir [PATH]              set download directory"
            '\n'    f"-f, --ffmpeg [PATH]           set the exact path to ffmpeg binary"
            '\n'    f"-l, --limit [NUMBER]          set concurrent download limit"

            '\n\n'  f"[FLAGS]                       [USAGE]"
            '\n'    f"-h, --help                    show help on using the ytmp3-dl CLI"
        )
        exit()

    def print_status(self):
        """ Printing on terminal """
        self.clear()
        print(
            f"{Color.ERROR}yt{Color.WARNING}mp3-dl {Color.OKGREEN}v3.0 {Color.OKCYAN}~poseidon-code{Color.ENDC}"
            '\n'    f"{Color.ERROR}|{Color.ENDC} URLs                       : {len(self.urls)}"
            '\n'    f"{Color.ERROR}|{Color.ENDC} Using ffmpeg at            : {self.ffmpeg_path}"
            '\n'    f"{Color.ERROR}|{Color.ENDC} Download Directory         : {self.download_path}"
            '\n'    f"{Color.ERROR}|{Color.ENDC} Concurrent Download Limit  : {self.limit}"
        )
        print()
        [print(item) for item in self.status]

    def download(self, url):
        """
        Downloading mp3 for every YouTube video URL passed during execution
        """
        with CustomYoutubeDL(self.opts) as mp3:
            info = mp3.extract_info(url, download=False)
            info['title'] = self.get_title(info)

            self.status[self.urls.index(url)] = (
                f"{Color.WARNING}[downloading]{Color.ENDC}\t {info['title']}"
            )
            self.print_status()

            mp3.download([url])

            self.status[self.urls.index(url)] = (
                f"{Color.OKGREEN}[finished]{Color.ENDC}\t {info['title']}"
            )
            self.print_status()

    def get_title(self, info: dict = None) -> str:
        if info:
            title = get_title_from_info(info)
        else:
            with CustomYoutubeDL(self.opts) as mp3:
                info = mp3.extract_info(self.urls[0], download=False)
                title = get_title_from_info(info)

        return title


class CustomYoutubeDL(YoutubeDL):
    """ Redefine 'prepare_filename' method, to clean duplicates in artists """

    def prepare_filename(self, info_dict, dir_type='', warn=False):
        old = super().prepare_filename(info_dict, dir_type, warn)

        path = '/'.join(old.split('/')[:-1])
        title = get_title_from_info(info_dict)

        return f'{path}/{title}.mp3'


def get_title_from_info(info: dict) -> str:
    artists = ', '.join(sorted(set(info.get('artist', '').split(', '))))

    title = '{artists} - {title}'.format(
        artists=artists,
        title=f"{info.get('title', '')}"
    )
    return title
