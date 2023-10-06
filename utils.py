import typing as tp
from config import WEEKDAY


def get_lessons_data(lesson) -> tp.Dict:
    lesson_data = {
        "id": lesson.id,
        "group": lesson.group,
        "day": lesson.day,
        "even_week": lesson.even_week,
        "subject": lesson.subject,
        "type": lesson.type,
        "time_start": lesson.time_start,
        "time_end": lesson.time_end,
        "teacher_name": lesson.teacher_name,
        "room": lesson.room,
        "address": lesson.address,
        "zoom_url": lesson.zoom_url
    }
    return lesson_data


def get_person_data(person) -> tp.Dict:
    person_data = {
        "id": person.id,
        "fio": person.fio,
        "gender": person.gender,
        "phone": person.phone,
        "email": person.email,
        "work": person.work,
        "education": person.education
    }
    return person_data


def get_group_data(group) -> tp.Dict:
    group_data = {
        "id": group.id,
        "name": group.name,
        "faculty": group.faculty,
        "direction": group.direction,
        "people_count": group.people_count
    }
    return group_data


def check_week(week_number) -> tp.Tuple:
    if not week_number.isdigit() and week_number != "EVEN" and week_number != "ODD":
        return None, None, True
    if week_number.isdigit():
        if int(week_number) < 1 or int(week_number) > 7:
            return None, None, True
        is_even, key = (1, "even_week") if int(week_number) % 2 == 0 else (0, "odd_week")
    else:
        is_even, key = (1, "even_week") if week_number == "EVEN" else (0, "odd_week")
    return is_even, key, False


def check_day(day) -> bool:
    if not day.isdigit() and day not in WEEKDAY:
        return False
    if day.isdigit() and (int(day) < 1 or int(day) > 7):
        return False
    return True
