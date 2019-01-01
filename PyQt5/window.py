# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_pic.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def __init__(self, Dialog):
        self.setupUi(Dialog)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1102, 862)
        Dialog.setSizeGripEnabled(False)
        self.gridWidget = QtWidgets.QWidget(Dialog)
        self.gridWidget.setGeometry(QtCore.QRect(40, 20, 761, 141))
        self.gridWidget.setObjectName("gridWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ImageFolderBtn = QtWidgets.QPushButton(self.gridWidget)
        self.ImageFolderBtn.setObjectName("ImageFolderBtn")
        self.gridLayout.addWidget(self.ImageFolderBtn, 0, 0, 1, 1)
        self.ImageFoler = QtWidgets.QTextEdit(self.gridWidget)
        self.ImageFoler.setObjectName("ImageFoler")
        self.gridLayout.addWidget(self.ImageFoler, 0, 1, 1, 2)
        self.RightFolderBtn = QtWidgets.QPushButton(self.gridWidget)
        self.RightFolderBtn.setObjectName("RightFolderBtn")
        self.gridLayout.addWidget(self.RightFolderBtn, 1, 0, 1, 1)
        self.RightFoler = QtWidgets.QTextEdit(self.gridWidget)
        self.RightFoler.setObjectName("RightFoler")
        self.gridLayout.addWidget(self.RightFoler, 1, 1, 1, 2)
        self.DeleteFoler = QtWidgets.QTextEdit(self.gridWidget)
        self.DeleteFoler.setMinimumSize(QtCore.QSize(557, 35))
        self.DeleteFoler.setObjectName("DeleteFoler")
        self.gridLayout.addWidget(self.DeleteFoler, 2, 1, 1, 2)
        self.DeleteFolerBtn = QtWidgets.QPushButton(self.gridWidget)
        self.DeleteFolerBtn.setObjectName("DeleteFolerBtn")
        self.gridLayout.addWidget(self.DeleteFolerBtn, 2, 0, 1, 1)
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(825, 31, 271, 771))
        self.listView.setObjectName("listView")
        self.KeepBtn = QtWidgets.QPushButton(Dialog)
        self.KeepBtn.setGeometry(QtCore.QRect(470, 790, 275, 28))
        self.KeepBtn.setObjectName("KeepBtn")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(130, 790, 275, 28))
        self.pushButton.setObjectName("pushButton")
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(150, 240, 512, 512))
        self.graphicsView.setObjectName("graphicsView")
        self.imagename = QtWidgets.QTextEdit(Dialog)
        self.imagename.setGeometry(QtCore.QRect(230, 170, 561, 36))
        self.imagename.setObjectName("imagename")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(50, 170, 171, 36))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.ImageFoler, self.RightFolderBtn)
        Dialog.setTabOrder(self.RightFolderBtn, self.RightFoler)
        Dialog.setTabOrder(self.RightFoler, self.DeleteFolerBtn)
        Dialog.setTabOrder(self.DeleteFolerBtn, self.DeleteFoler)

        Dialog.show()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "SelectPic"))
        self.ImageFolderBtn.setText(_translate("Dialog", "Image Folder"))
        self.RightFolderBtn.setText(_translate("Dialog", "Right Folder"))
        self.DeleteFolerBtn.setText(_translate("Dialog", "Delete Folder"))
        self.KeepBtn.setText(_translate("Dialog", "Keep"))
        self.pushButton.setText(_translate("Dialog", "Delete"))
        self.plainTextEdit.setPlainText(_translate("Dialog", "      Image Name"))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # form = QWidget()
    form = QtWidgets.QDialog()
    widgetee = Ui_Dialog(form)
    form.show()
    sys.exit(app.exec_())