import webbrowser
from etc import *
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PySide2.QtCore import Qt, QPoint
from UI.bilidabout import Ui_Form
from BiliWorker.extra import checkLatest


############################################################################################
# 关于窗口类
class AboutWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)
        self.Move = False
        # 设置窗口透明
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置鼠标动作位置
        self.m_Position = QPoint(0, 0)
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)
        # 连接器
        self.btnmin.clicked.connect(lambda: self.showMinimized())
        self.btn_access.clicked.connect(self.accessWeb)
        self.btn_latest.clicked.connect(self.checkLatest)
        self.btn_bugCall.clicked.connect(self.callBUG)
        # 初始化显示设置
        self.lab_version.setText(Release_INFO[0])
        self.label_6.setText(Release_INFO[1])

    # ###################### RW Part #######################
    # 鼠标点击事件产生
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.Move = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.Move:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    # 鼠标释放事件
    def mouseReleaseEvent(self, QMouseEvent):
        self.Move = False

    # ###################### BS Part #######################
    # 访问作者网站按钮函数
    def accessWeb(self):
        webbrowser.open("https://jimmyliang-lzm.github.io/")

    # 检查版本更新函数
    def checkLatest(self):
        self.cl = checkLatest(Release_INFO[0])
        self.btn_latest.setEnabled(False)
        self.cl._feedback.connect(self.verShow)
        self.cl.start()

    # 打开BUG反馈ISSUE页面
    def callBUG(self):
        webbrowser.open("https://github.com/JimmyLiang-lzm/biliDownloader_GUI/issues")

    # ##### 槽函数 ######
    def verShow(self, inum):
        if inum == -1:
            self.btn_latest.setEnabled(True)
            self.btn_latest.setText("检查更新")
        elif inum == 0:
            self.btn_latest.setText("已最新")
        elif inum == 1:
            self.btn_latest.setEnabled(True)
            self.btn_latest.setText("可更新")
        elif inum == 2:
            self.btn_latest.setText("网络出错")
