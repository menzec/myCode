'''
hello_world

    QWidget:
        resize()
        move()
        setGeometry(poistion,size)
        setWindowTitle(string)
        setWindowIcon(QIcon(string filename)) -图标
        QToolTip.setFont(QFont(string fontname,int size))
        QPushButton(string button_name,QWidget parent=self)
        button.setToolTip(string tip)
        button.resize()
        button.move()
        qbtn.clicked.connect(QCoreApplication.instance().quit)--事件传递系统
    QMessageBox

        
状态栏--self.statusBar().showMessage('Ready')
exitAct = QAction(QIcon('exit.png'), '&Exit', self)
exitAct.setShortcut('Ctrl+Q')
exitAct.setStatusTip('Exit application')
QAction 是菜单栏、工具栏或者快捷键的动作的组合。前面两行，我们创建了一个图标、一个exit的标签和一个快捷键组合，
都执行了一个动作。第三行，创建了一个状态栏，当鼠标悬停在菜单栏的时候，能显示当前状态。
menubar = QMainWindow.menuBar()
fileMenu = menubar.addMenu('&File')
fileMenu.addAction(exitAct)
menuBar()创建菜单栏。这里创建了一个菜单栏，并在上面添加了一个file菜单，并关联了点击退出应用的事件。
impMenu = QMenu('Import', self)
'''
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        self.setGeometry(300, 300, 250, 150)        
        self.setWindowTitle('Message box')    
        self.show()
        
        
    def closeEvent(self, event):
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())