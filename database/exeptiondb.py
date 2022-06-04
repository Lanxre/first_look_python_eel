class StudentDbException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Ошибка подключения к базе данных StudentDbException, сообщение: {}'.format(self.message)