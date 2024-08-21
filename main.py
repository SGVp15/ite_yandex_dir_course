import datetime
import os
from datetime import date, timedelta

from config import yandex_dir
from course import Course
from parser import parse_for_course


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days) + 1
    for n in range(days):
        yield start_date + timedelta(n)


def create_dirs(course: Course):
    path_course = os.path.join(yandex_dir, str(course))
    for single_date in daterange(course.date_start, course.date_stop):
        path_full = os.path.join(path_course, single_date.strftime("%Y-%m-%d"))
        os.makedirs(path_full, exist_ok=True)
        print(path_full)


def main():
    with open('./course.txt', mode='r', encoding='utf-8') as f:
        s = f.read()
    courses = parse_for_course(s)
    for course in courses:
        create_dirs(course)


if __name__ == '__main__':
    main()
