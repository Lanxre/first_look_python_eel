import random

from dataclasses import dataclass
from enum import Enum

class Role(Enum):
    """
    Enum class for roles
    """
    ADMIN = {"id": 1, "name": 'Администратор'}
    TEACHER = {"id": 2, "name": 'Преподователь'}
    EMPLOYEE = {"id": 3, "name": 'Работник Деконата'}
    ELDER = {"id": 4, "name": 'Староста'}
    STUDENT = {"id": 5, "name": 'Абитуриент'}
    

class PerformanceMark(Enum):
    """
    Enum class for teacher marks
    """
    ELDER_MARK_GOOD = {"id": 0, "name": 'Присутствие на занятии, ошибки в представлении и прочее'}
    ELDER_MARK_BAD = {"id": 1, "name": 'Отсутствие на занятии'}
    TEACHER_MARK_DONT_WATCH = {"id": 0, "name": 'Преподаватель не поставил оценку'}
    TEACHER_MARK_BAD = {"id": 1, "name": 'Проверено преподователем, отсутствие на занятии'}
    TEACHER_MARK_GOOD = {"id": 2, "name": 'Проверено преподователем, присутствие на занятии, ошибки в представлении и прочее'}


class StatusAccount(Enum):
    """
    Enum class for status account
    """
    CONFIRMED = {"id": 1, "name": 'потвержден'}
    NOT_CONFIRMED = {"id": 0, "name": 'не подтвержден'}


class StudentType(Enum):

    Budget = 1, 'Бюджетный'
    Payer = 2, 'Платник'

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.type = name
        return member

    def __int__(self):
        return self.value


@dataclass
class StudentGroupStatistics():
    """
    Class for statistics of student group
    """
    student_name : str
    count_performance_marks : int


@dataclass
class Users:
    id: int
    login: str
    password: str
    email: str
    role_id: Role
    status_account: bool

@dataclass
class StudentGroup:
    id: int
    name: str


@dataclass
class Student:
    id: int
    full_name: str
    group_id: str
    student_type_id: int = random.choice([1, 2])
    user_id: int | None = None

@dataclass
class Roles:
    id: int
    name: str

@dataclass
class Performance:
    id: int
    mark: int
    student_id: int
    subject_id: int
    mark_date: str
    teacher_mark: int


@dataclass
class Subject:
    id: int
    name: str


@dataclass
class Teacher:
    id: int
    full_name: str
    subject_id: int
    user_id: int | None = None


@dataclass
class StudentGroup:
    id: int
    name: str