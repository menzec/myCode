import os
import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class SelectPic(QWidget):
    def __init__(self, parent=None):
        super(SelectPic, self).__init__(parent)
        layout = QVBoxLayout()

        self.btn = QPushButton()
        self.btn.clicked.connect(self.loadpic)
        self.btn.setText("open picture")
        layout.addWidget(self.btn)
        self.label = QLabel()
        layout.addWidget(self.label)

        self.content = QTextEdit()
        layout.addWidget(self.content)
        self.setWindowTitle("筛选图片")

        self.setLayout(layout)

    def loadpic(self):
        fname, _ = QFileDialog.getExistingDirectory(
            self, '选择图片', os.getcwd(), 'Image files(*.jpg *.gif *.png)')
        self.label.setPixmap(QPixmap(fname))

    # 在


if __name__ == "__main__":

    def main():
        app = QApplication(sys.argv)
        fileload = SelectPic()
        fileload.show()
        sys.exit(app.exec_())

    main()
