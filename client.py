#!/bin/python3

from gui import client_gui
from chat_server import ChatServer
from server_listener import ServerListener
from PyQt5.QtWidgets import *

import sys


# print(sys.argv)
def create_client(**kwargs: dict):
    app = QApplication(sys.argv)
    window = client_gui()
    proc_num = kwargs['proc_num'] or None
    print(proc_num)
    server = ChatServer(window, app)
    server_listener = ServerListener(window, app, server)
    server_listener.start()
    app.exec_()


if __name__ == '__main__':
    create_client()
