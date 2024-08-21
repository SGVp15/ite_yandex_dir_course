import datetime


class Course:
    def __init__(self, name, date_start: datetime.date, date_stop: datetime.date, teacher='', site=''):
        self.name: str = name
        self.days = (date_stop - date_start).days
        self.date_start = date_start
        self.date_stop = date_stop
        self.teacher: str = teacher
        self.site: str = site

    def __str__(self):
        # 2024-08-19 CPI-online Аношин Zoom_1
        return f'{self.date_start} {self.date_stop} {self.name} {self.teacher.split(' ')[0]} {self.site}'
