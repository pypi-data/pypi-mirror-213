from random import randint, sample
from datetime import datetime
import binascii
import faker
import hashlib
import os

import sqlalchemy as sa
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import default_comparator  # необходим для сборки проекта

from const import Permission, DB_PATH, CHAT_NAME

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __tableargs__ = {'comment': 'Пользователи'}

    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)
    salt = sa.Column(sa.String, nullable=False)
    public_key = sa.Column(sa.String)

    def __repr__(self):
        return f'User(id={self.id}, login={self.login}, hash={self.password}, salt={self.salt})'


class Room(Base):
    __tablename__ = 'rooms'
    __tableargs__ = {'comment': 'Комнаты со списками пользователей'}

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False, unique=True)

    def __repr__(self):
        return f'Room(id={self.id}, name={self.name})'


class History(Base):
    __tablename__ = 'history'
    __tableargs__ = {'comment': 'История подключений пользователя'}

    id = sa.Column(sa.Integer, primary_key=True)
    time = sa.Column(sa.DateTime, default=datetime.now)
    ip = sa.Column(sa.String)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    def __repr__(self):
        return f'History(id={self.id}, time={self.time}, ip={self.ip},  User_id={self.user_id})'


class RoomUser(Base):
    __tablename__ = 'rooms_users'
    __tableargs__ = {'comment': 'Список комнат и пользователей'}

    room_id = sa.Column(sa.Integer, sa.ForeignKey('rooms.id'), primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
    permission = sa.Column(sa.Integer, default=Permission.READ | Permission.WRITE)

    def __repr__(self):
        return f'RoomUser(room_id={self.room_id}, user_id={self.user_id}, permission={self.permission})'


class Message(Base):
    __tablename__ = 'messages'
    __tableargs__ = {'comment': 'Сообщения чата'}

    id = sa.Column(sa.Integer, primary_key=True)
    room_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('rooms.id'))
    msg = sa.Column(sa.String)
    time = sa.Column(sa.DateTime)

    def __repr__(self):
        return \
            f'Message(id={self.id}, user_id={self.user_id}, room_id={self.room_id}, msg={self.msg}, time={self.time})'


class ChatDb:
    """ Запросы к БД """
    def __init__(self, url=DB_PATH, echo=False):
        """Создаем подключение к БД"""
        engine = sa.create_engine(url=url, echo=echo)  # in-memory database, print log - false
        Base.metadata.create_all(engine)  # создаем таблицы в БД, определенные с помощью Base
        self.session: Session = sessionmaker(bind=engine)()  # Создаем объект сессии из фабрики

    def get_user_password(self, username: str) -> tuple:
        data = self.session.query(User.password, User.salt).filter_by(login=username)
        return (data.first()[0], data.first()[1]) if data.count() else ('', '')  # salt, hash пароля

    def insert_message(self, msg: str):
        self.session.add(Message(msg=msg))
        self.session.commit()

    def add_contact(self, login: str, password=''):
        self.session.add(User(login=login, password=password))
        self.session.commit()

    def del_contact(self, login: str):
        self.session.query(User).filter(User.login == login).delete()
        self.session.commit()

    def last_entries(self):
        iter_ = self.session.query(Message.msg).order_by(Message.id.desc()).limit(10).all()[::-1]
        return [i[0] for i in iter_]

    def list_of_users(self):
        iter_ = self.session.query(User.login).all()
        return [i[0] for i in iter_]

    def list_of_users_in_room(self, name_room: str) -> list[str]:
        try:
            users = {k: val for k, val in self.session.query(User.id, User.login).all()}
            id_room = self.session.query(Room.id).where(Room.name == name_room).first()[0]
            return [users[j[0]] for j in self.session.query(RoomUser.user_id).where(RoomUser.room_id == id_room).all()]
        except TypeError:
            return []

    def list_of_rooms(self):
        iter_ = self.session.query(Room.name).all()
        return [i[0] for i in iter_]

    def statistics_by_user(self, user_id: int):
        return self.session.query(History.id, History.time, History.ip).filter(History.user_id == user_id)

    def statistics_by_users_all(self):
        dict_cl = {}
        for id_, login_ in [i for i in self.session.query(User.id, User.login)]:
            dict_cl.update({(id_, login_): [i for i in self.statistics_by_user(id_)]})
        return dict_cl

    @staticmethod
    def hash_password(psw: str, salt=''):
        b_salt = salt.encode('utf-8') if salt else binascii.hexlify(os.urandom(32))
        b_hash = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', psw.encode('utf-8'), b_salt, 100000))
        return b_hash.decode('utf-8'), b_salt.decode('utf-8')

    def registrate_user(self, name: str, psw: str) -> bool:
        psw_hash, salt = self.hash_password(psw)  # создаем соль и hash пароля
        self.session.add(User(login=name, password=psw_hash, salt=salt, public_key=''))
        try:
            self.session.commit()
            return True
        except exc.SQLAlchemyError:  # пользователь с таким именем существует
            self.session.rollback()  # чтобы не вызвать 'PendingRollbackError' при следующем обращении к БД
            return False

    def authenticate_user(self, name: str, psw: str) -> bool:
        db_hash, db_salt, = self.get_user_password(name)  # забираем hash и password из базы
        calc_hash, _ = self.hash_password(psw, db_salt)  # вычисляем hash с солью по psw
        return db_hash == calc_hash


