# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import os
import sys
import cv2
import shutil
import platform

from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_MainWindow import Ui_MainWindow


class UI(Ui_MainWindow):
    def __init__(self, MainWindow):
        self.loglist = []
        self.setupUi(MainWindow)
        self.connect_action()

    def connect_action(self):
        self.ImageFolderBtn.clicked.connect(self.imagefolderBtn_func)
        self.RightFolderBtn.clicked.connect(self.RightFolderBtn_func)
        self.DeleteFolerBtn.clicked.connect(self.DeleteFolerBtn_func)
        self.KeepBtn.clicked.connect(self.KeepBtn_func)
        self.DeleteBtn.clicked.connect(self.DeleteBtn_func)
        self.NextBtn.clicked.connect(self.NextBtn_func)

    def filter_file(self, filelist, filters):
        if not len(filelist):
            return None
        i = 0
        imagefile = filelist[i]
        while imagefile:
            if not os.path.splitext(imagefile)[1] in filters:
                filelist.pop(i)
            else:
                i = i + 1
            if i < len(filelist):
                imagefile = filelist[i]
            else:
                imagefile = None

    def getimagefile(self):
        if len(self.imagefilelist):
            return self.imagefilelist.pop(0)
        else:
            return None

    def showimage(self, image):
        img_origin = cv2.imread(os.path.join(self.imagefolder_var,
                                             image))  #读取图像
        img_origin = cv2.cvtColor(img_origin, cv2.COLOR_BGR2RGB)  #转换图像通道
        img = cv2.resize(img_origin, (760, 760), cv2.INTER_LINEAR)
        x = img.shape[1]  #获取图像大小
        y = img.shape[0]
        # self.zoomscale = 1  #图片放缩尺度
        frame = QtGui.QImage(img, x, y, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(frame)
        self.item = QtWidgets.QGraphicsPixmapItem(pix)  #创建像素图元
        #self.item.setScale(self.zoomscale)
        self.scene = QtWidgets.QGraphicsScene()  #创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)  #将场景添加至视图

    def next_image(self):
        self.cur_image = self.getimagefile()
        if self.cur_image:
            self.show_ImageFolder_info()
            self.imageinfoText.setText(self.cur_image)
            self.showimage(self.cur_image)
            if hasattr(self, "RightFolder_var"):
                self.show_RightFolder_info()
            if hasattr(self, "DeleteFoler_var"):
                self.show_DeleteFolder_info()
        else:
            self.imageinfoText.setText("No Images.")

    def show_ImageFolder_info(self):
        self.ImageFolerText.setText(self.imagefolder_var + '\t' +
                                    str(len(os.listdir(self.imagefolder_var))))

    def show_DeleteFolder_info(self):
        parent_dir = os.path.abspath(os.path.join(self.DeleteFoler_var, ".."))
        self.DeleteFolerText.setText(self.DeleteFoler_var + '\t' + str(
            len(os.listdir(self.DeleteFoler_var))) + '\t' +
                                     str(parent_dir == self.imagefolder_var))

    def show_RightFolder_info(self):
        parent_dir = os.path.abspath(os.path.join(self.RightFolder_var, ".."))
        self.RightFolerText.setText(self.RightFolder_var + '\t' + str(
            len(os.listdir(self.RightFolder_var))) + '\t' +
                                    str(parent_dir == self.imagefolder_var))

    def imagefolderBtn_func(self):
        if str(platform.system()) == 'Windows' and os.path.exists(
                r'D:\data\qinghua\img'):
            cur_path = r'D:\data\qinghua\img'
        self.imagefolder_var = os.path.abspath(
            QtWidgets.QFileDialog.getExistingDirectory(
                None, 'Choose image folder', cur_path))
        if not self.imagefolder_var:
            return False
        self.ImageFolerText.setText(self.imagefolder_var)
        self.imagefilelist = os.listdir(self.imagefolder_var)
        self.filter_file(self.imagefilelist, ['.jpg', '.gif', '.png', '.tif'])
        self.next_image()

    def RightFolderBtn_func(self):
        cur_path = ''
        if hasattr(self, 'imagefolder_var'):
            cur_path = self.imagefolder_var
        else:
            cur_path = os.getcwd()
        self.RightFolder_var = os.path.abspath(
            QtWidgets.QFileDialog.getExistingDirectory(
                None, 'Choose save right image folder', cur_path))
        self.show_RightFolder_info()

    def DeleteFolerBtn_func(self):
        cur_path = ''
        if hasattr(self, 'imagefolder_var'):
            cur_path = self.imagefolder_var
        else:
            cur_path = os.getcwd()
        self.DeleteFoler_var = os.path.abspath(
            QtWidgets.QFileDialog.getExistingDirectory(
                None, 'Choose save not qualified image folder', cur_path))
        self.show_DeleteFolder_info()

    def KeepBtn_func(self):
        if not self.cur_image:
            return None
        shutil.move(
            os.path.join(self.imagefolder_var, self.cur_image),
            self.RightFolder_var)
        self.loglist.append(
            [self.cur_image, self.imagefolder_var, self.RightFolder_var])
        if len(self.loglist) > 50:
            self.write_log()
        self.next_image()

    def DeleteBtn_func(self):
        if not self.cur_image:
            return None
        shutil.move(
            os.path.join(self.imagefolder_var, self.cur_image),
            self.DeleteFoler_var)
        self.loglist.append(
            [self.cur_image, self.imagefolder_var, self.DeleteFoler_var])
        if len(self.loglist) > 50:
            self.write_log()
        self.next_image()

    def NextBtn_func(self):
        self.next_image()

    def write_log(self):
        logfile = open(os.path.join(self.imagefolder_var, 'move-log.txt'), 'a')
        while len(self.loglist):
            write_info = self.loglist.pop(0)
            for info in write_info:
                logfile.write(info + ',')
        logfile.close()

    def closeEvent(self, event):
        self.write_log()
        # reply = QtWidgets.QMessageBox.question(
        #     self, '本程序', "是否要退出程序？",
        #     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        #     QtWidgets.QMessageBox.No)
        # if reply == QtWidgets.QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QMainWindow()
    try:
        widgetee = UI(form)
        form.show()
    except:
        form.write_log()
    sys.exit(app.exec_())
