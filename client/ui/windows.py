import time
from PyQt5 import QtCore, QtWidgets

from client.ui.login_ui import Ui_Login_Dialog as login_ui_class
from client.ui.contacts_ui import Ui_ContactsWindow as contacts_ui_class
from client.ui.chat_ui import Ui_ChatMainWindow as chat_ui_class


class LoginWindow(QtWidgets.QDialog):
    """Login Window (user interface)"""

    def __init__(self, parent=None):
        """
        :param auth_instance: instance of client.client_proto.ClientAuth
        :param parent: default None
        """
        super().__init__(parent)
        #self.username = None
        #self.password = None
        #self.auth_instance = auth_instance

        self.ui = login_ui_class()
        self.ui.setupUi(self)


class ContactsWindow(QtWidgets.QMainWindow):
    """Contacts Window (user interface)"""

    def __init__(self, parent=None):
        """

        :param client_instance: instance of client.client_proto.ChatClientProtocol
        :param user_name: client's username
        :param chat_ins: instance of ChatWindow
        :param parent:
        """
        super().__init__(parent)

        self.ui = contacts_ui_class()
        self.ui.setupUi(self)


class ChatWindow(QtWidgets.QMainWindow):
    """Chat Window (user interface)"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = chat_ui_class()
        self.ui.setupUi(self)
        self.parent_window = parent   # bind parent's window attributes
        self.after_start()

    def after_start(self):
        """do appropriate things after starting this window"""
        self.contact_username = self.parent_window.ui.all_contacts.currentItem().text()
        self.username = self.parent_window.username
        self.client_instance = self.parent_window.client_instance
        self.parent_window.chat_ins = self.update_chat
        self.update_chat()

    def keyPressEvent(self, event):
        """Events after pressing key buttons"""
        if event.key() == QtCore.Qt.Key_Enter:
            # here accept the event and do something
            self.on_send_btn_pressed()
            event.accept()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            event.ignore()

    def update_chat(self, quantity=20):
        """Receive client's messages from Database
        :param quantity: how many messages we want to show
        """

        #print('update chat for {}'.format(self.username))
        self.ui.chat_window.clear()
        client_msgs = [c for c in self.client_instance.get_client_messages(self.username)
                       if c.contact.username == self.contact_username]
        contact_msgs = [c for c in self.client_instance.get_client_messages(self.contact_username)
                        if c.contact.username == self.username]
        msgs = sorted(client_msgs + contact_msgs, key=lambda x: x.time)  # all messages between client and contact

        for msg in msgs[-quantity:]:  # show last 20 messages
            sender = msg.client.username
            if msg.client.username == self.username:
                sender = 'me'

            self.ui.chat_window.addItem('{} from {}: {}'.format(msg.time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                sender, msg.message))

    def on_send_btn_pressed(self):
        """After send button clicked, send message to the server and update chat window"""

        msg = self.ui.send_text.text()

        if msg:
            self.client_instance.send_msg(to_user=self.contact_username, content=msg)
            time.sleep(0.1)
            self.update_chat()
            self.ui.send_text.clear()



