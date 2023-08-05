from sigure_emulator import functions
from sigure_emulator import sigur_methods


class SigurEmulator:
    """ Класс, эмулирующий подключение по socket с реальным контроллером СКУД, имеет методы:
    send - для отправки команд, recv - для получения ответа.
    Так-же имеет метод engine, который обрабатывает ответы полученные из send и создает ответы, доступные для recv """
    def __init__(self,
                 name='SigurEmulator',
                 login="Administrator",
                 password="",
                 version="1.8",
                 points=4):
        self.name = name
        self.buffer = ''
        self.login = login
        self.password = password
        self.version = version
        self.auth = False
        self.points_dict = functions.create_points_dict(points)

    def send(self, command, *args, **kwargs):
        self.engine(command)
        return '\n{} got command: {}'.format(self.name, command)

    def engine(self, command):
        """ Обрабатывает полученную команду через send и сохраняет ответ в буффер self.buffer """
        command = command.decode()
        command = command.replace('\r\n', '')
        splitted = command.split(' ')
        command_tag = splitted[0]
        method = functions.get_method(command_tag)
        if method['status']:
            response = method['info'](*splitted, all_points_states=self.points_dict)
            self.buffer += response

    def recv(self, *args, **kwargs):
        buffer = self.buffer
        self.buffer = ''
        return buffer.encode()

    def connect(self, *args, **kwargs):
        print('\nConnecting to SigurEmulator naming {}...'.format(self.name))
