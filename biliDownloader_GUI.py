import sys, os, webbrowser, socket
import requests.packages.urllib3.util.connection as urllib3_conn
import json, re, subprocess
# from time import time,sleep
from time import sleep
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QCheckBox, QListWidgetItem, QFileDialog, QWidget, QTreeWidgetItem
from PySide2.QtCore import Qt, QThread, Signal, QPoint, QTimer
from PySide2.QtGui import QIntValidator
from pyecharts import options as opts
from pyecharts.charts import Tree
from UI import biliDownloader, bilidsetting, bilidabout, biliInteractive
# 共享VIP Cookie预留（不使用请注释）
# import requests
# import req_encrypt as request

# 不使用共享VIP Cookie（不使用请取消注释）
import requests as request

# Release Information
Release_INFO = ["V1.5.20220311","2022/03/11"]

# 强制使用IPv4
urllib3_conn.allowed_gai_family = lambda: socket.AF_INET

# Initialize
Objective = biliDownloader.Ui_MainWindow
Objective_setting = bilidsetting.Ui_Form
Objective_about = bilidabout.Ui_Form
Objective_interact = biliInteractive.Ui_Form
DF_Path = os.path.dirname(os.path.realpath(sys.argv[0]))
indict = {
    "Address":"",
    "DownList":[],
    "VideoQuality":0,
    "AudioQuality":0,
    "Output":"",
    "Synthesis":1,
    "sys":"",
    "cookie":"",
    "sym":True,
    "useCookie":False,
    "useProxy":False,
    "Proxy": {'http': '','https':'',}
}

