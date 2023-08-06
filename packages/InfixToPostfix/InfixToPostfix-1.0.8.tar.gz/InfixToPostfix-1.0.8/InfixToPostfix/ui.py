import os

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QTableWidget

from InfixToPostfix.infix_to_postfix import InfixToPostfix


class MainWindow(QWidget):
    STYLE_QSS_PATH = os.path.join(os.path.dirname(__file__), "data/style.qss")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("后缀表达式生成器")
        self.setStyleSheet(open(MainWindow.STYLE_QSS_PATH).read())
        self.resize(1280, 720)
        self.conf = ""
        self.file_chooser = QPushButton("选取配置文件")
        self.file_chooser.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.expression = QLineEdit()
        self.expression.setPlaceholderText("输入表达式")
        self.expression.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.expression.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.data_process = QPushButton("提交")
        self.data_process.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.child_window = QWidget()
        self.child_window.setStyleSheet(open(MainWindow.STYLE_QSS_PATH).read())
        self.child_window.setWindowTitle("分析结果")
        self.child_window.resize(1280, 720)
        self.init_layout()
        self.show()

    def init_layout(self):
        def file_chooser_connect():
            self.conf = QFileDialog().getOpenFileName(self, "选取配置文件", "./", "All Files (*)")[0]
            self.file_chooser.setText(self.conf)

        def data_process_connect():
            data = InfixToPostfix() if self.conf == "" else InfixToPostfix(self.conf)
            words, actions, states, result = data.analyze(self.expression.text())

            child_layout = QGridLayout()

            analyze_result = QTableWidget(len(actions), 2)
            analyze_result.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            analyze_result.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            analyze_result.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
            for i, action, state in zip(range(len(actions)), actions, states):
                item_0 = QtWidgets.QTableWidgetItem(action)
                item_1 = QtWidgets.QTableWidgetItem(state)
                item_0.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_1.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                analyze_result.setItem(i, 0, item_0)
                analyze_result.setItem(i, 1, item_1)
            analyze_result.setColumnWidth(0, 605)
            analyze_result.setColumnWidth(1, 605)

            raw = QLabel(f"中缀表达式   {' '.join([word[1] for word in words])}")
            raw.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            result = QLabel(f"后缀表达式   {' '.join(result)}")
            result.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            child_layout.addWidget(analyze_result, 0, 0, 3, 2)
            child_layout.addWidget(raw, 3, 0, 1, 1)
            child_layout.addWidget(result, 3, 1, 1, 1)

            self.child_window.setLayout(child_layout)
            self.child_window.show()

        grid = QGridLayout()

        self.file_chooser.clicked.connect(file_chooser_connect)
        self.data_process.clicked.connect(data_process_connect)

        grid.addWidget(self.file_chooser, 0, 0, 2, 1)
        grid.addWidget(self.expression, 0, 1, 1, 1)
        grid.addWidget(self.data_process, 1, 1, 1, 1)

        self.setLayout(grid)
