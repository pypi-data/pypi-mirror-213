import tkinter as tk
from datetime import datetime

import ttkbootstrap.dialogs


class DatePickerDialog(ttkbootstrap.dialogs.DatePickerDialog):
    def __init__(self, **kwargs):
        super(DatePickerDialog, self).__init__(**kwargs)

    def _header_columns(self):
        """
        重写日历上周末文字
        """
        weekdays = [
            "周一",
            "周二",
            "周三",
            "周四",
            "周五",
            "周六",
            "周日",
        ]
        header = weekdays[self.firstweekday:] + weekdays[: self.firstweekday]
        return header


class Querybox(ttkbootstrap.Querybox):

    @staticmethod
    def get_date(
            parent=None,
            title=" ",
            firstweekday=6,
            startdate=None,
            bootstyle="primary",
    ):
        chooser = DatePickerDialog(
            parent=parent,
            title=title,
            firstweekday=firstweekday,
            startdate=startdate,
            bootstyle=bootstyle,
        )
        return chooser.date_selected


class DateEntry(ttkbootstrap.DateEntry):
    def __init__(self, master, dateformat="%Y-%m-%d", firstweekday=0, **kwargs):
        super().__init__(master, dateformat=dateformat, firstweekday=firstweekday, **kwargs)
        self.button.configure(takefocus=False)

    def _on_date_ask(self):
        """Callback for pushing the date button"""
        _val = self.entry.get() or datetime.today().strftime(self._dateformat)
        try:
            self._startdate = datetime.strptime(_val, self._dateformat)
        except Exception as e:
            print("Date entry text does not match", self._dateformat)
            self._startdate = datetime.today()
            self.entry.delete(first=0, last=tk.END)
            self.entry.insert(
                tk.END, self._startdate.strftime(self._dateformat)
            )

        old_date = datetime.strptime(_val, self._dateformat)

        # get the new date and insert into the entry
        new_date = Querybox.get_date(
            parent=self.entry,
            startdate=old_date,
            firstweekday=self._firstweekday,
            bootstyle=self._bootstyle,
        )
        self.entry.delete(first=0, last=tk.END)
        self.entry.insert(tk.END, new_date.strftime(self._dateformat))
        self.entry.focus_force()
