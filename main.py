import datetime
import os
from datetime import date, timedelta

from UTILS.log import log
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
        if not os.path.exists(path_full):
            os.makedirs(path_full, exist_ok=True)
            log.info(f'[CREATE] {path_full}')


def rename_old_dirs():
    dirs = [f for f in os.listdir(yandex_dir) if os.path.isdir(os.path.join(yandex_dir, f))]
    for dir in dirs:
        # '2024-08-26 2024-08-30 ITILF4-online Громаков Zoom_1'
        words = dir.split(' ')
        try:
            date_course_str = list(map(int, words[1].split('-')))
            date_end_course = datetime.date(date_course_str[0], date_course_str[1], date_course_str[2])
            today = datetime.date.today()
            if date_end_course < today and is_empty_folders(os.path.join(yandex_dir, dir)) is False:
                new_name = f'{words[2]} {words[3]} {words[4]} {words[0]}'
                old_path = os.path.join(yandex_dir, dir)
                os.rename(old_path, os.path.join(yandex_dir, new_name))
                log.info(f'[RENAME] {old_path}')
        except (ValueError, IndexError):
            continue


def is_empty_folders(path):
    for root, dirs, files in os.walk(path):
        if not dirs and not files:
            return True
    return False


def main():
    with open('./course.txt', mode='r', encoding='utf-8') as f:
        s = f.read()
    courses = parse_for_course(s)
    now = datetime.datetime.now().date()
    courses = [x for x in courses if x.date_stop >= now]
    for course in courses:
        create_dirs(course)


if __name__ == '__main__':
    log.info('run')
    rename_old_dirs()
    main()
