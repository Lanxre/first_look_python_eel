import eel

@eel.expose
def user_page():
    eel.show('user.html')

@eel.expose
def register_page():
    eel.show('register.html')

@eel.expose
def unregister_page():
    eel.show('unregister_user.html')

@eel.expose
def login_page():
    eel.show('login.html')

@eel.expose
def admin_page():
    eel.show('admin.html')


@eel.expose
def teacher_page():
    eel.show('teacher.html')


@eel.expose
def employee_page():
    eel.show('employee.html')