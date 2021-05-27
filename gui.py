from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Chat System (ADis) Client")

        g_layout = QVBoxLayout()

        # connections label layout
        msg_label_layout = QHBoxLayout()
        msg_label_layout.setContentsMargins(QMargins())

        self.con_status = QLabel('Connection Status: Connecting...', self)
        self.con_status.setAlignment(Qt.AlignRight)
        self.user_lbl = QLabel(None, self)
        self.user_lbl.setAlignment(Qt.AlignRight)
        boldFont = QFont()
        boldFont.setBold(True)
        self.user_lbl.setFont(boldFont)

        msg_label_layout.addWidget(self.con_status, 1)
        msg_label_layout.addWidget(self.user_lbl)

        msg_label_widget = QWidget(self)
        msg_label_widget.setLayout(msg_label_layout)
        g_layout.addWidget(msg_label_widget)
        # end: connections label layout

        # message layout
        msg_input_layout = QHBoxLayout()
        msg_input_layout.setContentsMargins(QMargins())

        self.msg_input = QLineEdit(self)
        self.msg_input.setMinimumSize(200, 22)
        self.msg_input.setDisabled(True)
        self.msg_input.setPlaceholderText('write a message...')
        self.clients_cb = QComboBox(self)
        self.clients_cb.setMinimumWidth(75)
        self.clients_cb.addItem('<none>')
        self.clients_cb.setMinimumHeight(22)
        self.send_btn = QPushButton('&Send', self)
        self.send_btn.setDisabled(True)
        self.send_btn.setFixedSize(80, 24)

        msg_input_layout.addWidget(self.msg_input)
        msg_input_layout.addWidget(self.clients_cb)
        msg_input_layout.addWidget(self.send_btn)

        msg_widget = QWidget(self)
        msg_widget.setLayout(msg_input_layout)
        g_layout.addWidget(msg_widget)
        # end: message layout

        # local event layout
        local_event_layout = QHBoxLayout()
        local_event_layout.setContentsMargins(QMargins())
        local_event_lbl = QLabel("Create a local event:", self)
        self.local_event_btn = QPushButton('Create &Event', self)
        self.local_event_btn.setFixedSize(80, 24)
        self.local_event_btn.setFixedWidth(80)
        local_event_spacer = QLabel("", self)
        local_event_spacer.setMinimumWidth(160)
        local_event_layout.addWidget(local_event_lbl, 1)
        local_event_layout.addWidget(self.local_event_btn)
        local_event_layout.addWidget(local_event_spacer)

        local_event_widget = QWidget(self)
        local_event_widget.setLayout(local_event_layout)
        g_layout.addWidget(local_event_widget)
        # end: local event layout

        # info layout
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(QMargins())

        # ########## conversation layout
        conversation_layout = QVBoxLayout()
        conversation_layout.setContentsMargins(QMargins())

        # #################### conversation header layout
        conversation_header_layout = QHBoxLayout()
        conversation_header_layout.setContentsMargins(QMargins())
        msg_label = QLabel("Messages:", self)
        msg_label.setMinimumHeight(24)
        conversation_header_layout.addWidget(msg_label, 1)
        clear_btn = QPushButton('&Clear Conversation', self)
        clear_btn.setFixedWidth(120)
        clear_btn.clicked.connect(lambda _: self.conversation_history.clear())
        conversation_header_layout.addWidget(clear_btn)
        conversation_header_widget = QWidget(self)
        conversation_header_widget.setLayout(conversation_header_layout)
        conversation_layout.addWidget(conversation_header_widget)
        # #################### end: conversation header layout

        self.conversation_history = QPlainTextEdit()
        self.conversation_history.setReadOnly(True)
        conversation_layout.addWidget(self.conversation_history)
        conversation_widget = QWidget(self)
        conversation_widget.setLayout(conversation_layout)
        info_layout.addWidget(conversation_widget, 1)
        # ########## end: conversation layout

        # ########## vector layout
        vector_layout = QVBoxLayout()
        vector_layout.setContentsMargins(QMargins())
        vector_label = QLabel("Values Vector:", self)
        vector_label.setMinimumHeight(24)
        self.values_vector = QTableWidget()
        self.values_vector.setMaximumWidth(160)
        self.values_vector.setColumnCount(2)
        header = self.values_vector.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.values_vector.setHorizontalHeaderLabels(
            ['Process n°', 'Num Value']
        )
        self.values_vector.resizeRowsToContents()
        vector_layout.addWidget(vector_label)
        vector_layout.addWidget(self.values_vector)
        vector_widget = QWidget(self)
        vector_widget.setLayout(vector_layout)
        info_layout.addWidget(vector_widget)

        # self.values_vector.setRowCount(1)
        # self.values_vector.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
        # self.values_vector.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
        # self.values_vector.setRowCount(2)
        # self.values_vector.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
        # self.values_vector.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))

        # ########## end: vector layout

        info_widget = QWidget(self)
        info_widget.setLayout(info_layout)
        g_layout.addWidget(info_widget)
        # end: info layout

        g_widget = QWidget(self)
        g_widget.setLayout(g_layout)

        self.setCentralWidget(g_widget)

    def setNoConnection(self):
        self.con_status.setText('Failed! Name Server Not Initialized')

    def setConnected(self, cl_id: str):
        self.con_status.setText(f'Connected as')
        self.user_lbl.setText(f'Process {cl_id}')
        self.msg_input.setDisabled(False)
        self.send_btn.setDisabled(False)
        self.msg_input.setFocus()


class ControlWindow(QMainWindow):
    def __init__(self, flags):
        super(ControlWindow, self).__init__(flags=flags)

        self.setWindowTitle("Chat System (ADis) Control")

        g_layout = QVBoxLayout()

        # nameserver layout
        nameserver_layout = QHBoxLayout()
        nameserver_layout.setContentsMargins(QMargins())

        nameserver_lbl = QLabel("Start nameserver:", self)
        self.start_nameserver = QPushButton('&Start', self)

        nameserver_layout.addWidget(nameserver_lbl, 1)
        nameserver_layout.addWidget(self.start_nameserver)

        nameserver_widget = QWidget(self)
        nameserver_widget.setLayout(nameserver_layout)
        g_layout.addWidget(nameserver_widget)
        # end: nameserver layout

        # client layout
        client_layout = QHBoxLayout()
        client_layout.setContentsMargins(QMargins())

        client_lbl = QLabel("Create client(s):", self)
        self.clients_num = QLineEdit()
        self.clients_num.setValidator(QIntValidator())
        self.clients_num.setText('1')
        self.clients_num.setAlignment(Qt.AlignRight)
        self.clients_num.setMaximumWidth(30)
        self.create_client = QPushButton('&Create', self)
        self.create_client.setDisabled(True)

        client_layout.addWidget(client_lbl, 1)
        client_layout.addWidget(self.clients_num)
        client_layout.addWidget(self.create_client)

        client_widget = QWidget(self)
        client_widget.setLayout(client_layout)
        g_layout.addWidget(client_widget)
        # end: client layout

        g_widget = QWidget(self)
        g_widget.setLayout(g_layout)

        self.setCentralWidget(g_widget)


def client_gui() -> MainWindow:
    window = MainWindow()
    window.resize(550, 400)
    window.move(80, 100)
    window.show()
    return window


def control_gui() -> ControlWindow:
    window = ControlWindow(Qt.WindowStaysOnTopHint)
    window.setFixedSize(320, 80)
    window.move(80, 100)
    window.show()
    return window
