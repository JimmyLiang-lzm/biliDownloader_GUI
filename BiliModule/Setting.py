import webbrowser
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PySide2.QtCore import Qt, QPoint, Signal
from UI.bilidsetting import Ui_Form
from BiliWorker.extra import checkProxy

############################################################################################
# 高级设置窗口类
class SettingWindow(QWidget, Ui_Form):
    _signal = Signal(dict)
    def __init__(self, ins_dict, parent=None):
        super(SettingWindow,self).__init__(parent)
        self.setupUi(self)
        self.Move = False
        self.ins_dict = ins_dict
        self.edit_cookies.setPlainText(ins_dict["cookie"])
        self.cb_useProxy.setChecked(ins_dict["useProxy"])
        self.lineEdit.setText(ins_dict["Proxy"]["http"])
        # 设置窗口透明
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置鼠标动作位置
        self.m_Position = QPoint(0,0)
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)
        # 连接器
        self.btnmin.clicked.connect(lambda: self.showMinimized())
        self.btn_cancel.clicked.connect(lambda: self.close())
        self.btn_editconfig.clicked.connect(self.setConfig)
        self.btn_cleanplain.clicked.connect(self.clearTEXT)
        self.btn_wherecookie.clicked.connect(self.forHelp)
        self.btn_testProxy.clicked.connect(self.testProxy)
        self.btn_huseProxy.clicked.connect(self.ProxyHelp)
    ####################### RW Part ##########################
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

    # 定义关闭事件
    def closeEvent(self, QCloseEvent):
        self._signal.emit({"code":0})

    ####################### BS Part ##########################
    # 测试代理函数
    def testProxy(self):
        proxy_url = self.lineEdit.text()
        proxy_temp = {'http': proxy_url,'https':proxy_url,}
        self.ts = checkProxy(proxy_temp)
        self.lineEdit.setEnabled(False)
        self.btn_testProxy.setEnabled(False)
        self.btn_testProxy.setText("正在检测")
        self.ts._feedback.connect(self.proxy_catch)
        self.ts.start()

    # 确定设置函数
    def setConfig(self):
        self.ins_dict["cookie"] = self.edit_cookies.toPlainText()
        if self.cb_useProxy.isChecked():
            self.ins_dict["useProxy"] = True
        else:
            self.ins_dict["useProxy"] = False
        proxy_url = self.lineEdit.text()
        self.ins_dict["Proxy"] = {'http': proxy_url,'https':proxy_url,}
        self._signal.emit({"code":1,"indict":self.ins_dict})
        self.close()

    # 清空编辑框
    def clearTEXT(self):
        self.edit_cookies.clear()

    # 帮助按钮
    def forHelp(self):
        webbrowser.open("https://jimmyliang-lzm.github.io/2021/10/06/Get_bilibili_cookie/")

    # 代理帮助按钮
    def ProxyHelp(self):
        webbrowser.open("https://jimmyliang-lzm.github.io/2021/10/07/bilid_GUI_help/#3-5-“僅限港澳台地區”视频下载")

    ########################### 槽函数 ################################
    # 代理地址测试线程槽函数
    def proxy_catch(self, in_dict):
        if in_dict["code"] == 1:
            text_temp = "测试状态：成功 地区：" + in_dict["area"] + " IP:" + in_dict["ip"]
            self.lineEdit_test.setText(text_temp)
            self.lineEdit.setEnabled(True)
            self.btn_testProxy.setText("测试地址")
            self.btn_testProxy.setEnabled(True)
        else:
            self.lineEdit_test.setText("测试状态：连接失败")
            self.lineEdit.setEnabled(True)
            self.btn_testProxy.setText("测试地址")
            self.btn_testProxy.setEnabled(True)
