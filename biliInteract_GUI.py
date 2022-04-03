import os, sys, webbrowser
import json, re
from pathlib import Path
import requests as request
from PySide2.QtCore import QThread, Signal, Qt, QPoint, QSize
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect, QApplication, QTreeWidgetItem, QVBoxLayout, QCheckBox, QLabel, QListWidgetItem, QFileDialog, QMessageBox
from PySide2.QtGui import QPixmap
from pyecharts.charts import Tree
from pyecharts import options as opts

from UI import biliInteractive_new

Object_Interactive_main = biliInteractive_new.Ui_Form

##############################################################################
# 交互视频处理主界面
class biliInteractMainWindow(QWidget, Object_Interactive_main):
    _Signal = Signal(dict)
    def __init__(self, args, parent=None):
        super(biliInteractMainWindow, self).__init__(parent)
        self.feedback_dict = {'dlmode': -1,}
        self.setupUi(self)
        self.Move = False
        # 节点树形框字典初始化
        self.treelist_dict = {}
        # 节点路径数组与节点深度信息初始化
        self.current_path = []
        self.choos = []
        self.pre_load = ''
        # 节点图对象
        self.node_chart = None
        # 节点访问线程对象
        self.iv_init = None
        # 初始化缓存路径
        self.cache_Path = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.list_NodeChoose.clear()
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
        self.m_Position = QPoint(0, 0)
        # 连接器
        self.btnmin.clicked.connect(lambda: self.showMinimized())
        self.btn_adjsize.clicked.connect(self.re_show)
        self.btn_nodeview.clicked.connect(self.show_chart)
        self.btn_save2html.clicked.connect(self.save2html)
        self.btn_exportJSON.clicked.connect(self.save2json)
        self.btn_next.clicked.connect(self.go_next_node)
        self.btn_back.clicked.connect(self.go_back_node)
        self.btn_refreash.clicked.connect(self.renew_show)
        self.tw_nodelist.itemClicked['QTreeWidgetItem*','int'].connect(self.item_setCheck)
        self.tw_nodelist.itemDoubleClicked['QTreeWidgetItem*','int'].connect(self.item_setNodePosition)
        self.btn_downCurChoose.clicked.connect(self.dl_current_node)
        # 初始化变量
        self.init_args = args
        self.info_init()

    # 初始化交互视频信息
    def info_init(self):
        self.base_info = {"bvid": "", "session": "", "vname": "", "graph_version": "", "cid": "", "node_id": "", "curname":""}
        self.init_args['imgcache'] = self.cb_showimage.isChecked()
        self.init_args['cache_path'] = self.cache_Path
        self.iv_init = biliWorker_interact(self.init_args)
        self.iv_init.back_result.connect(self.Slot_Handle)
        self.iv_init.run()

    # 更新显示信息
    def renew_show(self):
        self.lab_ivName.setText(self.base_info["vname"])
        self.base_info["curname"] = self.current_path[-1]
        self.lab_curchoose.setText(self.base_info["curname"])
        # print(json.dumps(self.treelist_dict))
        self.tw_nodelist.clear()
        self.renew_treelist(self.treelist_dict, self.tw_nodelist)
        self.tw_nodelist.expandAll()
        self.renew_chooselist()
        self.show_current_node()
        self.chartdict = self.recursion_for_chart(self.treelist_dict)
        self.lab_curStatus.setText("加载完毕")

    # 刷新树形框的显示
    def renew_treelist(self, in_dict, root):
        for ch in in_dict:
            item = QTreeWidgetItem(root)
            item.setText(0, ch)
            if in_dict[ch]["isChoose"]:
                item.setCheckState(0, Qt.Checked)
            else:
                item.setCheckState(0, Qt.Unchecked)
            item.setText(1, in_dict[ch]["cid"])
            if "choices" in in_dict[ch]:
                item.addChild(self.renew_treelist(in_dict[ch]["choices"], item))

    # 刷新选择窗口的选项
    def renew_chooselist(self):
        temp = self.get_current_list(self.current_path.copy(), 1)
        # 显示节点信息
        if 'node_id' in temp:
            self.lab_curNID.setText(temp["node_id"])
        if 'choices' in temp:
            temp = temp['choices']
        else:
            temp = {}
        if temp:
            self.list_NodeChoose.clear()
            self.choos.clear()
            # for zh in temp['choices']:
            for zh in temp:
                item = QListWidgetItem()
                item.setSizeHint(QSize(215, 160))
                widget = self.choose_item_widget(zh, temp[zh]['cid'])
                self.list_NodeChoose.addItem(item)
                self.list_NodeChoose.setItemWidget(item, widget)
        else:
            self.list_NodeChoose.clear()
            self.choos.clear()
            print('节点结束')

    # 单个节点选项样式函数
    def choose_item_widget(self, node_name, cid):
        # 总体框架
        widget = QWidget()
        # 总体纵向布局
        layout_main = QVBoxLayout()
        layout_top = QCheckBox(node_name)
        self.choos.append(layout_top)
        layout_main.addWidget(layout_top)
        if self.cb_showimage.isChecked():
            layout_img = QLabel()
            layout_img.setFixedSize(192,108)
            cache_img_path = self.cache_Path + "/temp/" + cid + "_node.jpg"
            if Path(cache_img_path).is_file():
                img = QPixmap(cache_img_path).scaled(192, 108)
            else:
                img = QPixmap(self.cache_Path + "/images/live_default.png").scaled(192, 108)
            layout_img.setPixmap(img)
            layout_main.addWidget(layout_img)
        widget.setLayout(layout_main)
        # widget.
        return widget

    # 显示当前所在节点
    def show_current_node(self):
        self.le_nodeway.clear()
        self.le_nodeway.setText(self.current_path[-1])
        print('位置指引' ,self.current_path)

    # 获取当前节点的选择信息字典
    def get_current_list(self, path: list, mode: int):
        tmp = self.treelist_dict.copy()
        for ch in path[:-1]:
            if 'choices' in tmp[ch]:
                tmp = tmp[ch]['choices']
            else:
                return {}
        # 判断输出为选项还是该节点信息
        if (mode == 0) and ('choices' in tmp[path[-1]]):
            tmp = tmp[path[-1]]['choices']
            return tmp
        elif mode == 1:
            tmp = tmp[path[-1]]
            return tmp
        else:
            return {}


    def get_curNode_info(self, path):
        tmp = self.treelist_dict.copy()
        for ch in path:
            pass


    def recursion_dict_update(self, input_dict: dict, keyPath: list, editKey, editValue):
        tmp = input_dict
        if len(keyPath) > 1:
            ckey = keyPath[0]
            tmp[ckey]['choices'] = self.recursion_dict_update(tmp[ckey]['choices'], keyPath[1:], editKey, editValue)
        else:
            tmp[keyPath[0]][editKey] = editValue
        return tmp

    # 探查下一节点
    def go_next_node(self):
        # 获取当前节点信息
        chooses = []
        self.lab_curStatus.setText('正在加载……')
        for cb in self.choos:
            if cb.isChecked():
                chooses.append(cb.text())
        if len(chooses) != 1:
            QMessageBox.information(self, '信息', '你需要选择一个选项哦~')
            return -1
        # 判断是否已探查到
        tmp = self.get_current_list(self.current_path.copy(), 0)[chooses[0]]
        self.pre_load = chooses[0]
        if 'choices' in tmp:
            if tmp['choices']:
                self.current_path.append(self.pre_load)
                self.renew_show()
            else:
                QMessageBox.information(self, '信息', '互动视频这条路已经结束咧！')
                return -1
        else:
            # 获取已选选项node_id
            node_id = tmp['node_id']
            if not self.iv_init:
                QMessageBox.information(self, '对象错误', '请关闭并重新载入本窗口！')
                return -1
            if not self.iv_init.change_method(1, node_id=node_id):
                return -1
            self.iv_init.run()
            # print(node_id)
        return 0


    # 回到上一节点
    def go_back_node(self):
        if len(self.current_path) <= 1:
            QMessageBox.information(self, '信息', '你已回到最初的起点~')
            return 0
        self.current_path.pop()
        self.renew_show()
        return 0


    # 设置Treedict的选中下载
    def item_setCheck(self, item, column):
        # 获取该条目的结构路径
        path = self.get_item_path(item)
        # 判断是否选中
        dict_status = False
        if item.checkState(0) == Qt.Checked:
            dict_status = True
        self.recursion_dict_update(self.treelist_dict, path, 'isChoose', dict_status)


    # 设置显示节点位置
    def item_setNodePosition(self, item, columu):
        tree_path = self.get_item_path(item)
        feed = self.get_current_list(tree_path, 0)
        if not feed:
            return -1
        self.current_path = tree_path
        self.renew_show()
        return 0


    # 获取条目路径
    def get_item_path(self, item):
        tmp = []
        if not item:
            return tmp
        tmp.extend(self.get_item_path(item.parent()))
        tmp.append(item.text(0))
        return tmp


    # 初始数据字典转化图像专用JSON递归函数
    def recursion_for_chart(self, in_json):
        temp = []
        for ch in in_json:
            stemp = {"name": "", "children": []}
            stemp["name"] = ch
            # print(in_json[ch])
            if "choices" in in_json[ch]:
                stemp["children"] = self.recursion_for_chart(in_json[ch]["choices"])
            temp.append(stemp)
        return temp

    # 节点图绘制程序
    def draw_chart(self, width, height, indict):
        self.node_chart = (
            Tree(init_opts=opts.InitOpts(width=width + "px", height=height + "px"))
                .add(
                "",
                indict,
                collapse_interval=2,
                symbol="roundRect",
                initial_tree_depth=-1
            )
        )

    # Re-size node picture.
    def re_show(self):
        w = self.lineEdit_width.text()
        h = self.lineEdit_height.text()
        self.draw_chart(w, h, self.chartdict)

    # 查看节点图
    def show_chart(self):
        dir_address = self.cache_Path.replace("\\","/") + "/temp"
        if not os.path.exists(dir_address):
            os.makedirs(dir_address)
        if not self.node_chart:
            self.re_show()
        self.node_chart.render(dir_address + "/node_temp.html")
        access_url = self.url_maker(dir_address + "/node_temp.html")
        webbrowser.open(access_url)

    # 访问URL制作
    def url_maker(self,in_dir):
        if sys.platform == "win32":
            return "file:///" + in_dir
        else:
            return "file://" + in_dir

    # 节点图保存为网页
    def save2html(self):
        init_path = self.init_args["Output"] + "/" + self.base_info["vname"] + ".html"
        directory = QFileDialog.getSaveFileName(None,'选择节点图保存路径',init_path,'HTML(*.html)')
        if not self.node_chart:
            self.re_show()
        if directory[0] != '':
            self.node_chart.set_global_opts(title_opts=opts.TitleOpts(
                title=self.ivideo_name,
                subtitle="Made By BiliDownloader"))\
                .render(directory[0])

    # 导出节点JSON
    def save2json(self):
        init_path = self.init_args["Output"] + "/" + self.base_info["vname"] + ".json"
        directory = QFileDialog.getSaveFileName(None, "选择JSON保存路径", init_path, 'JSON(*.json)')
        if directory[0] != '':
            with open(directory[0],'w') as f:
                f.write(json.dumps(self.full_json, ensure_ascii=False))


    # 下载当前节点处理函数
    def dl_current_node(self):
        pass

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
        self._Signal.emit(self.feedback_dict)
        for f in os.listdir(self.cache_Path + "/temp"):
            if f.endswith('_node.jpg'):
                os.remove(self.cache_Path + "/temp/" + f)

    ####################### Slot function ##########################
    # 进程反馈信息处理主函数
    def Slot_Handle(self, indict):
        if indict['code'] == 0:
            # Static variable
            self.base_info["bvid"] = indict['data']['bvid']
            self.base_info["session"] = indict['data']['session']
            self.base_info['graph_version'] = indict['data']['graph_version']
            self.base_info["vname"] = indict['data']['vname']
            # Current Variable
            self.base_info["cid"] = indict['data']['cid']
            self.base_info["node_id"] = indict['data']['node_id']
            self.base_info["curname"] = indict['data']['vname']
            # Renew Listdict
            self.treelist_dict[self.base_info["curname"]] = {}
            self.treelist_dict[self.base_info["curname"]]['choices'] = indict["nodelist"]
            self.treelist_dict[self.base_info["curname"]]['cid'] = indict['data']['cid']
            self.treelist_dict[self.base_info["curname"]]['isChoose'] = False
            # Renew Current path
            self.current_path.append(self.base_info["curname"])
            # Renew Show
            self.renew_show()
        elif indict['code'] == 1:
            # 修改字典
            print(self.treelist_dict)
            if indict['nodelist']:
                self.current_path.append(self.pre_load)
                self.treelist_dict = self.recursion_dict_update(self.treelist_dict, self.current_path, 'choices', indict['nodelist'])
                self.renew_show()
            else:
                tmp = self.current_path.copy()
                tmp.append(self.pre_load)
                self.treelist_dict = self.recursion_dict_update(self.treelist_dict, tmp, 'choices', indict['nodelist'])
                self.lab_curStatus.setText('加载完毕')
                QMessageBox.information(self, '信息', '互动视频这条路已经结束咧！')
            print(self.treelist_dict)

        elif indict['code'] == -1:
            self.lab_curStatus.setText(indict['data'])
        else:
            pass




