from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
import sys
from main import main

import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Гондурас')
        self.setGeometry(730, 100, 600, 600)

        self.main_button = QtWidgets.QPushButton(self)
        self.main_button.setIcon(QIcon(r'C:\Users\gnido\Documents\off_button.png'))
        #self.main_button.setText('Gondon')
        self.main_button.clicked.connect(self.run_main)
        self.main_button.setFixedSize(60, 60)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.main_button)

        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addStretch()
        central_layout.addLayout(button_layout)
        central_layout.addStretch()
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)


    def run_main(self):
        main()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