if __name__ == '__main__':

    def fill_test_data(session_: Session):  # заполнение пустой базы тестовыми данными
        f = faker.Faker()

        for i in range(1, 11):
            salt, psw_hash = ChatDb.hash_password(f'{i}')  # вычисляем hash с солью по psw
            session_.add(User(login=f'user{i}', password=psw_hash, salt=salt, public_key=''))

        session_.add(Room(name=CHAT_NAME))  # общий чат
        session_.add_all([Room(name=f'Room_{num:02}') for num in range(1, 4)])

        session_.add_all([
            History(time=f.date_time_this_year(), ip=f.ipv4(), user_id=randint(1, 10)) for _ in range(30)])

        session_.add(RoomUser(room_id=1, user_id=1, permission=Permission.READ | Permission.WRITE | Permission.MODER))
        session_.add_all([RoomUser(room_id=1, user_id=i) for i in range(2, 11)])

        session_.add(RoomUser(room_id=2, user_id=1, permission=Permission.READ | Permission.WRITE | Permission.MODER))
        session_.add_all([RoomUser(room_id=2, user_id=i) for i in sample(range(2, 11), 7)])

        session_.add(RoomUser(room_id=3, user_id=2, permission=Permission.READ | Permission.WRITE | Permission.MODER))
        session_.add_all([RoomUser(room_id=3, user_id=i) for i in sample(range(3, 11), 6)])

        session_.add(RoomUser(room_id=4, user_id=10, permission=Permission.READ | Permission.WRITE | Permission.MODER))
        session_.add_all([RoomUser(room_id=4, user_id=i) for i in sample(range(1, 10), 7)])

        session.add_all([Message(
            room_id=randint(1, 3), user_id=randint(1, 11), msg=f.text(max_nb_chars=30),
            time=f.date_time_this_year()) for _ in range(1, 50)])
        session_.commit()  # добавляем данные в таблицу


    def print_iter(iter_, info=''):
        print(f"\n        {info}:")
        [print(val) for val in iter_]


    # engine = sa.create_engine('sqlite:///:memory:', echo=False)  # in-memory database, print log - false
    # engine = sa.create_engine('sqlite:///chat.db', echo=False)  # in-memory database, print log - false
    # Base.metadata.create_all(engine)  # создаем таблицы в БД, определенные с помощью Base
    # session: Session = sessionmaker(bind=engine)()  # Создаем объект сессии из фабрики

    chat_db = ChatDb()
    session = chat_db.session

    if session.query(User).count() < 1:  # если записей user в БД не существует - заполнить тестовыми данными
        fill_test_data(session)

    print_iter(session.query(User), 'User: Все записи')

    # res = chat_db.registrate_user('user103', '103')
    # print(res)
    # b = chat_db.authenticate_user('user103', '103')
    # print(b)

    # print_iter(session.query(User), 'User: Все записи')
    # print_iter(session.query(Room), 'Room: Все записи')
    # print_iter(session.query(History).order_by(History.time), 'History: Все записи')
    print_iter(session.query(RoomUser), 'RoomUser: Все записи')
    # print_iter(session.query(Message), 'Message: Все записи')
    #
    # print('\nПоследние записи\n', chat_db.last_entries())
    # print('\nСписок пользователей\n', chat_db.list_of_users())
    #
    # print_iter(session.query(User).where(sa.or_(User.id == 2, User.id == 5)), 'where: User_id = 2 or 7')
    # print_iter(session.query(History).filter(History.user_id == 7).order_by(History.time),
    #            'filter: подключения User_id = 7 с сортировкой по date')
    # print_iter(session.query(History).order_by(History.time.desc()).limit(2),
    #            'Decs,limit: последние по времени 2 подключения')
    # print('\n', '       Количество записей в History = ', session.query(History).count())
    #
    print('\n', '       Владельцы и клиенты из RoomUser:')
    x = chat_db.list_of_users_in_room('Room_02')
    print(x)
    # try:
    #     users = {k: val for k, val in session.query(User.id, User.login).all()}
    #     id_room = session.query(Room.id).where(Room.name == 'uuu').first()[0]
    #     [print(users[j[0]]) for j in session.query(RoomUser.user_id).where(RoomUser.room_id == id_room).all()]
    # except TypeError:
    #     print('ошибка!!!')

    # users = {k: val for k, val in session.query(User.id, User.login).all()}
    # rooms = {k: val for k, val in session.query(Room.id, Room.name).all()}
    # [print(rooms[i], users[j]) for i, j in session.query(RoomUser.room_id, RoomUser.user_id).all()]

    # print_iter(session.query(User))
    # chat_db.del_contact('caroline_watson')
    # print_iter(session.query(User))
    # print_iter(chat_db.statistics_by_user(1))
    # print(chat_db.statistics_by_users_all())
