# aliases
CURR_PATH = 'current folder'
MAIN_CANVAS_TEXT = 'welcome to youtupy!'
INPUT_CANVAS_TEXT = 'paste your link:'
TYPE_TO_CLASS_TABLE = {
    'playlist': 'Playlist',
    'video': 'YouTube'
}
DOWNLOAD_CLASS_METHOD = {
    'Playlist': 'title',
    'YouTube': 'title'
}
TYPE_TO_METHOD_TABLE = {
    'playlist': 'videos',
    'video': 'title'
}

# errors
EMPTY_PLAYLIST = 'something went wrong. check the url'


# settings
WINDOW_TITLE = 'youtupy'
WINDOW_SIZE = '800x600'
MY_FONT = 'Arial Bold'
AVERAGE_DOWNLOAD_N_CONVERT_TIME = 15
AVERAGE_DOWNLOAD_TIME = 8
STEPS_AMOUNT = 20
INPUT_CANVAS_KWARGS = {
    'column': 0, 'row': 3, 'font_size': 14, 'padding_top': 0, 'long': 0,
    'text_id': '_input_text_id', 'text': INPUT_CANVAS_TEXT
}
MAIN_CANVAS_KWARGS = {
            'column': 6, 'row': 0, 'font_size': 24, 'padding_top': 8,
            'text_id': '_main_text_id', 'text': MAIN_CANVAS_TEXT, 'long': 200
        }
UNWISHED_NAME_PARTS = [
    '(official video)', '(remix - official video)', '(official)', '(hd)',
    '(official music video)', '(lyric video)', '[official video]',
    '[official lyric video]', 'official lyric video', '(official lyric video)',
    'official video - ', ' - official video', 'official video',
    'official audio', '(official audio)', '[official audio]', '(audio)'
    '[official music video]', '(official 4k video)', '[video]', '[audio]',
    '(video)', '[official animated video]', '[official animated music video]',
    '(official animated video)', '(official animated music video)',
    '(official mixtape)', '[official mixtape]', '(official hd video)',
    '[official hd video]'
]
