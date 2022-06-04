import dataclasses
from typing import Literal
import eel

from database import get_db
from services import *

db = get_db()


@eel.expose
def answer_ui_role_name() -> List[Role]:
    try:
        role_name: List[Role] = [dataclasses.asdict(role) for role in get_role_name(db)]
    except ServiceException as e:
        return 'Роли не найдены'

    return role_name




@eel.expose
def answer_ui_perfomance_student_by_user_id(user_id: int) -> List[Performance]:
    try:
        student: Student = get_student_by_user_id(db, user_id)
        student_perf: List[Performance] = \
            [dataclasses.asdict(perf) for perf in get_student_perfonce(db, student.id)]

    except ServiceException as e:
        return 'Error'
    
    return student_perf


@eel.expose
def answer_ui_all_subjects() -> List[Subject]:
    try:
        subjects: List[Subject] = [dataclasses.asdict(subject) for subject in get_all_subjects(db)]
    except ServiceException as e:
        return 'Предметы не найдены'

    return subjects




@eel.expose
def answer_ui_post_performance_student(performances: List[Performance]):
    try:
        for perf in performances:
            post_performance(db, Performance(
                id=None,
                student_id=perf['student_id'],
                subject_id=perf['subject_id'],
                mark=perf['mark'],
                mark_date=perf['mark_date'],
                teacher_mark=PerformanceMark.TEACHER_MARK_DONT_WATCH.value['id']
            ))
    except ServiceException as e:
        return 'Error'
    
    return 'Оценки добавлены'



@eel.expose
def answer_ui_teacher_by_user_id(user_id: int) -> Teacher:
    try:
        teacher: Teacher = get_teacher_by_user_id(db, user_id)
    except ServiceException as e:
        return 'Преподаватель не найден'

    return dataclasses.asdict(teacher)


@eel.expose
def answer_ui_teacher_subjects_by_user_id(user_id: int) -> List[Subject]:
    try:
        subjects: List[Subject] = [dataclasses.asdict(subject) for subject in get_teacher_subjects(db, user_id)]
        
    except ServiceException as e:
        return 'Преподаватель не найден'

    return subjects



@eel.expose
def performances_student_by_subject_id(subject_id: int) -> List[Performance]:
    try:
        performances: List[Performance] = [dataclasses.asdict(performance) for performance in get_performance_by_subject_id(db, subject_id)]
    except ServiceException as e:
        return 'Оценки не найдены'

    return performances




@eel.expose
def send_performances(performances: List[Performance]):
    try:
        for perf in performances:
            put_performance(db, Performance(
                id=None,
                student_id=perf['student_id'],
                subject_id=perf['subject_id'],
                mark=PerformanceMark.ELDER_MARK_GOOD.value['id']\
                     if perf['teacher_mark'] == PerformanceMark.TEACHER_MARK_GOOD.value['id']
                     else PerformanceMark.ELDER_MARK_BAD.value['id'],
                mark_date=perf['mark_date'],
                teacher_mark= perf['teacher_mark']
            ))
    except ServiceException as e:
        return 'Error'


@eel.expose
def answer_ui_count_student_perf(student_id: int) -> int:
    try:
        count_perf: int = get_count_student_perf(db, student_id)
    except ServiceException as e:
        return 'Оценок не найдено'

    return count_perf


@eel.expose
def answer_ui_all_groups() -> list[StudentGroup]:
    try:
        groups: List[StudentGroup] = [dataclasses.asdict(group) for group in get_all_groups(db)]
    except ServiceException as e:
        return 'Группы не найдены'

    return groups


@eel.expose
def answer_ui_performance_by_student_id(student_id: int) -> List[Performance]:
    try:
        performance: List[Performance] = [dataclasses.asdict(perf) for perf in get_performance_by_student_id(db, student_id)]
    except ServiceException as e:
        return 'Оценки не найдены'

    return performance