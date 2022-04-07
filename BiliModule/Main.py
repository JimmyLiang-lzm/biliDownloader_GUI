from etc import *
from BiliModule.About import AboutWindow
from BiliModule.Setting import SettingWindow
from BiliModule.Interact import biliInteractMainWindow

from BiliWorker.main import biliWorker
from BiliWorker.extra import *
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QCheckBox, QListWidgetItem, QFileDialog
from PySide2.QtCore import Qt, QPoint, QTimer
from UI.biliDownloader import Ui_MainWindow



class MainWindow(QMainWindow, Ui_MainWindow):
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
                # 新代码
                self.iv_tes = biliInteractMainWindow(indict)
                self.iv_tes._Signal.connect(self.interact_Page)
                self.iv_tes.show()
                # 老代码
                # self.tes = biliWorker(indict, 2)
                # self.tes.business_info.connect(self.businINFO_Catch)
                # self.tes.progr_bar.connect(self.progress_Bar)
                # self.tes.is_finished.connect(self.thread_finished)
                # self.tes.interact_info.connect(self.interact_Catch)
                # self.tes.Set_Structure(self.now_interact, {})
                # self.threadBusy = True
                # self.tes.start()
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
        if not indic:
            self.plainTextEdit.appendPlainText("交互视频下载已取消")
            self.thread_finished(3)
            QApplication.processEvents()
        else:
            self.plainTextEdit.appendPlainText("交互视频开始下载")
            # 新代码
            self.tes.progr_bar.connect(self.progress_Bar)
            self.tes.Set_Structure(indic['baseInfo'], indic['indic'])
            self.tes.model_set(3)
            self.btn_pause.setEnabled(True)
            self.btn_stop.setEnabled(True)
            self.threadBusy = True
            self.tes.start()
            # 老代码
            # self.tes.Set_Structure(self.now_interact, indic)
            # self.tes.model_set(3)
            # self.btn_pause.setEnabled(True)
            # self.btn_stop.setEnabled(True)
            # self.tes.start()


    # 交互视频下载线程数据接收槽函数
    def interact_Catch(self, indic):
        if indic["state"] == 0:
            self.isInteractive = False
        elif indic["state"] == 1:
            self.isInteractive = True
            self.now_interact = indic["data"]
            self.plainTextEdit.appendPlainText("探查到本下载视频为交互视频。")
        # 老代码
        # elif indic["state"] == 2:
        #     self.now_interact = indic["nowin"]
        #     self.inv_page = InteractWindow(indic["ivf"], self.now_interact["vname"])
        #     self.inv_page._Signal.connect(self.interact_Page)
        #     self.inv_page.show()
        elif indic["state"] == -2:
            self.plainTextEdit.appendPlainText("节点信息探查出错。")
        else:
            pass


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