# Mainwindow Class
class MainWindow(QMainWindow,Objective):
    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.threadBusy = False
        self.Move = False
        self.haveINFO = False
        self.allSelect = False
        self.setWindowOPEN = False
        self.isInteractive = False
        self.isAudio = False
        self.bu_info_count = 0
        self.in_dict = {"finish":1}
        # 设置窗口透明
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
        self.btnmin.clicked.connect(lambda:self.showMinimized())
        self.btn_search.clicked.connect(self.Get_preInfo)
        self.btn_dir.clicked.connect(self.selectDir)
        self.checkBox_usecookie.clicked.connect(self.useCookie)
        self.checkBox_sym.clicked.connect(self.useSym)
        self.btn_selectALL.clicked.connect(self.selectALL)
        self.btn_download.clicked.connect(self.download)
        self.btn_pause.clicked.connect(self.pause_download)
        self.btn_stop.clicked.connect(self.stop_download)
        self.btn_changeconfig.clicked.connect(self.set_config)
        self.btn_help.clicked.connect(self.forHELP)
        self.btn_about.clicked.connect(self.openAbout)
        # 默认目录
        try:
            with open(DF_Path + '/setting.conf', 'r', encoding='utf-8') as f:
                tempr = json.loads(f.read())
                indict["sys"] = tempr["sys"]
                indict["cookie"] = tempr["cookie"]
                indict["Output"] = tempr["output"]
                indict["useProxy"] = tempr["useProxy"]
                indict["Proxy"] = tempr["Proxy"]
                if tempr["UseCookie"]:
                    indict["useCookie"] = True
                    self.checkBox_usecookie.setChecked(True)
                else:
                    indict["useCookie"] = False
                    self.checkBox_usecookie.setChecked(False)
                if tempr["synthesis"]:
                    self.checkBox_sym.setChecked(True)
                    indict["sym"] = True
                else:
                    self.checkBox_sym.setChecked(False)
                    indict["sym"] = False
        except:
            indict["Output"] = DF_Path
            indict["sys"] = sys.platform
            self.checkBox_sym.setChecked(True)
        # 部分显示初始化
        self.lineEdit_dir.setText(indict["Output"])
        self.plainTextEdit.setPlainText("欢迎使用Bili Downloader {}\nRelease at {} ......"
                                        .format(Release_INFO[0],Release_INFO[1]))
        # 计时器初始化
        self.progressBarTimer = QTimer()
        self.progressBarTimer.start(100)
        self.progressBarTimer.timeout.connect(self.progress_Show)

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

    # 退出事件记录
    def closeEvent(self,QCloseEvent):
        with open(DF_Path + '/setting.conf', 'w', encoding='utf-8') as f:
            temp_dict = {
                "UseCookie":indict["useCookie"],
                "synthesis":indict["sym"],
                "cookie":indict["cookie"],
                "sys":indict["sys"],
                "output":indict["Output"],
                "useProxy":indict["useProxy"],
                "Proxy":indict["Proxy"]
            }
            f.write(json.dumps(temp_dict,sort_keys=True,indent=4))
            f.close()

    ####################### BS Part ##########################
    # 资源探查事件函数
    def Get_preInfo(self):
        #print(indict)
        indict["Address"] = self.source_search.text()
        # 无信息状态恢复
        self.haveINFO = False
        self.isAudio = False
        self.combo_vq.clear()
        self.combo_aq.clear()
        self.media_list.clear()
        # 启动线程
        self.tes = biliWorker(indict,0)
        self.tes.business_info.connect(self.businINFO_Catch)
        self.tes.vq_list.connect(self.vqulityList)
        self.tes.aq_list.connect(self.aqulityList)
        self.tes.media_list.connect(self.mediaList)
        self.tes.is_finished.connect(self.thread_finished)
        self.tes.interact_info.connect(self.interact_Catch)
        self.btn_search.setEnabled(False)
        self.groupBox.setEnabled(False)
        self.threadBusy = True
        self.tes.start()

    # 选择目录事件函数
    def selectDir(self):
        directory = QFileDialog.getExistingDirectory(None,"选择文件夹",indict["Output"])
        if directory != "":
            self.lineEdit_dir.setText(directory)
            indict["Output"] = directory
        QApplication.processEvents()

    # 使用VIP Cookie事件函数
    def useCookie(self):
        if self.checkBox_usecookie.isChecked():
            indict["useCookie"] = True
        else:
            indict["useCookie"] = False

    # 使用合成处理事件
    def useSym(self):
        if self.checkBox_sym.isChecked():
            indict["sym"] = True
        else:
            indict["sym"] = False

    # 选择全部视频列表处理函数
    def selectALL(self):
        if self.allSelect:
            count = self.media_list.count()
            if count == 0:
                return 0
            self.allSelect = False
            self.btn_selectALL.setText("全选")
            for i in range(count):
                self.media_list.itemWidget(self.media_list.item(i)).setChecked(False)
        else:
            count = self.media_list.count()
            if count == 0:
                return 0
            self.allSelect = True
            self.btn_selectALL.setText("全不选")
            for i in range(count):
                self.media_list.itemWidget(self.media_list.item(i)).setChecked(True)

    # 下载视频按钮事件处理函数
    def download(self):
        if self.haveINFO:
            if self.isInteractive:
                indict["DownList"] = []
                indict["VideoQuality"] = self.combo_vq.currentIndex()
                indict["AudioQuality"] = self.combo_aq.currentIndex()
                indict["Output"] = self.lineEdit_dir.text()
                self.btn_download.setEnabled(False)
                self.btn_search.setEnabled(False)
                self.btn_pause.setEnabled(False)
                self.btn_stop.setEnabled(False)
                self.speedCalc(0)
                self.tes = biliWorker(indict, 2)
                self.tes.business_info.connect(self.businINFO_Catch)
                self.tes.progr_bar.connect(self.progress_Bar)
                self.tes.is_finished.connect(self.thread_finished)
                self.tes.interact_info.connect(self.interact_Catch)
                self.tes.Set_Structure(self.now_interact, {})
                self.threadBusy = True
                self.tes.start()
            else:
                count = self.media_list.count()
                indict["DownList"] = []
                for i in range(count):
                    if self.media_list.itemWidget(self.media_list.item(i)).isChecked():
                        indict["DownList"].append(i + 1)
                indict["VideoQuality"] = self.combo_vq.currentIndex()
                indict["AudioQuality"] = self.combo_aq.currentIndex()
                indict["Output"] = self.lineEdit_dir.text()
                self.btn_download.setEnabled(False)
                self.btn_search.setEnabled(False)
                self.speedCalc(0)
                if self.isAudio:
                    self.tes = biliWorker(indict, 4)
                else:
                    self.tes = biliWorker(indict, 1)
                self.tes.business_info.connect(self.businINFO_Catch)
                self.tes.progr_bar.connect(self.progress_Bar)
                self.tes.is_finished.connect(self.thread_finished)
                self.threadBusy = True
                self.tes.start()

    # 暂停下载按钮函数
    def pause_download(self):
        if self.btn_pause.text() == "暂停下载":
            if self.threadBusy:
                if self.tes.pause()!=False:
                    self.btn_pause.setText("恢复下载")
        else:
            if self.threadBusy:
                self.tes.resume()
                self.btn_pause.setText("暂停下载")

    # 停止下载事件函数
    def stop_download(self):
        if self.threadBusy:
            self.tes.close_process()

    # 打开高级设置窗口函数
    def set_config(self):
        if not self.threadBusy:
            self.setting_win = SettingWindow(indict)
            self.setting_win._signal.connect(self.setWindow_catch)
            self.setWindowOPEN = True
            self.setting_win.show()

    # 帮助按钮函数
    def forHELP(self):
        webbrowser.open("https://jimmyliang-lzm.github.io/2021/10/07/bilid_GUI_help/")

    # 打开关于页面函数
    def openAbout(self):
        self.about_win = AboutWindow()
        self.about_win.show()

    ####################### Slot function ##########################
    # 交互视频下载页面接收数据槽函数
    def interact_Page(self,indic):
        if indic == {}:
            self.plainTextEdit.appendPlainText("交互视频下载已取消")
            self.thread_finished(3)
            QApplication.processEvents()
        else:
            self.plainTextEdit.appendPlainText("交互视频开始下载")
            self.tes.Set_Structure(self.now_interact, indic)
            self.tes.model_set(3)
            self.btn_pause.setEnabled(True)
            self.btn_stop.setEnabled(True)
            self.tes.start()

    # 交互视频下载线程数据接收槽函数
    def interact_Catch(self, indic):
        if indic["state"] == 0:
            self.isInteractive = False
        elif indic["state"] == 1:
            self.isInteractive = True
            self.now_interact = indic["data"]
            self.plainTextEdit.appendPlainText("探查到本下载视频为交互视频。")
        elif indic["state"] == 2:
            self.now_interact = indic["nowin"]
            self.inv_page = InteractWindow(indic["ivf"], self.now_interact["vname"])
            self.inv_page._Signal.connect(self.interact_Page)
            self.inv_page.show()
        elif indic["state"] == -2:
            self.plainTextEdit.appendPlainText("节点信息探查出错。")

    # 下载线程事件反馈槽函数
    def businINFO_Catch(self, instr):
        if self.bu_info_count >= 2233:
            self.plainTextEdit.setPlainText("")
            self.bu_info_count = 0
        self.plainTextEdit.appendPlainText(instr)
        self.bu_info_count += 1

    # 视频质量列表接收槽函数
    def vqulityList(self,instr):
        self.combo_vq.addItem(instr)

    # 音频质量列表接收槽函数
    def aqulityList(self,instr):
        self.combo_aq.addItem(instr)

    # 分P视频表接收槽函数
    def mediaList(self,instr):
        item = QListWidgetItem()
        self.media_list.addItem(item)
        ck = QCheckBox(instr[1])
        if instr[0]:
            ck.setChecked(True)
        self.media_list.setItemWidget(item, ck)

    def progress_Show(self):
        in_dict = self.in_dict
        if in_dict["finish"] == 1:
            self.speedCalc(0)
            self.progressBar.setFormat("biliDownloader就绪")
            self.progressBar.setValue(0)
            QApplication.processEvents()
        elif in_dict["finish"] == 0:
            nowValue = 1000 * round(in_dict["Now"] / in_dict["Max"], 3)
            self.speedCalc(1)
            str_Text = "总大小：{} 已下载：{} 下载速度：{}/s 进度：%p%".format(
                self.filesizeShow(in_dict["Max"]), self.filesizeShow(in_dict["Now"]), self.filesizeShow(self.speed))
            # str_Text = "总大小：{} 已下载：{} 进度：%p%".format(
            #     self.filesizeShow(in_dict["Max"]), self.filesizeShow(in_dict["Now"]))
            self.progressBar.setFormat(str_Text)
            self.progressBar.setValue(nowValue)
        else:
            nowValue = 1000 * round(in_dict["Now"] / in_dict["Max"], 3)
            str_Text = "正在合成视频：%p%"
            self.progressBar.setFormat(str_Text)
            self.progressBar.setValue(nowValue)

    # 进度条进度信息接收槽函数
    def progress_Bar(self, in_dict):
        self.in_dict = in_dict

    # 下载速度计算函数
    def speedCalc(self,inum):
        if inum == 0:
            self.speed = 0
            self.after_size = 0
        elif inum == 1:
            # 1000/200ms
            self.speed = (self.in_dict["Now"] - self.after_size)*5
            self.after_size = self.in_dict["Now"]

    # 文件数据大小计算函数
    def filesizeShow(self, filesize):
        if filesize / 1024 > 1 :
            a = filesize / 1024
            if a / 1024 > 1:
                a = a / 1024
                if a / 1024 > 1:
                    a = a / 1024
                    if a / 1024 > 1:
                        return "TB".format(round(a/1024,1))
                    else:
                        return "{}GB".format(round(a,1))
                else:
                    return "{}MB".format(round(a,1))
            else:
                return "{}KB".format(round(a,1))
        else:
            return "{}B".format(round(filesize,1))

    # 下载线程结束信号接收槽函数
    def thread_finished(self,inum):
        self.threadBusy = False
        if inum == 1:
            self.haveINFO = True
            self.btn_search.setEnabled(True)
            self.groupBox.setEnabled(True)
        elif inum == 2:
            self.btn_search.setEnabled(True)
            self.btn_download.setEnabled(True)
        elif inum == 0:
            self.haveINFO = False
            self.btn_search.setEnabled(True)
            self.groupBox.setEnabled(True)
            self.plainTextEdit.appendPlainText("未找到视频资源，请您确认以下条件是否满足：\n"
                                        "1.计算机已联网并能正常访问到B站；\n"
                                        "2.您已经使用VIP Cookie进行下载；\n"
                                        "3.区域限制类视频您已配置有效的代理地址；\n"
                                        "4.视频资源能在浏览器里能被正常访问到。\n"
                                        "若您确定已经满足以上条件，请及时进入“关于程序”界面反馈BUG。")
        elif inum == 3:
            self.btn_download.setEnabled(True)
            self.btn_search.setEnabled(True)
            self.btn_pause.setEnabled(True)
            self.btn_stop.setEnabled(True)
        elif inum == 4:
            self.haveINFO = True
            self.btn_search.setEnabled(True)
            self.groupBox.setEnabled(True)
            self.isAudio = True


    # 高级设置窗口交互接收槽函数
    def setWindow_catch(self, in_dict):
        global indict
        if in_dict["code"] == 1:
            indict = in_dict["indict"]
            self.plainTextEdit.appendPlainText('设置成功（成功修改cookie与网络代理）')
            QApplication.processEvents()
        elif in_dict["code"] == 0:
            self.setWindowOPEN = False
        else:
            pass


