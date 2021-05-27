#!/bin/python3

from gui import client_gui
from chat_server import ChatServer
from server_listener import ServerListener
from PyQt5.QtWidgets import *
from random import choices
from string import digits


import sys


# print(sys.argv)
def create_client(**kwargs: dict):
    app = QApplication(sys.argv)
    window = client_gui()
    proc_num: int = kwargs['proc_num'] if 'proc_num' in kwargs else int(
        ''.join(choices(digits, k=5))
    )
    server = ChatServer(window, app, proc_num)
    server_listener = ServerListener(window, app, server)
    server_listener.start()
    app.exec_()


if __name__ == '__main__':
    create_client()
