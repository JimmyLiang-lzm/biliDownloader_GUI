import sys, os, webbrowser
import requests, json, re, subprocess
from time import time,sleep
from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QCheckBox, QListWidgetItem, QFileDialog, QWidget
from PySide6.QtCore import Qt, QThread, Signal, QPoint
import biliDownloader, bilidabout, bilidsetting

# Initialize
Objective = biliDownloader.Ui_MainWindow
Objective_setting = bilidsetting.Ui_Form
Objective_about = bilidabout.Ui_Form
DF_Path = os.path.dirname(os.path.realpath(sys.argv[0]))
indict = {"Address":"","DownList":[],"VideoQuality":0,"AudioQuality":0,"Output":"","Synthesis":1,"sys":"","cookie":"","sym":True,"useCookie":False}

# Mainwindow Class
class MainWindow(QMainWindow,Objective):
    def __init__(self, parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.threadBusy = False
        self.haveINFO = False
        self.allSelect = False
        self.setWindowOPEN = False
        # 设置窗口透明
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground,True)
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
        self.btn_changecookie.clicked.connect(self.set_cookie)
        self.btn_help.clicked.connect(self.forHELP)
        self.btn_about.clicked.connect(self.openAbout)
        # 默认目录
        self.lineEdit_dir.setText(DF_Path)
        indict["Output"] = DF_Path
        try:
            with open(DF_Path + '/setting.conf', 'r', encoding='utf-8') as f:
                tempr = json.loads(f.read())
                indict["sys"] = tempr["sys"]
                indict["cookie"] = tempr["cookie"]
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
            indict["sys"] = sys.platform
            self.checkBox_sym.setChecked(True)

    ####################### RW Part ##########################
    # 鼠标点击事件产生
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    # 退出事件记录
    def closeEvent(self,QCloseEvent):
        with open(DF_Path + '/setting.conf', 'w', encoding='utf-8') as f:
            temp_dict = {"UseCookie":indict["useCookie"],"synthesis":indict["sym"],"cookie":indict["cookie"],"sys":indict["sys"]}
            f.write(json.dumps(temp_dict,sort_keys=True,indent=4))
            f.close()

    ####################### BS Part ##########################
    def Get_preInfo(self):
        #print(indict)
        indict["Address"] = self.source_search.text()
        self.combo_vq.clear()
        self.combo_aq.clear()
        self.media_list.clear()
        self.tes = biliWorker(indict,0)
        self.tes.business_info.connect(self.businINFO_Catch)
        self.tes.vq_list.connect(self.vqulityList)
        self.tes.aq_list.connect(self.aqulityList)
        self.tes.media_list.connect(self.mediaList)
        self.tes.is_finished.connect(self.thread_finished)
        self.btn_search.setEnabled(False)
        self.groupBox.setEnabled(False)
        self.threadBusy = True
        self.tes.start()

    def selectDir(self):
        directory = QFileDialog.getExistingDirectory(None,"选择文件夹",indict["Output"])
        if directory != "":
            self.lineEdit_dir.setText(directory)
        QApplication.processEvents()

    def useCookie(self):
        if self.checkBox_usecookie.isChecked():
            indict["useCookie"] = True
        else:
            indict["useCookie"] = False

    def useSym(self):
        if self.checkBox_sym.isChecked():
            indict["sym"] = True
        else:
            indict["sym"] = False

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

    def download(self):
        if self.haveINFO:
            count = self.media_list.count()
            indict["DownList"] = []
            for i in range(count):
                if self.media_list.itemWidget(self.media_list.item(i)).isChecked():
                    indict["DownList"].append(i+1)
            indict["VideoQuality"] = self.combo_vq.currentIndex()
            indict["AudioQuality"] = self.combo_aq.currentIndex()
            indict["Output"] = self.lineEdit_dir.text()
            self.btn_download.setEnabled(False)
            self.btn_search.setEnabled(False)
            self.speedCalc(0)
            self.tes = biliWorker(indict,1)
            self.tes.business_info.connect(self.businINFO_Catch)
            self.tes.progr_bar.connect(self.progress_Bar)
            self.tes.is_finished.connect(self.thread_finished)
            self.threadBusy = True
            self.tes.start()

    def pause_download(self):
        if self.btn_pause.text() == "暂停下载":
            if self.threadBusy:
                if self.tes.pause()!=False:
                    self.btn_pause.setText("恢复下载")
        else:
            if self.threadBusy:
                self.tes.resume()
                self.btn_pause.setText("暂停下载")

    def stop_download(self):
        if self.threadBusy:
            self.tes.close_process()

    def set_cookie(self):
        if not self.threadBusy:
            self.setting_win = SettingWindow(indict["cookie"])
            self.setting_win._signal.connect(self.setWindow_catch)
            self.setWindowOPEN = True
            self.setting_win.show()

    def forHELP(self):
        webbrowser.open("https://jimmyliang-lzm.github.io/2021/10/06/bilid_GUI_help/")

    def openAbout(self):
        self.about_win = AboutWindow()
        self.about_win.show()

    # 槽函数
    def businINFO_Catch(self, instr):
        self.plainTextEdit.appendPlainText(instr)

    def vqulityList(self,instr):
        self.combo_vq.addItem(instr)

    def aqulityList(self,instr):
        self.combo_aq.addItem(instr)

    def mediaList(self,instr):
        item = QListWidgetItem()
        self.media_list.addItem(item)
        self.media_list.setItemWidget(item, QCheckBox(instr))

    def progress_Bar(self, in_dict):
        if in_dict["finish"] == 1:
            self.progressBar.setFormat("biliDownloader就绪")
            self.progressBar.setValue(0)
        elif in_dict["finish"] == 0:
            nowValue = round(1000000*in_dict["Now"]/in_dict["Max"])
            self.speedCalc(1)
            str_Text = "总大小：{} 已下载：{} 下载速度：{}/s 进度：%p%".format(
                self.filesizeShow(in_dict["Max"]),self.filesizeShow(in_dict["Now"]),self.filesizeShow(self.speed))
            self.progressBar.setFormat(str_Text)
            self.progressBar.setValue(nowValue)
        else:
            nowValue = round(1000000*in_dict["Now"]/in_dict["Max"])
            str_Text = "正在合成视频：%p%"
            self.progressBar.setFormat(str_Text)
            self.progressBar.setValue(nowValue)

    def speedCalc(self,inum):
        if inum == 0:
            self.speed = 0
            self.calc = 0
            self.Time = time()
            self.showTime = time()
        elif inum == 1:
            self.calc += 1
            if time() - self.showTime >= 0.25:
                time_between = time() - self.Time
                if time_between != 0:
                    self.speed = 1024*self.calc/time_between
                    self.calc = 0
                    self.Time = time()
                self.showTime = time()

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

    def setWindow_catch(self, in_dict):
        if in_dict["code"] == 1:
            indict["cookie"] = in_dict["cookie"]
            self.plainTextEdit.appendPlainText('已成功修改Cookie')
            QApplication.processEvents()
        elif in_dict["code"] == 0:
            self.setWindowOPEN = False
        else:
            pass

