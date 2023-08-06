import time

from PyQt5 import QtWidgets, uic, QtGui, QtCore, Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QListView, QMessageBox, QGraphicsColorizeEffect

from jim import Jim, CHAT_NAME


class DlgLogin(QtWidgets.QDialog):
    """ Диалоговое окно логина и регистрации """
    on_filled_login = pyqtSignal(str)

    def __init__(self):
        super(DlgLogin, self).__init__()
        uic.loadUi('ui/dlg_login_window.ui', self)

        self.message = 'empty'

        self.setGeometry(300, 300, 500, 300)
        self.setModal(True)  # главное окно недоступно
        self.le_username: QLineEdit = self.findChild(QLineEdit, "le_username")
        self.le_password: QLineEdit = self.findChild(QLineEdit, "le_password")
        self.btn_register: QPushButton = self.findChild(QPushButton, "btn_register")
        self.btn_login: QPushButton = self.findChild(QPushButton, "btn_login")
        self.btn_login.setDefault(True)

        self.btn_login.clicked.connect(self.clicked_login)
        self.btn_register.clicked.connect(self.clicked_registration)

    def clicked_login(self):
        self.form_processing(True)

    def clicked_registration(self):
        self.form_processing(False)

    def form_processing(self, is_login: bool):
        name, psw = self.le_username.text(), self.le_password.text()
        if all([name, psw]):
            self.message = Jim.get_cmd_login(name, psw) if is_login else Jim.get_cmd_register(name, psw)
            self.close()
            self.on_filled_login.emit(self.message)
        else:
            QMessageBox.critical(self, 'Registration Errors', 'Not all fields of the form are filled')

    def display(self):
        self.le_username.clear()
        self.le_password.clear()
        self.show()


class MainWindow(QtWidgets.QMainWindow):
    """ Главное окно клиентского приложения """
    on_send_data = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('ui/main_window.ui', self)

        self.user_name = ''

        self.setGeometry(100, 100, 800, 1000)
        self.lbl_user_name = self.findChild(QLabel, "lbl_user_name")
        self.lbl_user_name.setStyleSheet('color: Olive')
        self.lbl_owner_name = self.findChild(QLabel, "lbl_owner_name")
        self.lbl_owner_name.setStyleSheet('color: SaddleBrown')
        self.lbl_owner_name.setHidden(True)
        self.btn_login: QPushButton = self.findChild(QPushButton, "btn_login")
        self.btn_login.setStyleSheet("background-color: Cornsilk")
        self.btn_send: QPushButton = self.findChild(QPushButton, "btn_send")
        self.btn_send.setStyleSheet("background-color: Cornsilk")
        self.le_msg: QLineEdit = self.findChild(QLineEdit, "le_msg")

        self.lbl_chat = self.findChild(QLabel, "lbl_chat")
        self.lbl_chat.setStyleSheet('color: SaddleBrown')
        # self.lbl_chat.setHidden(True)
        self.lv_chat: QListView = self.findChild(QListView, "lv_chat")
        self.lv_chat_sm = QtGui.QStandardItemModel(parent=self)
        self.lv_chat.setModel(self.lv_chat_sm)

        self.lbl_rooms = self.findChild(QLabel, "lbl_rooms")
        self.lbl_rooms.setStyleSheet('color: Olive')
        self.lv_rooms: QListView = self.findChild(QListView, "lv_rooms")
        self.lv_rooms_sm = QtGui.QStandardItemModel(parent=self)
        self.lv_rooms.setModel(self.lv_rooms_sm)
        self.lv_rooms.doubleClicked.connect(self.dbl_clicked_room_item)

        self.lbl_users = self.findChild(QLabel, "lbl_users")
        self.lbl_users.setStyleSheet('color: Olive')
        self.lv_users: QListView = self.findChild(QListView, "lv_users")
        self.lv_users_sm = QtGui.QStandardItemModel(parent=self)
        self.lv_users.setModel(self.lv_users_sm)

        self.btn_login.clicked.connect(self.clicked_login_btn)
        self.btn_send.clicked.connect(self.clicked_send)

        self.set_widgets_state(send=False)

        self.dlg_login = DlgLogin()
        self.dlg_login.on_filled_login.connect(self.closed_child)

    def dbl_clicked_room_item(self):
        room = self.lv_rooms.currentIndex().data()
        self.lbl_chat.setText(room)
        LVM.list_clear(self.lv_users)
        self.on_send_data.emit(Jim.get_cmd_contacts(room))

    def closed_child(self, message):
        self.on_send_data.emit(message)

    def clicked_login_btn(self):
        self.dlg_login.display()

    def clicked_send(self):
        if message := self.le_msg.text():
            self.le_msg.clear()
            self.on_send_data.emit(message)

    def connected_ok(self, username: str):
        self.user_name = username
        self.set_widgets_state(login=False)
        self.on_send_data.emit(Jim.get_cmd_contacts(CHAT_NAME))
        time.sleep(0.05)
        self.on_send_data.emit(Jim.get_cmd_rooms())

    def set_widgets_state(self, login=True, send=True):
        # self.btn_login.setText(f"{'Check In' if login else 'Check out'}")
        self.btn_login.setHidden(not login)
        self.lbl_owner_name.setText(f"{'Anonymous' if login else self.user_name}")
        self.lbl_owner_name.setHidden(login)
        self.lbl_chat.setText(f"{'?' if login else CHAT_NAME}")
        self.btn_send.setEnabled(send)
        self.le_msg.setEnabled(send)

    def print_msg(self, is_author: bool, msg: str):
        color, align = ('green', 'right') if is_author else ('blue', 'left')
        LVM.list_append(self.lv_chat, msg, color=color, align=align)

    def print_users(self, l_msg: list[str]):
        [LVM.list_append(self.lv_users, msg) for msg in l_msg]

    def print_rooms(self, l_msg: list[str]):
        [LVM.list_append(self.lv_rooms, msg) for msg in l_msg]

    def print_messages(self, l_msg: list[str]):
        [LVM.list_append(self.lv_chat, msg) for msg in l_msg]


