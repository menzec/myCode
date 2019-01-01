import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class filedialogdemo(QWidget):
    def __init__(self, parent=None):
        super(filedialogdemo, self).__init__(parent)
        layout = QVBoxLayout()

        self.btn = QPushButton()
        self.btn.clicked.connect(self.loadFile)
        self.btn.setText("从文件中获取照片")
        layout.addWidget(self.btn)

        self.label = QLabel()
        layout.addWidget(self.label)

        # self.btn_2 = QPushButton()
        # self.btn_2.clicked.connect(self.load_text)
        # self.btn_2.setText("加载电脑文本文件")
        # layout.addWidget(self.btn_2)

        self.content = QTextEdit()
        layout.addWidget(self.content)
        self.setWindowTitle("测试")

        self.setLayout(layout)


    def loadFile(self):
        print("load--file")
        # QFileDialog就是系统对话框的那个类第一个参数是上下文，第二个参数是弹框的名字，
        # 第三个参数是开始打开的路径，第四个参数是需要的格式
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', os.getcwd(),
                                            'Image files(*.jpg *.gif *.png)')
        self.label.setPixmap(QPixmap(fname))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileload = filedialogdemo()
    fileload.show()
    sys.exit(app.exec_())