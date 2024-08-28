import datetime
import re

from UTILS.log import log
from course import Course


def parse_for_course(s: str) -> [Course]:
    courses = []
    rows = s.split('\n')
    for row in rows:
        elem = row.split('\t')
        try:
            teacher = elem[3]
            name = elem[1]
            site = elem[8].split(' ')[0]
            date_start_str = elem[4].split('.')
            date_start_str = list(map(int, date_start_str))

            date_stop_str = elem[5].split('.')
            date_stop_str = list(map(int, date_stop_str))

            date_start = datetime.date(2000 + date_start_str[2], date_start_str[1], date_start_str[0])
            date_stop = datetime.date(2000 + date_stop_str[2], date_stop_str[1], date_stop_str[0])
            if re.findall(r'_\d', site):
                courses.append(Course(name, date_start, date_stop, teacher, site))
        except IndexError as e:
            log.error(e)
    return courses