############################################################################################
# Cookie设置窗口类
class SettingWindow(QWidget,Objective_setting):
    _signal = Signal(dict)
    def __init__(self, incookie, parent=None):
        super(SettingWindow,self).__init__(parent)
        self.setupUi(self)
        self.edit_cookies.setPlainText(incookie)
        # 设置窗口透明
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 设置鼠标动作位置
        self.m_Position = 0
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(30)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)
        # 连接器
        self.btnmin.clicked.connect(lambda: self.showMinimized())
        self.btn_editcookie.clicked.connect(self.setCookie)
        self.btn_cleanplain.clicked.connect(self.clearTEXT)
        self.btn_wherecookie.clicked.connect(self.forHelp)
    ####################### RW Part ##########################
    # 鼠标点击事件产生
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    # 定义关闭事件
    def closeEvent(self, QCloseEvent):
        self._signal.emit({"code":0})

    ####################### BS Part ##########################
    # 设置Cookie
    def setCookie(self):
        cookie = self.edit_cookies.toPlainText()
        self._signal.emit({"code":1,"cookie":cookie})
        self.close()

    # 清空编辑框
    def clearTEXT(self):
        self.edit_cookies.clear()

    # 帮助按钮
    def forHelp(self):
        webbrowser.open("https://zmtechn.gitee.io/2021/10/05/Get_bilibili_cookie/")

