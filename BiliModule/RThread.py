from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect, QMessageBox
from PySide2.QtCore import Signal, Qt, QPoint
from UI.biliRecurInfo import Ui_Form
from BiliWorker.extra import biliWorker_interact


##############################################################################
# 递归探查线程反馈主界面
class RecurThreadWindow(QWidget, Ui_Form):
    _RSignal = Signal(dict)
    def __init__(self, mode: int, module: biliWorker_interact, st_node: str, deep: int = -1, parent=None):
        super(RecurThreadWindow, self).__init__(parent)
        self.setupUi(self)
        self.Move = False
        # 初始化信息
        self.mode = mode
        self.rtmodule = module
        self.start_node = st_node
        self.search_deep = deep
        self.feedback = {}
        # 设置父窗口阻塞与窗口透明
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
        self.pushButton.clicked.connect(self.stop_thread)
        # 开始运行
        self.run_thread()

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
        self._RSignal.emit(self.feedback)


    ####################### BS Part ##########################
    # 开始运行线程
    def run_thread(self):
        self.rtmodule.change_method(2, cur_node_id=self.start_node, deep=self.search_deep)
        self.rtmodule.business_info.connect(self.RTSlot_bsinfo)
        self.rtmodule.rthread_status.connect(self.RTSlot_status)
        self.rtmodule.start()


    # 停止递归
    def stop_thread(self):
        self.rtmodule.kill_rthread()

    ####################### 槽函数 ############################
    # 接收递归线程反馈字符
    def RTSlot_bsinfo(self, instr):
        self.plainTextEdit.setPlainText(instr)

    # 接收线程反馈字典
    def RTSlot_status(self, indic):
        if indic['code'] == 0:
            self.label_5.setText(indic['node_id'])
            self.label_6.setText(str(indic['deep']))
            self.label_4.setText(indic['node_name'])
        elif indic['code'] == 1:
            self.feedback['status'] = self.mode
            self.feedback['data'] = indic['node_dict']
            self.close()
        else:
            QMessageBox.information(self, '探查反馈', indic['data'])
            self.close()
