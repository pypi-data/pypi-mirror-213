from pathlib import Path
from enum import IntFlag


# Права доступа
class Permission(IntFlag):
    READ = 1  # разрешение на просмотр сообщений в комнате
    WRITE = 2  # разрешение писать сообщения в комнате
    MODER = 4  # модератор


# Протокол JIM значения ключа ACTION:
ACT_LOGIN = 'login'
ACT_REG = 'register'
ACT_CONTACTS = 'get_contacts'
ACT_ROOMS = 'get_rooms'
ACT_MESSAGES = 'get_messages'
ACT_JOIN = 'join'
ACT_MSG = 'msg'
ACT_PRESENCE = 'presence'
ACT_LEAVE = 'leave'
ACT_DEL_CONTACT = 'del_contact'
ACT_ADD_CONTACT = 'add_contact'
ACT_QUIT = 'quit'
ACT_PROBE = 'probe'

CHAT_NAME = 'All chats'

OK = 200  # OK от сервера
MESSAGE_OK = 201  # Получено сообщение в чат
MESSAGE_LIST_OK = 296  # Получен список сообщений чата
ROOM_LIST_OK = 297  # Получен список комнат
USER_LIST_OK = 298  # Получен список пользователей
LOGIN_OK = 299  # корректный вход в чат
ERROR = 400  # получено сообщение с ошибкой
UNKNOWN_MESSAGE = 0

LIST_RECEIVED = (MESSAGE_LIST_OK, ROOM_LIST_OK, USER_LIST_OK)

# Сокет
SERVER_ADDRESS = ''
CLIENT_ADDRESS = '127.0.0.1'
PORT = 10000
BLOCK_LEN = 4096

DB_PROTOCOL = 'sqlite:///'
DB_NAME = 'chat.db'
DB_FILE_PATH = Path.cwd() / DB_NAME
DB_PATH = DB_PROTOCOL + str(DB_FILE_PATH)