############################################################################################
# 高级设置窗口类
class SettingWindow(QWidget,Objective_setting):
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


############################################################################################
# 关于窗口类
class AboutWindow(QWidget, Objective_about):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)
        self.Move = False
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
        self.btn_access.clicked.connect(self.accessWeb)
        self.btn_latest.clicked.connect(self.checkLatest)
        self.btn_bugCall.clicked.connect(self.callBUG)
        # 初始化显示设置
        self.lab_version.setText(Release_INFO[0])
        self.label_6.setText(Release_INFO[1])

    ####################### RW Part #######################
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

    ####################### BS Part #######################
    # 访问作者网站按钮函数
    def accessWeb(self):
        webbrowser.open("https://jimmyliang-lzm.github.io/")

    # 检查版本更新函数
    def checkLatest(self):
        self.cl = checkLatest(self.lab_version.text())
        self.btn_latest.setEnabled(False)
        self.cl._feedback.connect(self.verShow)
        self.cl.start()

    # 打开BUG反馈ISSUE页面
    def callBUG(self):
        webbrowser.open("https://github.com/JimmyLiang-lzm/biliDownloader_GUI/issues")

    ###### 槽函数 ######
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


############################################################################################
# 交互视频下载窗口类
class InteractWindow(QWidget, Objective_interact):
    _Signal = Signal(dict)
    def __init__(self, full_iv, vname, parent=None):
        super(InteractWindow, self).__init__(parent)
        assert type(full_iv) is dict
        assert type(vname) is str
        self.setupUi(self)
        self.Move = False
        self.feedback_dict = {}
        self.html_Path = DF_Path
        self.ivideo_name = self.name_replace(vname)
        self.lineEdit_height.setValidator(QIntValidator())
        self.lineEdit_width.setValidator(QIntValidator())
        # 设置窗口透明
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)
        # 设置鼠标动作位置
        self.m_Position = QPoint(0,0)
        # 连接器
        self.btnmin.clicked.connect(lambda: self.showMinimized())
        self.btn_adjsize.clicked.connect(self.re_show)
        self.btn_save2html.clicked.connect(self.save2html)
        self.btn_exportJSON.clicked.connect(self.save2json)
        self.btn_startdownload.clicked.connect(self.download_process)
        self.btn_nodeview.clicked.connect(self.show_chart)
        # 数据初始化
        self.full_json = full_iv
        self.chartdict = self.recursion_for_chart(full_iv)
        self.info_Init(full_iv,self.treeWidget_4)
        self.treeWidget_4.expandToDepth(2)
        self.draw_chart("670","420",self.chartdict)


    ####################### RW Part #######################
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
        # print(self.feedback_dict)
        self._Signal.emit(self.feedback_dict)

    ########################## BS PART #############################
    # 下载按钮->下载字典构建进程函数
    def download_process(self):
        n = self.treeWidget_4.topLevelItemCount()
        for i in range(n):
            item = self.treeWidget_4.topLevelItem(i)
            self.feedback_dict[item.text(0)] = {}
            if item.checkState(0) == Qt.Checked:
                self.feedback_dict[item.text(0)]["cid"] = item.text(1)
            self.feedback_dict[item.text(0)]["choices"] = self.download_list_make(item)
        self.close()

    # 属性选择框转下载字典递归函数
    def download_list_make(self,tree_widget_obj):
        temp = {}
        count = tree_widget_obj.childCount()
        if count == 0:
            return temp
        for i in range(count):
            name = tree_widget_obj.child(i).text(0)
            temp[name] = {}
            if tree_widget_obj.child(i).checkState(0) == Qt.Checked:
                temp[name]["cid"] = tree_widget_obj.child(i).text(1)
            temp[name]["choices"] = self.download_list_make(tree_widget_obj.child(i))
        return temp

    # Save origin node JSON File
    def save2json(self):
        init_path = indict["Output"] + "/" + self.ivideo_name + ".json"
        directory = QFileDialog.getSaveFileName(None,"选择JSON保存路径",init_path,'JSON(*.json)')
        if directory[0] != '':
            with open(directory[0],'w') as f:
                f.write(json.dumps(self.full_json, ensure_ascii=False))

    # Save node picture to HTML
    def save2html(self):
        init_path = indict["Output"]+"/"+self.ivideo_name+".html"
        directory = QFileDialog.getSaveFileName(None,'选择节点图保存路径',init_path,'HTML(*.html)')
        if directory[0] != '':
            self.node_chart.set_global_opts(title_opts=opts.TitleOpts(
                title=self.ivideo_name,
                subtitle="Made By BiliDownloader"))\
                .render(directory[0])

    # Re-size node picture.
    def re_show(self):
        w = self.lineEdit_width.text()
        h = self.lineEdit_height.text()
        self.draw_chart(w,h,self.chartdict)

    # File name conflict replace
    def name_replace(self, name):
        vn = name.replace(' ', '_').replace('\\', '').replace('/', '')
        vn = vn.replace('*', '').replace(':', '').replace('?', '').replace('<', '')
        vn = vn.replace('>', '').replace('\"', '').replace('|', '').replace('\x08','')
        return vn

    # 显示节点图
    def show_chart(self):
        dir_address = self.html_Path.replace("\\","/")+"/temp"
        if not os.path.exists(dir_address):
            os.makedirs(dir_address)
        self.node_chart.render(dir_address + "/node_temp.html")
        access_url = self.url_maker(dir_address + "/node_temp.html")
        webbrowser.open(access_url)

    # 跨系统平台节点文件路径生成函数
    def url_maker(self,in_dir):
        if indict["sys"] == "win32":
            return "file:///" + in_dir
        else:
            return "file://" + in_dir

    # 节点图绘制程序
    def draw_chart(self,width,height,indict):
        self.node_chart = (
            Tree(init_opts=opts.InitOpts(width=width+"px",height=height+"px"))
            .add(
                "",
                indict,
                collapse_interval=2,
                symbol="roundRect",
                initial_tree_depth=-1
            )
        )

    # 初始数据字典转化为树形图递归函数
    def info_Init(self,in_dict,root):
        for ch in in_dict:
            item = QTreeWidgetItem(root)
            item.setText(0,ch)
            item.setCheckState(0,Qt.Checked)
            item.setText(1,in_dict[ch]["cid"])
            item.addChild(self.info_Init(in_dict[ch]["choices"],item))

    # 初始数据字典转化图像专用JSON递归函数
    def recursion_for_chart(self,in_json):
        temp = []
        for ch in in_json:
            stemp = {"name":"","children":[]}
            stemp["name"] = ch
            stemp["children"] = self.recursion_for_chart(in_json[ch]["choices"])
            temp.append(stemp)
        return temp

    # 自动选择
    def onTreeClicked(self, item, num):
        # 如果是顶部节点，只考虑Child：
        if item.childCount() and not item.parent(): #判断是顶部节点，也就是根节点
            if item.checkState(0) == Qt.Unchecked: #规定点击根节点只有两态切换，没有中间态
                for i in range(item.childCount()): #遍历子节点进行状态切换
                    item.child(i).setCheckState(0, Qt.Unchecked)
            elif item.checkState(0) == Qt.Checked:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(0, Qt.Checked)

        # 如果是底部节点，只考虑Parent
        if item.parent() and not item.childCount():
            parent_item = item.parent() #获得父节点
            brother_item_num = parent_item.childCount() #获得兄弟节点的数目，包括自身在内
            checked_num = 0 #设置计数器
            for i in range(brother_item_num): #根据三态不同状态值进行数值累计
                checked_num += parent_item.child(i).checkState(0)
            if checked_num == 0: #最终结果进行比较，决定父节点的三态
                parent_item.setCheckState(0, Qt.Unchecked)
            elif checked_num/2 == brother_item_num:
                parent_item.setCheckState(0, Qt.Checked)
            else:
                parent_item.setCheckState(0, Qt.PartiallyChecked)

        # 中间层需要全面考虑
        if item.parent() and item.childCount():
            if item.checkState(0) == Qt.Unchecked: #规定点击根节点只有两态切换，没有中间态
                for i in range(item.childCount()): #遍历子节点进行状态切换
                    item.child(i).setCheckState(0, Qt.Unchecked)
            elif item.checkState(0) == Qt.Checked:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(0, Qt.Checked)
            parent_item = item.parent()  # 获得父节点
            brother_item_num = parent_item.childCount()  # 获得兄弟节点的数目，包括自身在内
            checked_num = 0  # 设置计数器
            for i in range(brother_item_num):  # 根据三态不同状态值进行数值累计
                checked_num += parent_item.child(i).checkState(0)
            if checked_num == 0:  # 最终结果进行比较，决定父节点的三态
                parent_item.setCheckState(0, Qt.Unchecked)
            elif checked_num / 2 == brother_item_num:
                parent_item.setCheckState(0, Qt.Checked)
            else:
                parent_item.setCheckState(0, Qt.PartiallyChecked)


