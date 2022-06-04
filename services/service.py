import re
from database import Database
from models import *
from typing import List
from .service_exeption import ServiceException

def get_all_admins(db: Database) -> List[Users]:
    admins = db.cursor.execute("SELECT * FROM users WHERE role_id = ?", (Role.ADMIN.value['id'],)).fetchall()
    return list(map(lambda admin: Users(*admin), admins))


def post_user(db: Database, user: Users) -> Users:
    db.cursor.execute("INSERT INTO users(login, password, email, role_id, status_account) VALUES (?, ?, ?, ?, ?)",
     (user.login, user.password, user.email, user.role_id, user.status_account))
    db.conn.commit()
    return user

def get_user(db: Database, user: Users) -> Users:
    try:
        user = Users(*db.cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?",
     (user.email, user.password)).fetchone())
    except TypeError:
        raise ServiceException(f"Пользователь с email: '{user.email}' и паролем: '{user.password}' не найден")

    return user 


def get_all_unregistered_users(db: Database) -> List[Users]:
    unregistered_users = db.cursor.execute("SELECT * FROM users WHERE status_account = ?", (0,)).fetchall()
    return list(map(lambda user: Users(*user), unregistered_users))

def get_all_registered_users(db: Database) -> List[Users]:
    registered_users = db.cursor.execute("SELECT * FROM users WHERE status_account = ?", (1,)).fetchall()
    return list(map(lambda user: Users(*user), registered_users))

def isRegister(db: Database, user: Users) -> bool:
    return db.cursor.execute("SELECT * FROM users WHERE email = ?",
     (user.email,)).fetchone() is not None

def get_student_group(db: Database) -> List[StudentGroup]:
    student_group = db.cursor.execute("SELECT * FROM StudentGroup").fetchall()
    return list(map(lambda group: StudentGroup(*group), student_group))

def switch_staus_user(db: Database, user: Users):
    db.cursor.execute("UPDATE users SET status_account = ?, role_id = ? WHERE id = ?", (user.status_account, user.role_id ,user.id))
    db.conn.commit()

def post_student(db: Database, student: Student) -> Student:
    db.cursor.execute("INSERT INTO students(full_name, group_id, truancy_num, student_type_id, user_id) VALUES (?, ?, ?, ?, ?)",
     (student.full_name, student.group_id, student.truancy_num, student.student_type_id, student.user_id))
    db.conn.commit()
    return student

def delete_user_by_id(db: Database, id: int):
    db.cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    db.conn.commit()

def update_user(db: Database, user: Users):
    db.cursor.execute("UPDATE users SET login = ?, password = ?, email = ?, role_id = ? WHERE id = ?",
     (user.login, user.password, user.email, user.role_id, user.id))
    db.conn.commit()

def get_role_name(db: Database) -> List[Roles]:
    roles = db.cursor.execute("SELECT * FROM Role").fetchall()
    return list(map(lambda role: Roles(*role), roles))


def get_student_by_user_id(db: Database, user_id: int) -> Student:
    student = db.cursor.execute("SELECT * FROM students WHERE user_id = ?", (user_id,)).fetchone()
    return Student(*student) if student else None


def get_student_perfonce(db: Database, student_id: int) -> List[Performance]:
    student_perfomance = db.cursor.execute("SELECT * FROM performance WHERE student_id = ?", (student_id,)).fetchall()
    return list(map(lambda perf: Performance(*perf), student_perfomance))

def get_all_subjects(db: Database) -> List[Subject]:
    subjects = db.cursor.execute("SELECT * FROM Subject").fetchall()
    return list(map(lambda subject: Subject(*subject), subjects))


def get_all_students_by_elder_group_id(db: Database, elder_group_id: int) -> List[Student]:
    students = db.cursor.execute("SELECT * FROM students WHERE group_id = ?", (elder_group_id,)).fetchall()
    return list(map(lambda student: Student(*student), students))

def post_performance(db: Database, performance: Performance) -> Performance:
    db.cursor.execute("INSERT INTO performance(subject_id, student_id, mark, mark_date, teacher_mark) VALUES (?, ?, ?, ?, ?)",
     (performance.subject_id, performance.student_id, performance.mark, performance.mark_date, performance.teacher_mark))
    db.conn.commit()


def post_teacher(db: Database, teacher: Teacher) -> Teacher:
    db.cursor.execute("INSERT INTO Teachers(full_name, subject_id) VALUES (?, ?)",
     (teacher.full_name, teacher.subject_id))
    db.conn.commit()
    return teacher


def get_teacher_by_user_id(db: Database, user_id: int) -> Teacher:
    teacher = db.cursor.execute("SELECT * FROM Teachers WHERE user_id = ?", (user_id,)).fetchone()
    return Teacher(*teacher) if teacher else None

def get_teacher_subjects(db: Database, user_id: int) -> Subject:
    subjects = db.cursor.execute("Select subject_id, name from Teachers inner join Subject on Teachers.subject_id = Subject.id where user_id = ?", (user_id,)).fetchall()
    return list(map(lambda subject: Subject(*subject), subjects))

def get_performance_by_subject_id(db: Database, subject_id: int) -> List[Performance]:
    performances = db.cursor.execute("SELECT * FROM performance WHERE subject_id = ? AND teacher_mark = 0", (subject_id,)).fetchall()
    return list(map(lambda performance: Performance(*performance), performances))


def get_student_by_id(db: Database, student_id: int) -> Student:
    student = db.cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    return Student(*student) if student else None

def get_group_by_id(db: Database, group_id: int) -> StudentGroup:
    group = db.cursor.execute("SELECT * FROM StudentGroup WHERE id = ?", (group_id,)).fetchone()
    return StudentGroup(*group) if group else None

def put_performance(db: Database, performance: Performance):
    db.cursor.execute("UPDATE performance SET teacher_mark = ?, mark = ? WHERE student_id = ?",
     (performance.teacher_mark, performance.mark, performance.student_id))
    db.conn.commit()


def get_count_student_perf(db: Database, student_id: int) -> int:
    count = db.cursor.execute("SELECT COUNT(*) FROM performance WHERE student_id = ? and mark = 1 and teacher_mark = 1", (student_id,)).fetchone()
    return count[0]

def get_all_groups(db: Database) -> List[StudentGroup]:
    groups = db.cursor.execute("SELECT * FROM StudentGroup").fetchall()
    return list(map(lambda group: StudentGroup(*group), groups))


def get_students_group_statistics(db: Database, group_id: int) -> list[StudentGroupStatistics]:

    sql = "Select full_name, Count(*) as 'Количество пропусков' from Students inner join Performance on Students.id = Performance.student_id where Students.group_id = ? and teacher_mark = 1 and mark = 1 group by full_name"
    students_group_statistics = db.cursor.execute(sql, (group_id,)).fetchall()
    return list(map(lambda student_group_statistics: StudentGroupStatistics(*student_group_statistics), students_group_statistics))


def get_performance_by_student_id(db: Database, student_id: int) -> list[Performance]:
    performances = db.cursor.execute("SELECT * FROM performance WHERE student_id = ?", (student_id,)).fetchall()
    return list(map(lambda performance: Performance(*performance), performances))