##############################################################################
# Bili交互视频处理总进程
class biliWorker_interact(QThread):
    #信号发射定义
    business_info = Signal(str)
    back_result = Signal(dict)
    # 初始化
    def __init__(self, args, model=0, parent=None):
        super(biliWorker_interact, self).__init__(parent)
        self.model = model
        self.index_url = args['url']
        self.index_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        self.re_playinfo = 'window.__playinfo__=([\s\S]*?)</script>'
        self.re_INITIAL_STATE = 'window.__INITIAL_STATE__=([\s\S]*?);\(function'
        if args["useCookie"]:
            self.index_headers["cookie"] = args["cookie"]
            self.second_headers["cookie"] = args["cookie"]
        else:
            self.index_headers["cookie"] = ""
            # self.second_headers["cookie"] = ""
        if args["useProxy"]:
            self.Proxy = args["Proxy"]
        else:
            self.Proxy = {}
        self.iscache = args['imgcache']
        self.cache_path = args['cache_path']+"/temp"

    ###################################################################
    # BiliDOwnloader基础功能
    # File name conflict replace
    def name_replace(self, name):
        vn = name.replace(' ', '_').replace('\\', '').replace('/', '')
        vn = vn.replace('*', '').replace(':', '').replace('?', '').replace('<', '')
        vn = vn.replace('>', '').replace('\"', '').replace('|', '').replace('\x08', '')
        return vn

    ###################################################################
    # 交互进程初始数据获取函数
    def interact_preinfo(self):
        self.now_interact = {"cid": "", "bvid": "", "session": "", "graph_version": "", "node_id": "", "vname": ""}
        t1 = self.Get_Init_Info(self.index_url)
        if t1[0]:
            return 1, {}, {}
        self.index_headers['referer'] = self.index_url
        self.second_headers = self.index_headers
        t2 = self.isInteract()
        if t2[0]:
            return 1, {}, {}
        print(self.now_interact)
        t3 = self.Get_Edge()
        if t3[0]:
            return 1, {}, {}
        return 0, self.now_interact, t3[1]

    # 改变线程运行模式
    def change_method(self, mode: int, **kwargs):
        # 单节点探查模式
        self.model = mode
        if mode == 1:
            if not kwargs.get('node_id'):
                return False
            self.now_interact['node_id'] = kwargs.get('node_id')
            return True
        # 递归探查模式
        elif mode == 2:
            return False
        else:
            return False

    # # 交互视频节点分析函数
    # def interact_nodeList(self):
    #     self.business_info.emit("开始分析互动视频节点，若长时间（10分钟）未弹出画面说明互动视频存在循环或进程坏死，请退出本程序...")
    #     self.business_info.emit(
    #         "-----------------------------------------------------------------------------------------")
    #     self.now_interact = {"cid": "", "bvid": "", "session": "", "graph_version": "", "node_id": "", "vname": ""}
    #     if self.Get_Init_Info(self.index_url) != 0:
    #         return -1
    #     self.index_headers['referer'] = self.index_url
    #     self.second_headers = self.index_headers
    #     if self.isInteract() != 0:
    #         return -1
    #     self.iv_structure = {}
    #     self.iv_structure[self.now_interact["vname"]] = {}
    #     self.iv_structure[self.now_interact["vname"]] = self.recursion_GET_List("初始节点")
    #     self.business_info.emit("节点探查完毕，窗口加载中...")
    #     return self.iv_structure
    #
    # # Interactive video download
    # def requests_start(self, now_interact, iv_structure):
    #     self.now_interact = now_interact
    #     self.recursion_for_Download(iv_structure, self.output)
    #     self.business_info.emit("下载交互视频完成。")
    #
    # # 设置预下载信息
    # def Set_Structure(self, now_interact, iv_structure):
    #     self.now_interact = now_interact
    #     self.iv_structure = iv_structure

    # Interactive video initial information
    def Get_Init_Info(self, url):
        try:
            res = request.get(url, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
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
        make_API = "https://api.bilibili.com/x/player/v2"
        param = {
            'cid': self.now_interact["cid"],
            'bvid': self.now_interact["bvid"],
        }
        try:
            res = request.get(make_API, headers=self.index_headers, params=param, timeout=10, proxies=self.Proxy)
            des = json.loads(res.content.decode('utf-8'))
            if "interaction" not in des["data"]:
                raise Exception("非交互视频")
            self.now_interact["graph_version"] = str(des["data"]["interaction"]["graph_version"])
            return 0, ""
        except Exception as e:
            return 1, str(e)

    # Edge Choose Search
    def Get_Edge(self):
        temp = {}
        make_API = "https://api.bilibili.com/x/stein/nodeinfo"
        param = {
            'bvid': self.now_interact["bvid"],
            'graph_version': self.now_interact["graph_version"],
        }
        if self.now_interact["node_id"] != "":
            param['node_id'] = self.now_interact["node_id"]
        try:
            des = request.get(make_API, headers=self.index_headers, params=param, timeout=10, proxies=self.Proxy)
            res = json.loads(des.content.decode('utf-8'))
        except Exception as e:
            print("Get Edges:",e)
            return 1, "获取节点失败（网络连接错误）"
        if "edges" not in res["data"]:
            return 0, temp
        for ch in res["data"]["edges"]["choices"]:
            temp[ch["option"]] = {}
            temp[ch["option"]]["cid"] = str(ch["cid"])
            temp[ch["option"]]["node_id"] = str(ch["node_id"])
            temp[ch["option"]]["isChoose"] = False
            if self.iscache:
                self.img_cache(temp[ch["option"]]["cid"])
        return 0, temp

    # 节点缩略图下载
    def img_cache(self, cid):
        url = "https://i0.hdslb.com/bfs/steins-gate/" + cid + "_screenshot.jpg"
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)
        output_file = self.cache_path + "/" + cid + "_node.jpg"
        if Path(output_file).is_file():
            return 0
        try:
            res = request.get(url, headers=self.index_headers, timeout=10, proxies=self.Proxy)
            file = res.content
            with open(output_file, 'wb') as f:
                f.write(file)
            return 0
        except Exception as e:
            self.business_info.emit("附带下载失败：{}".format(url))
            print("附带下载失败：", e)
            return 1


    # # Get interactive video node list (Use recursion algorithm)
    # def recursion_GET_List(self, inword):
    #     temp = {"choices": {}}
    #     temp["cid"] = self.now_interact["cid"]
    #     if self.now_interact["node_id"] == "":
    #         make_API = "https://api.bilibili.com/x/stein/nodeinfo?bvid=" + self.now_interact[
    #             "bvid"] + "&graph_version=" + self.now_interact["graph_version"]
    #     else:
    #         make_API = "https://api.bilibili.com/x/stein/nodeinfo?bvid=" + self.now_interact[
    #             "bvid"] + "&graph_version=" + self.now_interact["graph_version"] + "&node_id=" + self.now_interact[
    #                        "node_id"]
    #     try:
    #         des = request.get(make_API, headers=self.index_headers, stream=False, timeout=10, proxies=self.Proxy)
    #         desp = json.loads(des.content.decode('utf-8'))
    #     except Exception as e:
    #         self.business_info.emit("获取节点信息出现网络问题：节点提取可能不全")
    #         print("Interactive Video Get List Error:", e)
    #         return temp
    #     if "edges" not in desp["data"]:
    #         return temp
    #     for ch in desp["data"]["edges"]["choices"]:
    #         self.now_interact["cid"] = str(ch["cid"])
    #         self.now_interact["node_id"] = str(ch["node_id"])
    #         self.business_info.emit(inword + "-->" + ch["option"])
    #         temp["choices"][ch["option"]] = self.recursion_GET_List(inword + "-->" + ch["option"])
    #     return temp

    # Start Worker Thread
    def run(self) -> None:
        if self.model == 0:
            res = self.interact_preinfo()
            if res[0]:
                self.back_result.emit({'code': -1, 'data': '获取初始信息失败'})
            self.back_result.emit({'code':0,'data':res[1], 'nodelist':res[2]})
        elif self.model == 1:
            res = self.Get_Edge()
            if res[0]:
                self.back_result.emit({'code':-1,'data':'获取节点信息失败'})
            self.back_result.emit({'code': 1, 'nodelist': res[1]})
        else:
            print("操作指令有误:",self.model)
            self.back_result.emit({'code':-1,'data':'操作指令有误'})


if __name__ == '__main__':
    args = {
        'url':'https://www.bilibili.com/video/BV1Kb4y1v79e',
        'useProxy':False,
        'proxy':{},
        'useCookie':False,
        'cookie':'',
        'Output': 'G:/Cache',
    }
    app = QApplication(sys.argv)
    InteractiveWindow = biliInteractMainWindow(args)
    InteractiveWindow.show()
    sys.exit(app.exec_())
