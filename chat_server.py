from datetime import datetime
from typing import List, Union, Any
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Pyro4 import Proxy
from gui import MainWindow
from random import choices
from string import ascii_letters, digits
from threading import Thread

import Pyro4
import sys


class ChatServer(QObject):
    new_message_sig = pyqtSignal('QString', 'QString', 'QString')

    def __init__(self, window: MainWindow, app: QApplication):
        super().__init__(parent=app)
        self.window = window
        self.g_ns: Proxy = None
        self.client_id = 'user-' + ''.join(
            choices(ascii_letters + digits, k=5)
        )
        self.clients: List[Union[Proxy, ChatServer]] = []

        self.window.msg_input.returnPressed.connect(
            lambda: self.broadcast_message(self.window.msg_input)
        )
        self.window.send_btn.clicked.connect(
            lambda _: self.broadcast_message(self.window.msg_input)
        )
        self.window.closeEvent = self.window_close

        self.daemon = Pyro4.Daemon()
        self.uri = self.daemon.register(self)

        self.new_message_sig.connect(
            self.__update_conversation__
        )

    def window_close(self, event):
        event.accept()

        if (self.g_ns and hasattr(self.g_ns, 'remove')):
            self.g_ns.remove(
                'hahouari.client.' + self.client_id,
                str(self.uri)
            )
        self.daemon.unregister(self)
        self.daemon.shutdown()

    def broadcast_message(self, msg_input: QLineEdit):
        if (self.g_ns is None or len(msg_input.text()) == 0):
            return

        text = msg_input.text()
        now = datetime.now()

        data = {
            'id': self.client_id,
            'text': text,
            'time': f"{now:%H:%M:%S}"
        }

        self.__broadcast__(data)
        self.__update_conversation__(data['id'], data['text'], data['time'])

        msg_input.clear()

    def __broadcast__(self, data: dict):
        if (self.g_ns is None):
            return

        for client in self.clients:
            try:
                Thread(target=client.update_conversation, args=(data,)).start()
            except Exception:
                self.clients.remove(client)
                pass

    def __update_conversation__(self, cl_id: str, text: str, time: str):
        label = f'<b>[You]</b>' if cl_id == self.client_id else f'{cl_id}'
        self.window.conversation_history.appendHtml(
            f'{label} -> {text} - received at {time}'
        )

    @Pyro4.expose
    def update_conversation(self, data: dict):
        cl_id = data['id']
        text = data['text']
        time = data['time']
        self.new_message_sig.emit(cl_id, text, time)

    @Pyro4.expose
    def update_clients_list(self, data: dict) -> bool:
        try:
            client_uri: str = data['uri']
            self.clients.append(Pyro4.Proxy(client_uri))
            return True
        except Exception:
            return False
