from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Chat System (ADis)")

        g_layout = QVBoxLayout()

        # connections label layout
        msg_label_layout = QHBoxLayout()
        msg_label_layout.setContentsMargins(QMargins())

        msg_label = QLabel("Messages:", self)
        self.con_status = QLabel('Connection Status: Connecting...', self)
        self.user_lbl = QLabel(None, self)
        boldFont = QFont()
        boldFont.setBold(True)
        self.user_lbl.setFont(boldFont)

        msg_label_layout.addWidget(msg_label, 1)
        msg_label_layout.addWidget(self.con_status)
        # msg_label_layout.setAlignment(
        #     self.con_status, Qt.AlignmentFlag.AlignRight
        # )
        msg_label_layout.addWidget(self.user_lbl)
        # msg_label_layout.setAlignment(
        #     self.user_lbl, Qt.AlignmentFlag.AlignRight
        # )

        msg_label_widget = QWidget(self)
        msg_label_widget.setLayout(msg_label_layout)
        g_layout.addWidget(msg_label_widget)
        # end: connections label layout

        # conversation layout
        self.conversation_history = QPlainTextEdit()
        self.conversation_history.setReadOnly(True)

        g_layout.addWidget(self.conversation_history)
        # end: conversation layout

        # message layout
        msg_input_layout = QHBoxLayout()
        msg_input_layout.setContentsMargins(QMargins())

        self.msg_input = QLineEdit(self)
        self.msg_input.setDisabled(True)
        self.msg_input.setPlaceholderText('write a message...')

        self.send_btn = QPushButton(
            QIcon('./icons/send.png'), ' &Send', self
        )
        self.send_btn.setDisabled(True)
        self.send_btn.setFixedWidth(80)

        clean_btn = QPushButton(
            QIcon('./icons/clean.png'), ' &Clean Conversation', self
        )
        clean_btn.setFixedWidth(120)
        clean_btn.clicked.connect(lambda _: self.conversation_history.clear())

        msg_input_layout.addWidget(self.msg_input)
        msg_input_layout.addWidget(self.send_btn)
        msg_input_layout.addWidget(clean_btn)

        msg_widget = QWidget(self)
        msg_widget.setLayout(msg_input_layout)
        g_layout.addWidget(msg_widget)
        # end: message layout

        g_widget = QWidget(self)
        g_widget.setLayout(g_layout)

        self.setCentralWidget(g_widget)

    def setNoConnection(self):
        self.con_status.setText('Failed! Name Server Not Initialized')

    def setConnected(self, cl_id: str):
        self.con_status.setText(f'Connected as')
        self.user_lbl.setText(cl_id)
        self.msg_input.setDisabled(False)
        self.send_btn.setDisabled(False)
        self.msg_input.setFocus()


def create_gui() -> MainWindow:
    window = MainWindow()
    window.resize(550, 400)
    window.move(80, 100)
    window.show()
    return window
