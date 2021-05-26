from PyQt5.QtWidgets import *
from gui import ControlWindow
from client import create_client
from multiprocessing import Process
from typing import List

import Pyro4.core
import Pyro4.naming
import Pyro4.socketutil
import Pyro4
import os


def create_ns():
    os.system('python -m Pyro4.naming')


class ControlUtils:

    def __init__(self, controlWindow: ControlWindow):
        super().__init__()
        self.ns_proc: Process = None
        self.clients: List[Process] = []
        self.counter = 0
        self.controlWindow = controlWindow
        self.controlWindow.start_nameserver.clicked.connect(
            lambda _: self.on_name_server_start()
        )
        self.controlWindow.create_client.clicked.connect(
            lambda _: self.on_client_create()
        )
        self.controlWindow.closeEvent = self.window_close

    def on_client_create(self):
        print('onClientCreate')
        num = int(self.controlWindow.clients_num.text()) or 0
        self.controlWindow.clients_num.setText('1')
        for i in range(num):
            self.counter += 1
            print(f'Proc[{self.counter}]')
            p = Process(
                target=create_client,
                kwargs={
                    'proc_num': self.counter
                }
            )
            self.clients.append(p)
            p.start()

    def on_name_server_start(self):
        if self.ns_proc is not None and self.ns_proc.is_alive:
            self.ns_proc.kill()
            self.ns_proc = None
            self.controlWindow.create_client.setDisabled(True)
            self.controlWindow.start_nameserver.setText('&Start')
            for client in self.clients:
                if client.is_alive:
                    client.kill()
            self.counter = 0
        else:
            self.ns_proc = Process(target=create_ns)
            self.ns_proc.start()

            self.controlWindow.start_nameserver.setText('C&lose')
            self.controlWindow.create_client.setDisabled(False)

    def window_close(self, event):
        event.accept()
        if self.ns_proc is not None and self.ns_proc.is_alive:
            self.ns_proc.kill()
            for client in self.clients:
                if client.is_alive:
                    client.kill()