import dataclasses
from typing import Literal
import eel

from database import get_db
from services import *

db = get_db()

@eel.expose
def answer_is_register(user: dict[Literal['login'] | Literal['password'] | Literal['email']]) -> Users:
    return isRegister(db, Users(
        id=None,
        login=user['login'],
        password=user['password'],
        email=user['email'],
        role_id=None,
        status_account=False
))

@eel.expose
def make_ui_register(user: dict[Literal['login'] | Literal['password'] | Literal['email']]) -> Users:
    return post_user(db, Users(
        id=None,
        login=user['login'],
        password=user['password'],
        email=user['email'],
        role_id=Role.STUDENT.value['id'],
        status_account=StatusAccount.NOT_CONFIRMED.value['id']))



@eel.expose
def make_ui_login(user: dict[Literal['password'] | Literal['email']]) -> Users:
    try:
        user = get_user(db, Users(
            id=None,
            login=None,
            password=user['password'],
            email=user['email'],
            role_id=None,
            status_account=None
        ))
    except ServiceException as e:
        return 'Почта или пароль не верны'

    return dataclasses.asdict(user)