from tkinter import Label, Canvas

from typing import List, Union, Dict

from ui_tkinter.const import MY_FONT, CURR_PATH


__all__ = 'LabelsMixin',


class LabelsMixin:
    def _create_empty_strings(self, rows: List[int]) -> None:
        for row in rows:
            empty_string = Label(master=self._window, text='')  # noqa
            empty_string.grid(column=0, row=row)

    def _get_curr_path_label(self) -> None:
        self._curr_path_label = Label(
            master=self._window,  # noqa
            font=(MY_FONT, 14),
            text=f'{CURR_PATH}: {self._destination_path}'  # noqa
        )
        self._curr_path_label.grid(
            column=0, row=10, sticky='W', columnspan=100
        )

    def _change_text_canvas(self, text: str) -> None:
        # first set coords to default
        self._main_canvas.coords(self._main_text_id, 5, 5)  # noqa
        self._main_canvas.itemconfig(  # noqa
            tagOrId=self._main_text_id, text=text  # noqa
        )

    def _get_canvas(self, kw: Dict[str, Union[str, int]]) -> Canvas:
        canvas = Canvas(master=self._window)  # noqa
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