############################################################################################
# 关于窗口类
class AboutWindow(QWidget, Objective_about):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置窗口透明
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 设置鼠标动作位置
        self.m_Position = 0
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

    ####################### RW Part #######################
    # 鼠标点击事件产生
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    ####################### BS Part #######################
    def accessWeb(self):
        webbrowser.open("https://jimmyliang-lzm.github.io/")

    def checkLatest(self):
        self.cl = checkLatest(self.lab_version.text())
        self.btn_latest.setEnabled(False)
        self.cl._feedback.connect(self.verShow)
        self.cl.start()

    def accessRelease(self):
        webbrowser.open("https://github.com/JimmyLiang-lzm/biliDownloader_GUI/releases")

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
# 检查更新防阻滞线程类
class checkLatest(QThread):
    _feedback = Signal(int)
    def __init__(self, inVer):
        super(checkLatest, self).__init__()
        self.lab_version = inVer

    def run(self):
        try:
            des = requests.get("https://jimmyliang-lzm.github.io/source_storage/biliDownloader_verCheck.json",timeout=5)
            res = json.loads(des.content.decode('utf-8'))["biliDownloader_GUI"]
            if res == self.lab_version:
                self._feedback.emit(0)
                sleep(2)
                self._feedback.emit(-1)
            else:
                self._feedback.emit(1)
                webbrowser.open("https://github.com/JimmyLiang-lzm/biliDownloader_GUI/releases")
                sleep(2)
        except Exception as e:
            print(e)
            self._feedback.emit(2)
            sleep(2)
            self._feedback.emit(-1)