############################################################################################
# 检查更新防阻滞线程类
class checkLatest(QThread):
    _feedback = Signal(int)
    def __init__(self, inVer):
        super(checkLatest, self).__init__()
        self.lab_version = inVer

    def ver2num(self,inVer):
        temp = inVer.replace("V","").split(".")
        temp = int(temp[0] + temp[1] + temp[2])
        return temp

    def run(self):
        try:
            des = request.get("https://jimmyliang-lzm.github.io/source_storage/biliDownloader_verCheck.json", timeout=5)
            res = json.loads(des.content.decode('utf-8'))["biliDownloader_GUI"]
            latestVer = self.ver2num(res)
            myVer = self.ver2num(self.lab_version)
            if latestVer <= myVer:
                self._feedback.emit(0)
                sleep(2)
                self._feedback.emit(-1)
            else:
                self._feedback.emit(1)
                webbrowser.open("https://github.com/JimmyLiang-lzm/biliDownloader_GUI/releases/latest")
                sleep(2)
        except Exception as e:
            print(e)
            self._feedback.emit(2)
            sleep(2)
            self._feedback.emit(-1)


############################################################################################
# 测试代理地址防阻滞线程类
class checkProxy(QThread):
    _feedback = Signal(dict)
    def __init__(self, in_Proxy):
        super(checkProxy, self).__init__()
        self.use_Proxy = in_Proxy
        self.index_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }

    def run(self):
        try:
            temp = {"code":1}
            des = request.get("https://api.live.bilibili.com/xlive/web-room/v1/index/getIpInfo",
                              headers=self.index_headers, timeout=10, stream=False, proxies=self.use_Proxy)
            res = json.loads(des.content.decode('utf-8'))["data"]
            temp["ip"] = res["addr"]
            temp["area"] = res["country"]
            self._feedback.emit(temp)
        except Exception as e:
            self._feedback.emit({"code":-1,"message":"测试失败"})


