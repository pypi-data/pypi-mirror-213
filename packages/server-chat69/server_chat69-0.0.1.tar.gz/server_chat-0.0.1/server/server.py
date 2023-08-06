import time
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM
import select
import json

from server_db import ChatDb
from jim import Jim
from const import SERVER_ADDRESS, PORT, BLOCK_LEN, \
    ACT_LOGIN, ACT_REG, ACT_JOIN, ACT_MSG, ACT_LEAVE, ACT_CONTACTS, ACT_MESSAGES, ACT_ADD_CONTACT, ACT_DEL_CONTACT, \
    ACT_ROOMS


class MessageParser:
    """ Класс анализирует входное сообщение клиента, выполняет нужные действия и дает ответ """
    def __init__(self, chat_db, sockets_dict):
        self.chat_db: ChatDb = chat_db
        self.sockets_dict = sockets_dict
        self.sock = None
        self.jim_dict = {}
        self.jim_str = ''
        self.functions = {ACT_LOGIN: self.login, ACT_REG: self.login, ACT_CONTACTS: self.get_contacts,
                          ACT_ROOMS: self.get_rooms,
                          ACT_JOIN: self.welcome_proc, ACT_MSG: self.message_proc, ACT_LEAVE: self.leave_proc,
                          ACT_MESSAGES: self.get_messages,
                          ACT_ADD_CONTACT: self.add_contact, ACT_DEL_CONTACT: self.del_contact, }

    def login(self):
        user = self.jim_dict.get('login', {}).get('account_name', '')
        password = self.jim_dict.get('login', {}).get('password', '')
        if not all([user, password]):
            return [1, [Jim.response_err(400, 'The fields is required to be filled'), ]]
        if self.jim_dict.get('action', {}) == ACT_REG:  # регистрация нового пользователя
            if not self.chat_db.registrate_user(user, password):
                return [1, [Jim.response_err(400, f'User name "{user}" already registered'), ]]
        if self.chat_db.authenticate_user(user, password):
            return [1, [Jim.response_err(400, f'No user with name "{user}"'), ]]
        self.sockets_dict[self.sock] = user  # присвоить имя пользователя сокету
        # добавить в таблицу History

        return [1, [Jim.response_login_ok(user)]]

    def get_contacts(self):
        room = self.jim_dict.get('room', '')
        return [1, [Jim.user_list(self.chat_db.list_of_users_in_room(room)), ]]

    def get_rooms(self):
        return [1, [Jim.rooms_list(self.chat_db.list_of_rooms()), ]]

    def get_messages(self):
        return [1, [*self.chat_db.last_entries()]]

    def add_contact(self):
        self.chat_db.add_contact(login=self.jim_dict.get('user_id'))
        return [1, [Jim.response_ok('Contact added to the chat room!'), ]]

    def del_contact(self):
        self.chat_db.del_contact(login=self.jim_dict.get('user_id'))
        return [1, [Jim.response_ok('Contact added to the chat room!'), ]]

    @staticmethod
    def welcome_proc():
        return [1, [Jim.response_ok('Welcome to the chat room!')]]

    def message_proc(self):
        self.chat_db.insert_message(self.jim_str)
        return [0, [self.jim_str, ]]

    @staticmethod
    def leave_proc():
        return [1, [Jim.response_ok('By!'), ]]

    @staticmethod
    def error_proc():
        return [1, [Jim.response_err(400, 'Incorrect message'), ]]

    def parse_message(self, message: str, sock: socket):  #
        """ Разбор полученного сообщения и вызов соответствующей функции для формирования ответа."""
        """
        :param sock: socket, с которого пришло сообщение message
        :param message: JIM строка, полученная от клиента
        :return: структура [0 | 1, [JIM-строка ответа сервера, JIM-строка, JIM-строка, ...]
                            0-широковещательное сообщение, 1-ответ клиенту
        """
        self.jim_str = message
        self.sock = sock
        try:
            self.jim_dict = json.loads(message)
        except json.JSONDecodeError:
            self.jim_dict = {}
        return self.functions.get(self.jim_dict.get("action"), self.error_proc)()