############################################################################################
# biliDownloader下载主工作线程
class biliWorker(QThread):
    # 信息槽发射
    business_info = Signal(str)
    vq_list = Signal(str)
    aq_list = Signal(str)
    media_list = Signal(str)
    progr_bar = Signal(dict)
    is_finished = Signal(int)
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

    def close_process(self):
        self.killprocess = True
        self.pauseprocess = False
        self.business_info.emit("正在结束下载进程......")

    def pause(self):
        if self.subpON:
            self.business_info.emit("视频正在合成，只能终止不能暂停")
            return False
        else:
            self.business_info.emit("下载已暂停")
            self.pauseprocess = True

    def resume(self):
        self.business_info.emit("下载已恢复")
        self.pauseprocess = False

    # File name conflict replace
    def name_replace(self, name):
        vn = name.replace(' ', '_').replace('\\', '').replace('/', '')
        vn = vn.replace('*', '').replace(':', '').replace('?', '').replace('<', '')
        vn = vn.replace('>', '').replace('\"', '').replace('|', '')
        return vn

    # Change /SS movie address
    def ssADDRCheck(self, inurl):
        checking = re.findall('/play/ss', inurl.split("?")[0], re.S)
        try:
            if checking != []:
                res = requests.get(inurl, headers=self.index_headers, stream=False, timeout=10)
                dec = res.content.decode('utf-8')
                INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
                temp = json.loads(INITIAL_STATE[0])
                self.index_url = temp["mediaInfo"]["episodes"][0]["link"]
                return temp["mediaInfo"]["episodes"][0]["link"]
            else:
                return inurl
        except Exception as e:
            print(e)
            return inurl

    # Searching Key Word
    def search_preinfo(self, index_url):
        # Get Html Information
        index_url = self.ssADDRCheck(index_url)
        try:
            res = requests.get(index_url, headers=self.index_headers, stream=False, timeout=10)
            dec = res.content.decode('utf-8')
        except:
            return 0, "", "", {}
        # Use RE to find Download JSON Data
        playinfo = re.findall(self.re_playinfo, dec, re.S)
        INITIAL_STATE = re.findall(self.re_INITIAL_STATE, dec, re.S)
        # If Crawler can GET Data
        if playinfo != [] and INITIAL_STATE != []:
            try:
                #print(playinfo[0])
                re_init = json.loads(INITIAL_STATE[0])
                re_GET = json.loads(playinfo[0])
                # Get video name
                vn1 = re.findall(self.vname_expression, dec, re.S)[0].split('>')[1]
                vn2 = ""
                if "videoData" in re_init:
                    vn2 = re_init["videoData"]["pages"][re_init["p"] - 1]["part"]
                elif "mediaInfo" in re_init:
                    vn2 = re_init["epInfo"]["titleFormat"] + ":" + re_init["epInfo"]["longTitle"]
                video_name = self.name_replace(vn1) + "_[" + self.name_replace(vn2) + "]"
                # List Video Quality Table
                temp_v = {}
                for i in range(len(re_GET["data"]["accept_quality"])):
                    temp_v[str(re_GET["data"]["accept_quality"][i])] = str(re_GET["data"]["accept_description"][i])
                # List Video Download Quality
                down_dic = {"video": {}, "audio": {}}
                i = 0
                # Get Video identity information and Initial SegmentBase.
                #print(1)
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
                #print(2)
                for dic in re_GET["data"]["dash"]["audio"]:
                    au_stream = dic["codecs"] + "  音频带宽：" + str(dic["bandwidth"])
                    down_dic["audio"][i] = [au_stream, [dic["baseUrl"]],
                                            'bytes=' + dic["SegmentBase"]["Initialization"]]
                    for a in range(len(dic["backupUrl"])):
                        down_dic["audio"][i][1].append(dic["backupUrl"][a])
                    i += 1
                # Get Video Length
                length = re_GET["data"]["dash"]["duration"]
                # Return Data
                #print(down_dic)
                return 1, video_name, length, down_dic
            except Exception as e:
                print("PreInfo:",e)
                return 0, "", "", {}
        else:
            return 0, "", "", {}

    # Search the list of Video download address.
    def search_videoList(self, index_url):
        try:
            res = requests.get(index_url, headers=self.index_headers, stream=False, timeout=10)
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
                    init_list["p"] = re_init["epInfo"]["i"]
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
                    #self.business_info.emit('-----------具体分P视频名称与下载号-----------')
                    for sp in preList[1]["pages"]:
                        self.media_list.emit("{}-->{}".format(sp["page"], sp["part"]))
                elif preList[0] == 2:
                    # Show media pages
                    self.business_info.emit('当前需要下载的媒体号为：{}'.format(preList[1]["bvid"]))
                    self.business_info.emit('当前媒体包含视频数量为{}个'.format(len(preList[1]["pages"])))
                    #self.business_info.emit('-----------具体分P视频名称与下载号-----------')
                    for sp in preList[1]["pages"]:
                        self.media_list.emit("{}-->{}".format(sp["title"], sp["share_copy"]))
                self.business_info.emit('--------------------我是分割线--------------------')
                # Show Video Download Detail
                self.business_info.emit('当前下载视频名称：{}'.format(temp[1]))
                self.business_info.emit('当前下载视频长度： {} 秒'.format(temp[2]))
                #print('当前可下载视频流：')
                for i in range(len(temp[3]["video"])):
                    #print("{}-->视频画质：{}".format(i, temp[3]["video"][i][0]))
                    self.vq_list.emit("{}.{}".format(i+1, temp[3]["video"][i][0]))
                for i in range(len(temp[3]["audio"])):
                    #print("{}-->音频编码：{}".format(i, temp[3]["audio"][i][0]))
                    self.aq_list.emit("{}.{}".format(i+1, temp[3]["audio"][i][0]))
                return 1
            else:
                self.business_info.emit("尚未找到源地址，请检查网站地址或充值大会员！")
                return 0
        except Exception as e:
            print(e)
            return 0


    # Download Stream fuction
    def d_processor(self,url_list,output_dir,dest):
        for line in url_list:
            self.business_info.emit('使用线路：{}'.format(line.split("?")[0]))
            try:
                # video stream length sniffing
                video_bytes = requests.get(line, headers=self.second_headers, stream=False, timeout=(5,10))
                vc_range = video_bytes.headers['Content-Range'].split('/')[1]
                self.business_info.emit("获取{}流范围为：{}".format(dest,vc_range))
                self.business_info.emit('{}文件大小：{} MB'.format(dest,round(float(vc_range) / self.chunk_size / 1024), 4))
                # Get the full video stream
                proc = {"Max": 0, "Now": 0, "finish": 0}
                err = 0
                while(err <= 3):
                    try:
                        self.second_headers['range'] = 'bytes=' + str(proc["Now"]) + '-' + vc_range
                        m4sv_bytes = requests.get(line, headers=self.second_headers, stream=True, timeout=10)
                        proc["Max"] = int(vc_range)
                        self.progr_bar.emit(proc)
                        with open(output_dir, 'ab') as f:
                            for chunks in m4sv_bytes.iter_content(chunk_size=self.chunk_size):
                                while self.pauseprocess:
                                    sleep(1.5)
                                if chunks:
                                    f.write(chunks)
                                    proc["Now"] += self.chunk_size
                                    self.progr_bar.emit(proc)
                                if self.killprocess == True:
                                    return -1
                        break
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
                print(proc)
                os.remove(output_dir)
        return 1


    # FFMPEG Synthesis fuction
    def ffmpeg_synthesis(self,input_v,input_a,output_add):
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
            self.business_info.emit("视频合成失败：", e)
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
                if os.path.exists(video_dir):
                    self.business_info.emit("文件：{}\n已存在。".format(video_dir))
                    return -1
                if os.path.exists(audio_dir):
                    self.business_info.emit("文件：{}\n已存在。".format(audio_dir))
                    return -1
                # self.business_info.emit("需要下载的视频：{}".format(video_name))
                # Perform video stream length sniffing
                self.second_headers['referer'] = index
                self.second_headers['range'] = down_dic["video"][self.VQuality][2]
                # Switch between main line and backup line(video).
                if self.killprocess:
                    return -2
                a = self.d_processor(down_dic["video"][self.VQuality][1], video_dir, "下载视频")
                # Perform audio stream length sniffing
                self.second_headers['range'] = down_dic["audio"][self.AQuality][2]
                # Switch between main line and backup line(audio).
                if self.killprocess:
                    return -2
                b = self.d_processor(down_dic["audio"][self.AQuality][1], audio_dir, "下载音频")
                if a or b:
                    return -3
                # Merge audio and video (USE FFMPEG)
                if self.killprocess:
                    return -2
                if self.synthesis:
                    self.business_info.emit('正在启动ffmpeg......')
                    # Synthesis processor
                    self.ffmpeg_synthesis(video_dir, audio_dir, self.output + '/' + video_name + '.mp4')
            except Exception as e:
                print(e)
        else:
            self.business_info.emit("下载失败：尚未找到源地址，请检查网站地址或充值大会员！")


    # For Download partition Video
    def Download_List(self):
        # r_list = self.args2list()
        r_list = self.d_list
        all_list = self.search_videoList(self.index_url)
        preIndex = self.index_url.split("?")[0]
        # print(2)
        # print(all_list,r_list)
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


    def run(self):
        #self.reloader()
        if self.run_model == 0:
            r = self.show_preDetail()
            if r == 1:
                self.is_finished.emit(1)
            else:
                self.is_finished.emit(0)
        elif self.run_model == 1:
            if self.d_list != []:
                # print(1)
                self.Download_List()
                if self.killprocess:
                    self.business_info.emit("下载已终止")
                self.progr_bar.emit({"finish": 1})
                self.is_finished.emit(2)
            else:
                self.is_finished.emit(2)

######################################################################
# 程序入口
if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
