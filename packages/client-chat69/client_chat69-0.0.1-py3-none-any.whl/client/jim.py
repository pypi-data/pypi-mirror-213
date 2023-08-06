import time
from json import dumps

from const import *


class Jim:
    def __init__(self, user=''):
        self.user = user
        self.room = CHAT_NAME

    @staticmethod
    def get_login(name: str, psw: str) -> str:  # "action": "login" — авторизация на сервере
        return dumps(dict(action=ACT_LOGIN, time=time.time(), login=dict(account_name=name, password=psw)))

    @staticmethod
    def get_cmd_login(name: str, psw: str) -> str:  # команда '##login##Ivan##123##' — регистрация на сервере
        return f'##{ACT_LOGIN}##{name}##{psw}##'

    @staticmethod
    def get_register(name: str, psw: str) -> str:  # "action": "register" — регистрация на сервере
        return dumps(dict(action=ACT_REG, time=time.time(), login=dict(account_name=name, password=psw)))

    @staticmethod
    def get_cmd_register(name: str, psw: str) -> str:  # команда '##register##Ivan##123##' — регистрация на сервере
        return f'##{ACT_REG}##{name}##{psw}##'

    def get_contacts(self, room: str) -> str:  # "action": "contacts" — получить список контактов
        self.room = room
        return dumps(dict(action=ACT_CONTACTS, time=time.time(), user=self.user, room=self.room))

    @staticmethod
    def get_cmd_contacts(room: str) -> str:  # команда '##contacts##' — запрос списка контактов
        return f'##{ACT_CONTACTS}##{room}##'

    def get_rooms(self) -> str:  # "action": "get_contacts" — получить список контактов '##get_contacts##'
        return dumps(dict(action=ACT_ROOMS, time=time.time(), user=self.user))

    @staticmethod
    def get_cmd_rooms() -> str:  # команда '##chats##' — запрос списка контактов
        return f'##{ACT_ROOMS}##'

    def get_messages(self) -> str:  # "action": "get_contacts" — получить список сообщений чата
        return dumps(dict(action=ACT_MESSAGES, time=time.time(), user=self.user))

    @staticmethod
    def get_cmd_messages() -> str:  # команда '##messages##' — запрос списка сообщений чата
        return '##messages##'

    def message(self, msg: str) -> str:  # "action": "msg" — простое сообщение пользователю или в чат;
        return dumps(dict(action=ACT_MSG, time=time.time(), author=self.user, to=self.room, message=msg))

    def join(self) -> str:  # "action": "join" — присоединиться к чату
        return dumps(dict(action=ACT_JOIN, time=time.time(), room=self.room))

    def presence(self) -> str:  # — присутствие. Сообщение для сервера о присутствии клиента online;
        return dumps(dict(
            action=ACT_PRESENCE, time=time.time(), type='status', user=dict(account_name=self.user, status="I'm here")))

    def leave(self) -> str:  # "action": "leave" — покинуть чат. (##leave)
        return dumps(dict(action=ACT_LEAVE, time=time.time(), room=self.room))

    def del_contact(self, user_id: str) -> str:  # "action": "del_contact" -контакт в список контактов (##del_contact)
        return dumps(dict(action=ACT_DEL_CONTACT, user_id=user_id, time=time.time(), user=self.user))

    def add_contact(self, new_user: str) -> str:  # "action": "add_contact"; команда: '##add_contact##'
        return dumps(dict(action=ACT_ADD_CONTACT, new_user=new_user, time=time.time(), user=self.user))

    @staticmethod
    def quit() -> str:  # "action": "quit" — отключение от сервера (##quit)
        return dumps(dict(action=ACT_QUIT))

    @staticmethod
    def probe() -> str:  # "action": "probe" - запрос отправляет сервер, клиент отвечает "presence"
        return dumps(dict(action=ACT_PROBE, time=time.time()))

    @staticmethod
    def response_login_ok(username: str):
        return dumps(dict(response=LOGIN_OK, time=time.time(), username=username))

    @staticmethod
    def response_ok(msg: str) -> str:  # Сообщение-ответ сервера: успешное завершение
        return dumps(dict(response=OK, time=time.time(), alert=msg))

    @staticmethod
    def response_err(code: int, msg: str):  # Сообщение-ответ сервера: ошибка
        return dumps(dict(response=code, time=time.time(), error=msg))

    @staticmethod
    def user_list(lst: list):  # Сообщение-ответ сервера: список пользователей
        return dumps(dict(response=USER_LIST_OK, time=time.time(), list=lst))

    @staticmethod
    def rooms_list(lst: list):  # Сообщение-ответ сервера: список пользователей
        return dumps(dict(response=ROOM_LIST_OK, time=time.time(), list=lst))


class MessageParser:

    def __init__(self, member_: Jim):
        self.str = ''
        self.member = member_  # NickName, password, room
        self.command_query = {
            ACT_QUIT: lambda _: sys.exit(0),
            ACT_LOGIN: lambda data: self.member.get_login(data[2], data[3]),  # login
            ACT_REG: lambda data: self.member.get_register(data[2], data[3]),  # registration
            ACT_CONTACTS: lambda data: self.member.get_contacts(data[2]),  # получить список пользователей чата
            ACT_ROOMS: lambda _: self.member.get_rooms(),  # получить список чатов
            ACT_JOIN: lambda _: self.member.join(),  # присоединиться к чату
            ACT_LEAVE: lambda _: self.member.leave(),  # покинуть чат
            ACT_MESSAGES: lambda _: self.member.get_messages(),  # получить последние сообщения чата
            ACT_ADD_CONTACT: lambda data: self.member.add_contact(data[2]),  # добавить контакт в чата
            ACT_DEL_CONTACT: lambda data: self.member.del_contact(data[2]),  # удалить контакт из чата
        }

    def get_message(self, data):
        return self.member.message(data[0])

    def kbd_message_parser(self, message: str) -> str:
        """ Разбор команд клиента, начинающихся с ## """
        l_msg: list[str] = [message, *message[2:].split('##')]  # ['##login##Ivan##123##', 'login', 'Ivan', '123', '']
        return self.command_query.get(l_msg[1], self.get_message)(l_msg)

    @staticmethod
    def srv_message_parser(dict_: dict) -> (int, list[str]):  # расшифровка ответов сервера
        """ Разбор сообщения принятых от сервера """
        if dict_.get('action', '') == ACT_MSG:
            return MESSAGE_OK, [f'{dict_.get("author", "")}: {dict_.get("message", "")}']
        if rsp := dict_.get('response', 0):
            if rsp:
                if rsp in LIST_RECEIVED:  # список пользователей, комнат
                    return rsp, dict_.get('list', [])
                msg = dict_.get('error', '') if rsp >= ERROR else dict_.get('alert', '')
                return rsp, [msg]
            else:
                return UNKNOWN_MESSAGE, "???: unrecognized server message"

    @staticmethod
    def expect_ok_login(dict_: dict) -> str:
        return dict_.get('username', '') if dict_.get('response', 0) == LOGIN_OK else ''


if __name__ == "__main__":
    member = Jim()
    inp = ['##get_contacts##Room2##', '##login##Ivan##123##', '##register##peter##password', 'hello!', '##hi##']
    parser = MessageParser(member)
    for inp_i in inp:
        s = parser.kbd_message_parser(inp_i)
        print(s)