class LVM:
    """ Класс реализует основные методы работы с QListView (модель QStandardItemModel) """
    COLORS = dict(black=QColor(0, 0, 0), red=QColor(150, 50, 50), blue=QColor(50, 100, 150), green=QColor(92, 184, 92))
    ALIGN = dict(left=QtCore.Qt.AlignLeft, right=QtCore.Qt.AlignRight)

    @staticmethod
    def list_append(lv: QListView, s: str, color='black', align='left'):
        """ Добавляет элемент в конец списка """
        item = QtGui.QStandardItem(s)
        txt_align = LVM.ALIGN.get(align, QtCore.Qt.AlignLeft)
        txt_color = LVM.COLORS.get(color, QColor(0, 0, 0))
        item.setData(QtGui.QColor(txt_color), QtCore.Qt.TextColorRole)
        item.setTextAlignment(txt_align)
        lv.model().appendRow([item, ])

    @staticmethod
    def list_len(lv: QListView) -> int:
        """ Возвращает количество элементов """
        return lv.model().rowCount()

    @staticmethod
    def list_clear(lv: QListView):
        """ Очищает список """
        lv.model().clear()

    @staticmethod
    def list_remove(lv: QListView, s: str) -> bool:
        """ Удаляет первый элемент в списке, имеющий значение s"""
        model: QtGui.QStandardItemModel = lv.model()
        try:
            num = [model.item(i).text() for i in range(model.rowCount())].index(s)
        except ValueError:
            return False
        model.removeRow(num)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

#         LVM.list_append(self.lv_rooms, f'Новая строка {LVM.list_len(self.lv_rooms) + 1}')
#         LVM.list_append(self.lv_users, 'New Line1', color='red')
#         LVM.list_append(self.lv_chat, 'Привет! ', color='blue')
#         LVM.list_append(self.lv_chat, 'Я снова здесь.', color='green', align='right')
