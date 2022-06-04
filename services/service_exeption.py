class ServiceException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'Ошибка: {}'.format(self.message)