from etc import *
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
from BiliModule.Main import MainWindow


######################################################################
# 程序入口
if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
