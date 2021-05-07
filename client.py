#!/bin/python3

from gui import create_gui
from chat_server import ChatServer
from server_listener import ServerListener
from PyQt5.QtWidgets import *

import sys


app = QApplication(sys.argv)
window = create_gui()
server = ChatServer(window, app)
server_listener = ServerListener(window, app, server)
server_listener.start()
app.exec_()
