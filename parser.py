import datetime
import re

from UTILS.log import log
from course import Course


def parse_for_course(s: str) -> [Course]:
    courses = []
    rows = s.split('\n')
    rows = [r for r in rows if r.strip()]
    for row in rows:
        elem = row.split('\t')
        try:
            for i, l in enumerate(elem):
                if '-online' in l:
                    break

            name = elem[i]
            teacher = elem[i + 2]
            site = elem[i + 7].split(' ')[0]

            date_start_str = elem[i + 3].split('.')
            date_start_str = list(map(int, date_start_str))

            date_stop_str = elem[i + 4].split('.')
            date_stop_str = list(map(int, date_stop_str))

            date_start = datetime.date(date_start_str[2], date_start_str[1], date_start_str[0])
            date_stop = datetime.date(date_stop_str[2], date_stop_str[1], date_stop_str[0])
            if re.findall(r'(zoom_\d)|(mts)', site.lower()):
                courses.append(Course(name, date_start, date_stop, teacher, site))
        except IndexError as e:
            log.error(e)
    return courses