class Server:
    """ Сокет сервер (Низкоуровневый API) использует системный вызов select.select(). """
    """Select() всегда возвращает готовые сокеты. Блокировка отсутствует """
    def __init__(self, address='', port=10000):
        """
        :param address: IP адрес сокета
        :param port: порт
        """
        self.address = (address, port)
        self.chat_db = ChatDb()
        self.sockets_dict = {}
        self.msg_parser = MessageParser(self.chat_db, self.sockets_dict)

    def send_response(self, data: str, sock: socket, all_clients: list):
        """ Ответ сервера клиенту, от которого получено сообщение (клиентам - широковещательно)"""
        type_sending, messages = self.msg_parser.parse_message(data, sock)
        sockets = [sock] if type_sending else all_clients[1:]  # 0 - всем; 1 - клиенту
        for next_sock in sockets:
            for next_msg in messages:
                try:
                    next_sock.sendall(next_msg.encode('utf-8'))  # Ответ клиенту
                    time.sleep(0.001)  # В клиенте такая же задержка (иначе все сообщения идут одним пакетом)
                except OSError:  # Сокет недоступен, клиент отключился
                    self.close_connection(sock)

    def close_connection(self, del_socket: socket) -> list[socket]:
        """ Закрывает соединение с клиентом"""
        if del_socket in self.sockets_dict:
            print(f'Client [{del_socket.fileno()}, {del_socket.getpeername()}] disconnected')
            del self.sockets_dict[del_socket]
            del_socket.close()  # Закрываем соединение
        return list(self.sockets_dict.keys())

    def run(self):
        """ Основной цикл сокет-сервера """
        with socket(AF_INET, SOCK_STREAM) as server_socket:
            server_socket.setblocking(False)  # устанавливаем неблокирующий режим серверного сокета
            server_socket.bind(self.address)  # привязываем сокет к адресу
            server_socket.listen()  # переводим сервер для приема подключений
            self.sockets_dict = {server_socket: 'server'}  # список подключенных сокетов
            message_queues = Queue()  # входная очередь сообщений (socket, message)
            print(f"Running server on {server_socket.fileno()}: '{server_socket}'")

            while self.sockets_dict:
                sockets_list = list(self.sockets_dict.keys())
                r, _, e = select.select(sockets_list, [], sockets_list)  # Проверяем наличие событий ввода
                print(f"r:{[i.fileno() for i in r]}")
                for sock in r:  # Перебираем сокеты на прослушивание
                    if sock is server_socket:  # Регистрация нового соединение:
                        new_socket, client_address = sock.accept()  # принять соединение от клиента
                        new_socket.setblocking(False)  # устанавливаем неблокирующий режим нового клиентского сокета
                        self.sockets_dict[new_socket] = 'Anonymous'  # новое соединение в список для прослушивания
                        sockets_list = list(self.sockets_dict.keys())
                        print(f"Соединение установлено с {client_address}")
                    else:  # Чтение данных
                        if sock in e:
                            sockets_list = self.close_connection(sock)
                            continue
                        try:
                            if data := sock.recv(BLOCK_LEN).decode('utf-8'):
                                message_queues.put((sock, data,))
                            else:
                                sockets_list = self.close_connection(sock)
                        except OSError:
                            sockets_list = self.close_connection(sock)
                while not message_queues.empty():
                    sock, data = message_queues.get_nowait()
                    self.send_response(data, sock, sockets_list)


if __name__ == "__main__":
    Server(SERVER_ADDRESS, PORT).run()

    # chat = MessageParser()
    # s0 = '{"action": "join", "time": 1665998251.5553887, "room": "my chat"}'
    # s = chat.parse_message(s0)
    # print('\n'.join([f"{x[0]},{x[1]}" for x in s]))
    # s1 = '{"action": "msg", "time": 1665998251.5553887, "to": "my chat", "author": "user1", "message": "Message!!!"}'
    # print(chat.parse_message(s1))
