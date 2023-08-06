from tkinter.ttk import Label

from pytk_net.utils import load_font_icon

from overwrite.DateEntry import DateEntry


class Icon(Label):
    def __init__(self, parent, icon_name, size, color):
        super().__init__(parent, image=load_font_icon(icon_name, size, color))


ALL_WIDGET = [
    DateEntry, Icon
]
