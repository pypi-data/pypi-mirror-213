import json
import sys
from socket import socket, AF_INET, SOCK_STREAM

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

from const import USER_LIST_OK, MESSAGE_OK, MESSAGE_LIST_OK, ROOM_LIST_OK
from jim import Jim, MessageParser
from client_gui import MainWindow


class SockRecvSignal(QtCore.QThread):
    """ Мониторинг входящих сообщений от сервера """
    on_recv_data = pyqtSignal(str)

    def __init__(self, server_socket, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.server_socket = server_socket
        self.message = None

    def run(self):  # SocketClientGUI_connect(): message_monitor.start()
        """ QQThread: получает сообщение от сервера"""
        while True:
            self.message = self.server_socket.recv(1024)
            self.on_recv_data.emit(self.message.decode('utf-8'))  # -> SocketClientGUI_received_msg()


class SocketClientGUI:
    """ Сокет клиент. Подключается к серверу, запускает GUI интерфейс клиента и обрабатывает сообщения """
    def __init__(self, address='localhost', port=10000):
        self.address = (address, port)
        self.sock = socket(AF_INET, SOCK_STREAM)

        self.user_jim = Jim()
        self.user_parser = MessageParser(self.user_jim)
        self.is_not_auth = True

        self.window = MainWindow()
        self.message_monitor = SockRecvSignal(self.sock)

    # def connect_to_server(self):
        try:
            self.sock.connect(self.address)
            self.message_monitor.on_recv_data.connect(self.recv_msg, QtCore.Qt.BlockingQueuedConnection)
            self.window.on_send_data.connect(self.send_msg)  # , QtCore.Qt.QueuedConnection)

            self.message_monitor.start()  # Запускаем мониторинг входящих сообщений

        except OSError:
            QMessageBox.critical(self.window, 'Connection Errors', f'Try again next tim')
            sys.exit(1)

    def recv_msg(self, value):  # Пришло сообщение от сервера
        dict_ = json.loads(value)
        if self.is_not_auth:  # пользователь еще не зарегистрировался
            self.user_jim.user = self.user_parser.expect_ok_login(dict_)
            if not self.user_jim.user:  # ошибка регистрации
                QMessageBox.critical(self.window, 'Registration Errors', dict_.get('error'))
                return
            else:  # регистрация прошла успешно
                self.is_not_auth = False
                self.window.connected_ok(self.user_jim.user)
        else:  # для зарегистрированного пользователя
            code, l_msg = self.user_parser.srv_message_parser(dict_)
            if code == MESSAGE_OK:
                self.window.print_msg(dict_.get('author', '') == self.user_jim.user, l_msg[0])
            elif code == ROOM_LIST_OK:
                self.window.print_rooms(l_msg)  # список комнат
            elif code == USER_LIST_OK:
                self.window.print_users(l_msg)  # список пользователей
            elif code == MESSAGE_LIST_OK:
                self.window.print_messages(l_msg)  # список последних сообщений чата
            else:
                QMessageBox.warning(self.window, 'Message from the server', l_msg[0])

    def send_msg(self, message: str):  # Пришло сообщение для отправки на сервер
        json_msg = self.user_parser.kbd_message_parser(message)
        try:
            self.sock.send(json_msg.encode('utf-8'))
        except OSError:
            self.sock.close()
            sys.exit(2)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    sc_gui = SocketClientGUI()
    sc_gui.window.show()
    app.exec_()
