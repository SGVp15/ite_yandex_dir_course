import datetime
import os
from datetime import date, timedelta
from pathlib import Path

from UTILS.log import log
from config import YANDEX_DIR, INPUT_FILE
from course import Course
from parser import parse_for_course


def daterange(start_date: date, end_date: date):
    days = int((end_date - start_date).days) + 1
    for n in range(days):
        yield start_date + timedelta(n)


def create_dirs(course: Course):
    path_course = Path(YANDEX_DIR) / str(course)

    if path_course.exists():
        return

    if 'itilf4-online' in course.name.lower():
        path_course.mkdir(parents=True, exist_ok=True)
        log.info(f'[CREATE] {path_course}')
        return

    for single_date in daterange(course.date_start, course.date_stop):
        path_full = Path(path_course,
                         f'{single_date.strftime("%Y-%m-%d")} {course.name} {course.teacher}')
        if not path_full.exists():
            path_full.mkdir(parents=True, exist_ok=True)
            log.info(f'[CREATE] {path_full}')


def rename_old_dirs():
    dirs = [f for f in YANDEX_DIR.iterdir() if f.is_dir()]
    for dir in dirs:
        # '2024-08-26 2024-08-30 ITILF4-online Громаков Zoom_1'
        words = dir.name.split(' ')
        try:
            date_course_str = list(map(int, words[1].split('-')))
            date_end_course = datetime.date(date_course_str[0], date_course_str[1], date_course_str[2])
            today = datetime.date.today()
            if date_end_course < today and is_empty_folders_in_path(dir) is False:
                new_name = f'{words[2]} {words[3]} {words[4]} {words[0]}'
                Path.rename(dir, Path(YANDEX_DIR, new_name))
                log.info(f'[RENAME] {dir}')
        except (ValueError, IndexError):
            continue


def is_empty_folders_in_path(path):
    for root, dirs, files in os.walk(path):
        if not dirs and not files:
            return True
    return False


def create_folder_courses_from_file(file=INPUT_FILE):
    if not file.exists():
        log.warning(f'File not exist: {file}')
        return
    with open(file, mode='r', encoding='utf-8') as f:
        s = f.read()
    courses = parse_for_course(s)
    now = datetime.datetime.now().date()
    courses = [x for x in courses if x.date_stop >= now]
    for course in courses:
        create_dirs(course)


if __name__ == '__main__':
    log.warning('[ RUN ]')
    rename_old_dirs()
    create_folder_courses_from_file(INPUT_FILE)
