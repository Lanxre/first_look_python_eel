import dataclasses
from typing import Literal
import eel

from database import get_db
from services import *

db = get_db()

@eel.expose
def get_unregistered_users() -> List[Users]:
    try:
        unregistered_users: List[Users] = [dataclasses.asdict(user) for user in get_all_unregistered_users(db)]
        
    except ServiceException as e:
        return 'Пользователи не найдены'

    return unregistered_users


@eel.expose
def get_registered_users() -> List[Users]:
    try:
        registered_users: List[Users] = [dataclasses.asdict(user) for user in get_all_registered_users(db)]
    except ServiceException as e:
        return 'Пользователи не найдены'

    return registered_users


@eel.expose
def delete_ui_user_by_id(id: int):
    delete_user_by_id(db, id)

@eel.expose
def update_ui_user(user: Users):
    update_user(db, Users(
        id=user['user_id'],
        login=user['login'],
        password=user['password'],
        email=user['email'],
        role_id=user['role_id'],
        status_account=StatusAccount.CONFIRMED.value['id']

    ))

