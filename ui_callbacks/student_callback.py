import dataclasses
from typing import Literal
import eel

from database import get_db
from services import *

db = get_db()



@eel.expose
def answer_student_group() -> List[StudentGroup]:
    try:
        student_group: List[StudentGroup] = [dataclasses.asdict(group) for group in get_student_group(db)]
    except ServiceException as e:
        return 'Группы не найдены'

    return student_group


@eel.expose
def create_ui_student(user: dict[
    Literal['user_id'] | Literal['full_name'] | Literal['group_id'] | Literal['email'], str
]):
    
    if int(user['role_id']) == Role.STUDENT.value['id'] or int(user['role_id']) == Role.ELDER.value['id']:
        switch_staus_user(db, Users(
        id=user['user_id'],
            login=None,
            password=None,
            email=user['email'],
            role_id=user['role_id'],
            status_account=StatusAccount.CONFIRMED.value['id']
        ))
        return post_student(db, Student(
            id=None,
            full_name=user['full_name'],
            group_id=user['group_id'],
            student_type_id=int(StudentType.Budget),
            user_id=user['user_id']
        ))
    elif int(user['role_id']) == Role.TEACHER.value['id']:
        switch_staus_user(db, Users(
        id=user['user_id'],
            login=None,
            password=None,
            email=user['email'],
            role_id=user['role_id'],
            status_account=StatusAccount.CONFIRMED.value['id']
        ))
        
        return post_teacher(db, Teacher(
            id=None,
            full_name=user['full_name'],
            subject_id = random.randint(1, 3),
        ))
    else:
        switch_staus_user(db, Users(
            id=user['user_id'],
            login=None,
            password=None,
            email=user['email'],
            role_id=user['role_id'],
            status_account=StatusAccount.CONFIRMED.value['id']
        ))
        return user['user_id']


@eel.expose
def answer_ui_student_by_user_id(user_id: int) -> Student:
    try:
        student: Student = get_student_by_user_id(db, user_id)
    except ServiceException as e:
        return 'Студент не найден'

    return dataclasses.asdict(student)


@eel.expose
def answer_ui_all_students_by_elder_group_id(user_id: int) -> List[Student]:
    try:
        elder: Student = get_student_by_user_id(db, user_id)
        students: List[Student] = [dataclasses.asdict(student) for student in get_all_students_by_elder_group_id(db, elder.group_id)]
    except ServiceException as e:
        return 'Студенты не найдены'

    return students


@eel.expose
def answer_ui_student_group_by_id(group_id: int) -> StudentGroup:
    try:
        group: StudentGroup = get_group_by_id(db, group_id)
    except ServiceException as e:
        return 'Группа не найдена'

    return dataclasses.asdict(group)


@eel.expose
def answer_ui_student_by_id(student_id: int) -> Student:
    try:
        student: Student = get_student_by_id(db, student_id)
    except ServiceException as e:
        return 'Студент не найден'

    return dataclasses.asdict(student)


@eel.expose
def answer_ui_student_group_statistics(group_id: int) -> list[StudentGroupStatistics]:
    try:
        statistics: list[StudentGroupStatistics] = [dataclasses.asdict(statistic) for statistic in get_students_group_statistics(db, group_id)]
    except ServiceException as e:
        return 'Статистика не найдена'

    return statistics


@eel.expose
def answer_iu_students_by_group_id(group_id: int) -> list[Student]:
    try:
        students: list[Student] = [dataclasses.asdict(student) for student in get_all_students_by_elder_group_id(db, group_id)]
    except ServiceException as e:
        return 'Студенты не найдены'

    return students