############################################################################################
# biliDownloader下载主工作线程
class biliWorker(QThread):
    # 信息槽发射
    business_info = Signal(str)
    vq_list = Signal(str)
    aq_list = Signal(str)
    media_list = Signal(list)
    progr_bar = Signal(dict)
    is_finished = Signal(int)
    interact_info = Signal(dict)
    # 初始化
    def __init__(self, args, model=0):
        super(biliWorker, self).__init__()
        self.run_model = model
        self.haveINFO = False
        self.pauseprocess = False
        self.subpON = False
        self.killprocess = False
        self.index_url = args["Address"]
        self.d_list = args["DownList"]
        self.VQuality = args["VideoQuality"]
        self.AQuality = args["AudioQuality"]
        self.output = args["Output"]
        self.synthesis = args["sym"]
        self.systemd = args["sys"]
        self.re_playinfo = 'window.__playinfo__=([\s\S]*?)</script>'
        self.re_INITIAL_STATE = 'window.__INITIAL_STATE__=([\s\S]*?);\(function'
        self.vname_expression = '<title(.*?)</title>'
        self.chunk_size = 1024
        self.index_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        self.second_headers = {
            "accept": "*/*",
            "Connection": "keep-alive",
            "accept-encoding": "identity",
            "accept-language": "zh-CN,zh;q=0.9",
            "origin": "https://www.bilibili.com",
            "sec-fetch-site": "cross-site",
            "sec-fetch-mode": "cors",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        if args["useCookie"]:
            self.index_headers["cookie"] = args["cookie"]
            self.second_headers["cookie"] = args["cookie"]
        else:
            self.index_headers["cookie"] = ""
            self.second_headers["cookie"] = ""
        if args["useProxy"]:
            self.Proxy = args["Proxy"]
        else:
            self.Proxy = {}

    # 运行模式设置函数
    def model_set(self, innum):
        self.run_model = innum

    # 结束进程函数
    def close_process(self):
        self.killprocess = True
        self.pauseprocess = False
        self.business_info.emit("正在结束下载进程......")

    # 暂停下载进程函数
    def pause(self):
        if self.subpON:
            self.business_info.emit("视频正在合成，只能终止不能暂停")
            return False
        else:
            self.business_info.emit("下载已暂停")
            self.pauseprocess = True

    # 恢复下载进程函数
    def resume(self):
        self.business_info.emit("下载已恢复")
        self.pauseprocess = False

    # File name conflict replace
    def name_replace(self, name):
        vn = name.replace(' ', '_').replace('\\', '').replace('/', '')
        vn = vn.replace('*', '').replace(':', '').replace('?', '').replace('<', '')
        vn = vn.replace('>', '').replace('\"', '').replace('|', '').replace('\x08','')
        return vn

    # Change /SS movie address
    def ssADDRCheck(self, inurl):
        # checking1:番剧首页视频地址检查； checking2:番剧单个视频地址检查
        checking1 = re.findall('/play/ss', inurl.split("?")[0], re.S)
        checking2 = re.findall('/play/ep', inurl.split("?")[0], re.S)
        try:
            if checking1 != []:
                res = request.get(inurl, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
                dec = res.content.decode('utf-8')
                INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
                temp = json.loads(INITIAL_STATE[0])
                self.index_url = temp["mediaInfo"]["episodes"][0]["link"]
                return 1, temp["mediaInfo"]["episodes"][0]["link"]
            elif checking2 != []:
                return 1, inurl
            else:
                return 0, inurl
        except Exception as e:
            print(e)
            return 0, inurl

    # Searching Key Word
    def search_preinfo(self, index_url):
        # Get Html Information
        index_url = self.ssADDRCheck(index_url)
        try:
            res = request.get(index_url[1], headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
            dec = res.content.decode('utf-8')
        except:
            print("初始化信息获取失败。")
            return 0, "", "", {}
        # Use RE to find Download JSON Data
        playinfo = re.findall(self.re_playinfo, dec, re.S)
        INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
        if playinfo == [] or INITIAL_STATE == []:
            print("Session等初始化信息获取失败。")
            return 0, "", "", {}
        # Bangumi Video
        re_init = json.loads(INITIAL_STATE[0])
        re_GET = json.loads(playinfo[0])
        # Normal Video
        # if index_url[0] == 0:
        #     now_cid = re_init["videoData"]["pages"][re_init["p"]-1]["cid"]
        #     try:
        #         makeurl = "https://api.bilibili.com/x/player/playurl?cid="+ str(now_cid) +\
        #                   "&qn=116&type=&otype=json&fourk=1&bvid="+ re_init["bvid"] +\
        #                   "&fnver=0&fnval=976&session=" + re_GET["session"]
        #         self.second_headers['referer'] = index_url[1]
        #         res = request.get(makeurl, headers=self.second_headers, stream=False, timeout=10, proxies=self.Proxy)
        #         re_GET = json.loads(res.content.decode('utf-8'))
        #         # print(json.dumps(re_GET))
        #     except Exception as e:
        #         print("获取Playlist失败:",e)
        #         return 0, "", "", {}
        # If Crawler can GET Data
        try:
            # Get video name
            vn1 = re.findall(self.vname_expression, dec, re.S)[0].split('>')[1]
            vn2 = ""
            if "videoData" in re_init:
                vn2 = re_init["videoData"]["pages"][re_init["p"] - 1]["part"]
            elif "mediaInfo" in re_init:
                vn2 = re_init["epInfo"]["titleFormat"] + ":" + re_init["epInfo"]["longTitle"]
            video_name = self.name_replace(vn1) + "_[" + self.name_replace(vn2) + "]"
            # List Video Quality Table
            length, down_dic = self.tmp_dffss(re_GET)
            # Return Data
            return 1, video_name, length, down_dic
        except Exception as e:
            print("PreInfo:",e)
            return 0, "", "", {}


    def tmp_dffss(self, re_GET):
        temp_v = {}
        for i in range(len(re_GET["data"]["accept_quality"])):
            temp_v[str(re_GET["data"]["accept_quality"][i])] = str(re_GET["data"]["accept_description"][i])
        # List Video Download Quality
        down_dic = {"video": {}, "audio": {}}
        i = 0
        # Get Video identity information and Initial SegmentBase.
        for dic in re_GET["data"]["dash"]["video"]:
            if str(dic["id"]) in temp_v:
                qc = temp_v[str(dic["id"])]
                down_dic["video"][i] = [qc, [dic["baseUrl"]], 'bytes=' + dic["SegmentBase"]["Initialization"]]
                for a in range(len(dic["backupUrl"])):
                    down_dic["video"][i][1].append(dic["backupUrl"][a])
                i += 1
            else:
                continue
        # List Audio Stream
        i = 0
        for dic in re_GET["data"]["dash"]["audio"]:
            au_stream = dic["codecs"] + "  音频带宽：" + str(dic["bandwidth"])
            down_dic["audio"][i] = [au_stream, [dic["baseUrl"]],
                                    'bytes=' + dic["SegmentBase"]["Initialization"]]
            for a in range(len(dic["backupUrl"])):
                down_dic["audio"][i][1].append(dic["backupUrl"][a])
            i += 1
        # Get Video Length
        length = re_GET["data"]["dash"]["duration"]
        return length, down_dic


    # Search the list of Video download address.
    def search_videoList(self, index_url):
        try:
            res = request.get(index_url, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
            dec = res.content.decode('utf-8')
        except:
            return 0, {}
        INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
        if INITIAL_STATE != []:
            try:
                re_init = json.loads(INITIAL_STATE[0])
                init_list = {}
                if "videoData" in re_init:
                    init_list["bvid"] = re_init["bvid"]
                    init_list["p"] = re_init["p"]
                    init_list["pages"] = re_init["videoData"]["pages"]
                    #print(init_list)
                    return 1, init_list
                elif "mediaInfo" in re_init:
                    init_list["bvid"] = re_init["mediaInfo"]["media_id"]
                    init_list["p"] = re_init["epInfo"]["i"] + 1
                    init_list["pages"] = re_init["mediaInfo"]["episodes"]
                    #print(init_list)
                    return 2, init_list
                else:
                    return 0, {}
            except Exception as e:
                print("videoList:",e)
                return 0, {}
        else:
            return 0, {}


    # Show preDownload Detail
    def show_preDetail(self):
        # flag,video_name,length,down_dic,init_list = self.search_preinfo()
        temp = self.search_preinfo(self.index_url)
        preList = self.search_videoList(self.index_url)
        self.business_info.emit('--------------------我是分割线--------------------')
        try:
            if temp[0] and preList[0] != 0:
                if preList[0] == 1:
                    # Show video pages
                    #self.business_info.emit("We Get!")
                    self.business_info.emit('当前需要下载的BV号为：{}'.format(preList[1]["bvid"]))
                    self.business_info.emit('当前BV包含视频数量为{}个'.format(len(preList[1]["pages"])))
                    for sp in preList[1]["pages"]:
                        form_str = "{}-->{}".format(sp["page"], sp["part"])
                        if sp["page"] == preList[1]["p"]:
                            self.media_list.emit([1,form_str])
                        else:
                            self.media_list.emit([0,form_str])
                elif preList[0] == 2:
                    # Show media pages
                    self.business_info.emit('当前需要下载的媒体号为：{}'.format(preList[1]["bvid"]))
                    self.business_info.emit('当前媒体包含视频数量为{}个'.format(len(preList[1]["pages"])))
                    #self.business_info.emit('-----------具体分P视频名称与下载号-----------')
                    i = 0
                    for sp in preList[1]["pages"]:
                        i += 1
                        form_str = "{}-->{}".format(i, sp["share_copy"])
                        if i == preList[1]["p"]:
                            self.media_list.emit([1,form_str])
                        else:
                            self.media_list.emit([0, form_str])
                self.business_info.emit('--------------------我是分割线--------------------')
                # Show Video Download Detail
                self.business_info.emit('当前下载视频名称：{}'.format(temp[1]))
                self.business_info.emit('当前下载视频长度： {} 秒'.format(temp[2]))
                #print('当前可下载视频流：')
                for i in range(len(temp[3]["video"])):
                    # print("{}-->视频画质：{}".format(i, temp[3]["video"][i][0]))
                    self.vq_list.emit("{}.{}".format(i+1, temp[3]["video"][i][0]))
                for i in range(len(temp[3]["audio"])):
                    # print("{}-->音频编码：{}".format(i, temp[3]["audio"][i][0]))
                    self.aq_list.emit("{}.{}".format(i+1, temp[3]["audio"][i][0]))
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
            return 0


    # Download Stream function
    def d_processor(self,url_list,output_dir,output_file,dest):
        for line in url_list:
            self.business_info.emit('使用线路：{}'.format(line.split("?")[0]))
            try:
                # video stream length sniffing
                video_bytes = request.get(line, headers=self.second_headers, stream=False, timeout=(5,10), proxies=self.Proxy)
                vc_range = video_bytes.headers['Content-Range'].split('/')[1]
                self.business_info.emit("获取{}流范围为：{}".format(dest,vc_range))
                self.business_info.emit('{}文件大小：{} MB'.format(dest,round(float(vc_range) / self.chunk_size / 1024), 4))
                # Get the full video stream
                proc = {"Max": int(vc_range), "Now": 0, "finish": 0}
                err = 0
                while(err <= 3):
                    try:
                        self.second_headers['range'] = 'bytes=' + str(proc["Now"]) + '-' + vc_range
                        m4sv_bytes = request.get(line, headers=self.second_headers, stream=True, timeout=10, proxies=self.Proxy)
                        self.progr_bar.emit(proc)
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                        with open(output_file, 'ab') as f:
                            for chunks in m4sv_bytes.iter_content(chunk_size=self.chunk_size):
                                while self.pauseprocess:
                                    sleep(1.5)
                                    if self.killprocess == True:
                                        return -1
                                if chunks:
                                    f.write(chunks)
                                    proc["Now"] += self.chunk_size
                                    self.progr_bar.emit(proc)
                                if self.killprocess == True:
                                    m4sv_bytes.close()
                                    return -1
                        if proc["Now"] >= proc["Max"]:
                            m4sv_bytes.close()
                            break
                        else:
                            print("服务器断开连接，重新连接下载端口....")
                    except Exception as e:
                        if re.findall('10054',str(e),re.S) == []:
                            err += 1
                        print(e,err)
                if err > 3:
                    raise Exception('线路出错，切换线路。')
                proc["finish"] = 1
                self.progr_bar.emit(proc)
                self.business_info.emit("{}成功！".format(dest))
                return 0
            except Exception as e:
                print(e)
                self.business_info.emit("{}出错：{}".format(dest,e))
                # print(proc)
                if os.path.exists(output_file):
                    os.remove(output_file)
        return 1

    # FFMPEG Synthesis Function
    def ffmpeg_synthesis(self,input_v,input_a,output_add):
        if os.path.exists(output_add):
            self.business_info.emit("文件：{}\n已存在。".format(output_add))
            return -1
        ffcommand = ""
        if self.systemd == "win32":
            ffpath = os.path.dirname(os.path.realpath(sys.argv[0]))
            ffcommand = ffpath + '/ffmpeg.exe -i "' + input_v + '" -i "' + input_a + '" -c:v copy -c:a aac -strict experimental "' + output_add + '"'
        elif self.systemd == "linux":
            ffcommand = 'ffmpeg -i ' + input_v + ' -i ' + input_a + ' -c:v copy -c:a aac -strict experimental ' + output_add
        elif self.systemd == "darwin":
            ffpath = os.path.dirname(os.path.realpath(sys.argv[0]))
            ffcommand = ffpath + '/ffmpeg -i ' + input_v + ' -i ' + input_a + ' -c:v copy -c:a aac -strict experimental ' + output_add
        else:
            self.business_info.emit("未知操作系统：无法确定FFMpeg命令。")
            return -2
        try:
            self.subpON = True
            temp = self.subp_GUIFollow(ffcommand)
            if temp:
                raise Exception(temp)
            self.subpON = False
            self.business_info.emit("视频合并完成！")
            os.remove(input_v)
            os.remove(input_a)
        except Exception as e:
            self.business_info.emit("视频合成失败：{}".format(e))
            self.subpON = False


    # Subprocess Progress of FFMPEG, RUN and Following Function
    def subp_GUIFollow(self, ffcommand):
        proc = {"Max": 100, "Now": 0, "finish": 2}
        subp = subprocess.Popen(ffcommand, shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        self.business_info.emit('FFMPEG正在执行合成指令')
        while True:
            status = subp.poll()
            if status != None:
                if status != 0:
                    self.business_info.emit("FFMPEG运行出错，代码：{}".format(status))
                    proc["finish"] = 1
                    self.progr_bar.emit(proc)
                    return status
                else:
                    proc["finish"] = 1
                    self.progr_bar.emit(proc)
                    return 0
            if self.killprocess:
                subp.stdin.write('q')
            line = os.read(subp.stderr.fileno(), 1024)
            if line:
                # print(line)
                sf = re.findall('Duration: ([\s\S]*?),', str(line), re.S)
                cf = re.findall('time=([\s\S]*?) bitrate=', str(line), re.S)
                if sf != []:
                    temp = sf[0]
                    temp = temp.split(".")[0].split(":")
                    num = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
                    #print("视频总长：", num)
                    proc["Max"] = num
                if cf != []:
                    temp = cf[0].split(".")[0].split(":")
                    cnum = int(temp[0]) * 3600 + int(temp[1]) * 60 + int(temp[2])
                    #print("当前进度", cnum)
                    proc["Now"] = cnum
                self.progr_bar.emit(proc)


    # For Download Single Video
    def Download_single(self, index=""):
        # Get video pre-detial
        if index == "":
            flag, video_name, _, down_dic = self.search_preinfo(self.index_url)
            index = self.index_url
        else:
            flag, video_name, _, down_dic = self.search_preinfo(index)
        # If we can access the video page
        if flag:
            try:
                # Judge file whether exists
                video_dir = self.output + '/' + video_name + '_video.m4s'
                audio_dir = self.output + '/' + video_name + '_audio.m4s'
                sym_video_dir = self.output + '/' + video_name + '.mp4'
                if os.path.exists(video_dir):
                    self.business_info.emit("文件：{}\n已存在。".format(video_dir))
                    return -1
                if os.path.exists(audio_dir):
                    self.business_info.emit("文件：{}\n已存在。".format(audio_dir))
                    return -1
                if os.path.exists(sym_video_dir):
                    self.business_info.emit("文件：{}\n已存在。".format(sym_video_dir))
                    return -1
                # self.business_info.emit("需要下载的视频：{}".format(video_name))
                # Perform video stream length sniffing
                self.second_headers['referer'] = index
                self.second_headers['range'] = down_dic["video"][self.VQuality][2]
                # Switch between main line and backup line(video).
                if self.killprocess:
                    return -2
                a = self.d_processor(down_dic["video"][self.VQuality][1], self.output, video_dir, "下载视频")
                # Perform audio stream length sniffing
                self.second_headers['range'] = down_dic["audio"][self.AQuality][2]
                # Switch between main line and backup line(audio).
                if self.killprocess:
                    return -2
                b = self.d_processor(down_dic["audio"][self.AQuality][1], self.output, audio_dir, "下载音频")
                if a or b:
                    return -3
                # Merge audio and video (USE FFMPEG)
                if self.killprocess:
                    return -2
                if self.synthesis:
                    self.business_info.emit('正在启动FFMPEG......')
                    # Synthesis processor
                    self.ffmpeg_synthesis(video_dir, audio_dir, sym_video_dir)
            except Exception as e:
                print(e)
        else:
            self.business_info.emit("下载失败：尚未找到源地址，请检查网站地址或充值大会员！")


    # For Download partition Video
    def Download_List(self):
        r_list = self.d_list
        all_list = self.search_videoList(self.index_url)
        preIndex = self.index_url.split("?")[0]
        # print(all_list,r_list)
        # print(preIndex)
        if all_list[0] == 1:
            if r_list[0] == 0:
                for p in all_list[1]["pages"]:
                    if self.killprocess:
                        break
                    self.Download_single(preIndex + "?p=" + str(p["page"]))
            else:
                listLEN = len(all_list[1]["pages"])
                for i in r_list:
                    if self.killprocess:
                        break
                    if i <= listLEN:
                        self.Download_single(preIndex + "?p=" + str(i))
                    else:
                        continue
            self.business_info.emit("列表视频下载进程结束！")
        elif all_list[0] == 2:
            if r_list[0] == 0:
                for p in all_list[1]["pages"]:
                    if self.killprocess:
                        break
                    self.Download_single(p["link"])
            else:
                listLEN = len(all_list[1]["pages"])
                for i in r_list:
                    if self.killprocess:
                        break
                    if i <= listLEN:
                        self.Download_single(all_list[1]["pages"][i - 1]["link"])
                    else:
                        continue
            self.business_info.emit("媒体视频下载进程结束！")
        else:
            self.business_info.emit("未找到视频列表信息。")

    ###################################################################
    # 交互进程初始数据获取函数
    def interact_preinfo(self):
        self.now_interact = {"cid": "", "bvid": "", "session": "", "graph_version": "", "node_id": "", "vname": ""}
        t1 = self.Get_Init_Info(self.index_url)
        self.index_headers['referer'] = self.index_url
        self.second_headers = self.index_headers
        t2 = self.isInteract()
        if t1[0] or t2[0]:
            return 1, {}, {}
        return 0, self.now_interact

    # 交互视频节点分析函数
    def interact_nodeList(self):
        self.business_info.emit("开始分析互动视频节点，若长时间（10分钟）未弹出画面说明互动视频存在循环或进程坏死，请退出本程序...")
        self.business_info.emit("-----------------------------------------------------------------------------------------")
        self.now_interact = {"cid": "", "bvid": "", "session": "", "graph_version": "", "node_id": "", "vname": ""}
        self.Get_Init_Info(self.index_url)
        self.index_headers['referer'] = self.index_url
        self.second_headers = self.index_headers
        self.isInteract()
        self.iv_structure = {}
        self.iv_structure[self.now_interact["vname"]] = {}
        self.iv_structure[self.now_interact["vname"]] = self.recursion_GET_List("初始节点")
        self.business_info.emit("节点探查完毕，窗口加载中...")
        return self.iv_structure

    # Interactive video download
    def requests_start(self, now_interact,iv_structure):
        self.now_interact = now_interact
        self.recursion_for_Download(iv_structure, self.output)
        self.business_info.emit("下载交互视频完成。")

    # 设置预下载信息
    def Set_Structure(self, now_interact,iv_structure):
        self.now_interact = now_interact
        self.iv_structure = iv_structure

    # Interactive video initial information
    def Get_Init_Info(self, url):
        try:
            res = request.get(url, headers=self.index_headers, stream=False,timeout=10, proxies=self.Proxy)
            dec = res.content.decode('utf-8')
            playinfo = re.findall(self.re_playinfo, dec, re.S)
            INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
            if playinfo == [] or INITIAL_STATE == []:
                raise Exception("无法找到初始化信息。")
            playinfo = json.loads(playinfo[0])
            INITIAL_STATE = json.loads(INITIAL_STATE[0])
            self.now_interact["session"] = playinfo["session"]
            self.now_interact["bvid"] = INITIAL_STATE["bvid"]
            self.now_interact["cid"] = str(INITIAL_STATE["cidMap"][INITIAL_STATE["bvid"]]["cids"]["1"])
            self.now_interact["vname"] = self.name_replace(INITIAL_STATE["videoData"]["title"])
            return 0, ""
        except Exception as e:
            return 1, str(e)

    # Judge the interactive video.
    def isInteract(self):
        make_API = "https://api.bilibili.com/x/player/v2?cid=" + self.now_interact["cid"] + "&bvid=" + \
                   self.now_interact["bvid"]
        try:
            res = request.get(make_API, headers=self.index_headers, stream=False,timeout=10, proxies=self.Proxy)
            des = json.loads(res.content.decode('utf-8'))
            if "interaction" not in des["data"]:
                raise Exception("非交互视频")
            self.now_interact["graph_version"] = str(des["data"]["interaction"]["graph_version"])
            return 0, ""
        except Exception as e:
            return 1, str(e)

    # Get interactive video pre-information
    def down_list_make(self, cid_num):
        make_API = "https://api.bilibili.com/x/player/playurl?cid=" + cid_num \
                   + "&bvid=" + self.now_interact[
                       "bvid"] + "&qn=116&type=&otype=json&fourk=1&fnver=0&fnval=976&session=" + \
                   self.now_interact["session"]
        try:
            des = request.get(make_API, headers=self.index_headers, stream=False,timeout=10, proxies=self.Proxy)
            playinfo = json.loads(des.content.decode('utf-8'))
        except Exception as e:
            return False, str(e)
        if playinfo != {}:
            re_GET = playinfo
            # List Video Quality Table
            length, down_dic = self.tmp_dffss(re_GET)
            # Return Data
            return True, length, down_dic
        else:
            return False, "Get Download List Error."

    # Get interactive video node list (Use recursion algorithm)
    def recursion_GET_List(self, inword):
        temp = {"choices": {}}
        temp["cid"] = self.now_interact["cid"]
        if self.now_interact["node_id"] == "":
            make_API = "https://api.bilibili.com/x/stein/nodeinfo?bvid=" + self.now_interact[
                "bvid"] + "&graph_version=" + self.now_interact["graph_version"]
        else:
            make_API = "https://api.bilibili.com/x/stein/nodeinfo?bvid=" + self.now_interact[
                "bvid"] + "&graph_version=" + self.now_interact["graph_version"] + "&node_id=" + self.now_interact[
                           "node_id"]
        try:
            des = request.get(make_API, headers=self.index_headers, stream=False,timeout=10, proxies=self.Proxy)
            desp = json.loads(des.content.decode('utf-8'))
        except Exception as e:
            self.business_info.emit("获取节点信息出现网络问题：节点提取可能不全")
            print("Interactive Video Get List Error:",e)
            return temp
        if "edges" not in desp["data"]:
            return temp
        for ch in desp["data"]["edges"]["choices"]:
            self.now_interact["cid"] = str(ch["cid"])
            self.now_interact["node_id"] = str(ch["node_id"])
            self.business_info.emit(inword +"-->"+ch["option"])
            temp["choices"][ch["option"]] = self.recursion_GET_List(inword +"-->"+ch["option"])
        return temp

    # Interactive video download processor (Use recursion algorithm)
    def recursion_for_Download(self, json_list, output_dir):
        for ch in json_list:
            chn = self.name_replace(ch)
            output = output_dir + "/" + chn
            video_dir = output + "/" + chn + '_video.m4s'
            audio_dir = output + "/" + chn + '_audio.m4s'
            if "cid" in json_list[ch]:
                dic_return = self.down_list_make(json_list[ch]["cid"])
                if not dic_return[0]:
                    self.business_info.emit("节点（{}）获取下载地址出错".format(ch))
                    print(dic_return[1])
                    return -1
                _, _, down_dic = dic_return
                self.second_headers["range"] = down_dic["video"][self.VQuality][2]
                self.d_processor(down_dic["video"][self.VQuality][1], output, video_dir, "下载视频：" + chn)
                self.second_headers['range'] = down_dic["audio"][self.AQuality][2]
                self.d_processor(down_dic["audio"][self.AQuality][1], output, audio_dir, "下载音频：" + chn)
                if self.synthesis:
                    self.business_info.emit('正在启动ffmpeg......')
                    self.ffmpeg_synthesis(video_dir, audio_dir, output + '/' + chn + '.mp4')
            self.recursion_for_Download(json_list[ch]["choices"], output)
        return 0

    ###################################################################
    # 音频进程
    def search_AUPreinfo(self, au_url):
        # check1:音乐歌单页面检测；check2:单个音乐页面检测
        check1 = re.findall(r'/audio/am(\d+)', au_url, re.S)
        check2 = re.findall(r'/audio/au(\d+)', au_url, re.S)
        if check1 != []:
            # print(check1[0])
            temps = self.AuList_Maker(check1[0], 2)
            if temps[0]:
                # print(json.dumps(temps[1]))
                return 1, temps[1]
            else:
                return 0, "Audio List Get Error."
        elif check2 != []:
            # print(check2[0])
            temps = self.AuList_Maker(check2[0], 1)
            if temps[0]:
                # print(json.dumps(temps[1]))
                return 2, temps[1]
            else:
                return 0, "Audio Single Get Error."
        else:
            print("Is NOT Music.")
            return 0, {}

    def AuList_Maker(self, sid, modeNUM):
        list_dict = {"audio":[],"total":0}
        if modeNUM == 1:
            try:
                makeURL = "https://www.bilibili.com/audio/music-service-c/web/song/info?sid=" + sid
                res = request.get(makeURL, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
                des = res.content.decode('utf-8')
                auinfo = json.loads(des)["data"]
                temp = {}
                temp["title"] = auinfo["title"]+"_"+auinfo["author"]
                temp["sid"] = sid
                temp["cover"] = auinfo["cover"]
                temp["duration"] = auinfo["duration"]
                temp["lyric"] = auinfo["lyric"]
                list_dict["audio"].append(temp)
                list_dict["total"] = 1
            except Exception as e:
                print("AuList_Maker_Single:",e)
                return 0, "AuList_Maker_Single:{}".format(e)
            return 1, list_dict
        elif modeNUM == 2:
            try:
                pn = 1
                while True:
                    makeURL = "https://www.bilibili.com/audio/music-service-c/web/song/of-menu?sid="+sid+"&pn="+str(pn)+"&ps=30"
                    res = request.get(makeURL, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
                    des = res.content.decode('utf-8')
                    mu_dic = json.loads(des)["data"]
                    for sp in mu_dic["data"]:
                        # print(sp)
                        temp = {}
                        temp["title"] = sp["title"] + "_" + sp["author"]
                        temp["sid"] = str(sp["id"])
                        temp["cover"] = sp["cover"]
                        temp["duration"] = sp["duration"]
                        temp["lyric"] = sp["lyric"]
                        list_dict["audio"].append(temp)
                        list_dict["total"] += 1
                    if pn >= mu_dic["pageCount"]:
                        break
                    else:
                        pn += 1
                        continue
            except Exception as e:
                print("AuList_Maker_List:",e)
                return 0, "AuList_Maker_List:{}".format(e)
            return 1, list_dict
        else:
            return 0, "ModeNum Error."

    # 显示音频信息
    @property
    def Audio_Show(self):
        au_dic = self.search_AUPreinfo(self.index_url)
        if au_dic[0] == 0:
            print(au_dic[1])
            return 0
        if au_dic[0] == 1:
            self.business_info.emit('当前歌单包含音乐数量为{}个'.format(au_dic[1]["total"]))
        elif au_dic[0] == 2:
            self.business_info.emit('当前下载歌曲名称为：{}'.format(au_dic[1]["audio"][0]["title"]))
            self.business_info.emit('歌曲长度为：{}'.format(au_dic[1]["audio"][0]["duration"]))
        else:
            return 0
        i = 0
        for sp in au_dic[1]["audio"]:
            i += 1
            form_make = "{}-->{}".format(i,sp["title"])
            self.media_list.emit([0,form_make])
        self.vq_list.emit("无")
        self.aq_list.emit("最高音质")
        return 1

    # 获取单个音频下载地址
    def Audio_getDownloadList(self, sid):
        make_url = "https://www.bilibili.com/audio/music-service-c/web/url?sid="+sid
        res = request.get(make_url, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
        des = res.content.decode('utf-8')
        au_list = json.loads(des)["data"]["cdns"]
        return au_list

    # 附带资源下载
    def simple_downloader(self, url, output_dir, output_file):
        try:
            res = request.get(url, headers=self.index_headers, timeout=10, proxies=self.Proxy)
            file = res.content
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(output_file, 'wb') as f:
                f.write(file)
        except Exception as e:
            self.business_info.emit("附带下载失败：{}".format(url))
            print("附带下载失败：",e)


    # 音乐下载函数
    def audio_downloader(self):
        self.second_headers["referer"] = "https://www.bilibili.com/"
        self.second_headers["sec-fetch-dest"] = 'audio'
        self.second_headers["sec-fetch-mode"] = 'no-cors'
        temp_dic = self.search_AUPreinfo(self.index_url)
        if temp_dic[0] == 0:
            self.business_info.emit("获取音乐前置信息出错。")
            return 0
        try:
            for index in self.d_list:
                sp = temp_dic[1]["audio"][index-1]
                output_dir = self.output + "/" + self.name_replace(sp["title"])
                output_name = output_dir + "/" + self.name_replace(sp["title"])
                self.business_info.emit("正在下载音乐：{}".format(sp["title"]))
                if sp["cover"] != "":
                    self.simple_downloader(sp["cover"],output_dir,output_name+"_封面.jpg")
                if sp["lyric"] != "":
                    self.simple_downloader(sp["lyric"],output_dir,output_name+"_歌词.lrc")
                au_downlist = self.Audio_getDownloadList(sp["sid"])
                self.second_headers["range"] = 'bytes=0-'
                self.d_processor(au_downlist,output_dir,output_name+".mp3","下载音乐")
            self.business_info.emit("音乐下载进程结束！")
            return 1
        except Exception as e:
            self.business_info.emit("音频下载出错：{}".format(e))
            print("音频下载出错：",e)
            return 0

    ###################################################################
    # 运行线程
    def run(self):
        #self.reloader()
        if self.run_model == 0:
            # 探查资源类型
            self.interact_info.emit({"state":0})
            d = self.interact_preinfo()
            r = self.show_preDetail()
            if r == 1:
                if d[0] == 0:
                    self.interact_info.emit({"state":1,"data":d[1]})
                self.is_finished.emit(1)
            elif self.Audio_Show:
                self.is_finished.emit(4)
            else:
                self.is_finished.emit(0)
        elif self.run_model == 1:
            # 下载非交互视频
            if self.d_list != []:
                # print(1)
                self.Download_List()
                if self.killprocess:
                    self.business_info.emit("下载已终止")
                self.progr_bar.emit({"finish": 1})
                self.is_finished.emit(2)
            else:
                self.is_finished.emit(2)
        elif self.run_model == 2:
            # 交互视频信息读取
            d = self.interact_nodeList()
            if d == {}:
                self.interact_info.emit({"state":-2,"data":{}})
                self.is_finished.emit(3)
            else:
                self.interact_info.emit({"state":2,"nowin":self.now_interact,"ivf":d})
        elif self.run_model == 3:
            # 交互视频下载
            self.requests_start(self.now_interact,self.iv_structure)
            self.is_finished.emit(3)
        elif self.run_model == 4:
            # 音频列表下载
            if self.d_list != []:
                self.audio_downloader()
                if self.killprocess:
                    self.business_info.emit("下载已终止")
                self.progr_bar.emit({"finish": 1})
                self.is_finished.emit(2)
            else:
                self.is_finished.emit(2)


######################################################################
# 程序入口
if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
