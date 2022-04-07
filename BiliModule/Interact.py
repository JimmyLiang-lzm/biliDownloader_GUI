import os, sys
import json, webbrowser
from pathlib import Path
from PySide2.QtCore import Signal, Qt, QPoint, QSize
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect, QApplication, QTreeWidgetItem, QVBoxLayout, QCheckBox, QLabel, QListWidgetItem, QFileDialog, QMessageBox
from PySide2.QtGui import QPixmap
from pyecharts.charts import Tree
from pyecharts import options as opts

from UI.biliInteractive import Ui_Form
from BiliWorker.extra import biliWorker_interact, BiliImgCache
from BiliModule.RThread import RecurThreadWindow


##############################################################################
# 交互视频处理主界面
class biliInteractMainWindow(QWidget, Ui_Form):
    _Signal = Signal(dict)
    def __init__(self, args, parent=None):
        super(biliInteractMainWindow, self).__init__(parent)
        self.feedback_dict = {}
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
        self.btn_downALLChoose.clicked.connect(self.dl_all_chooses)
        self.btn_stRecu.clicked.connect(self.st_recursion)
        # 初始化变量
        self.init_args = args
        self.info_init()


    # 初始化交互视频信息
    def info_init(self):
        self.base_info = {"bvid": "", "session": "", "vname": "", "graph_version": "", "cid": "", "node_id": "", "curname":""}
        self.init_args['imgcache'] = self.cb_showimage.isChecked()
        self.init_args['cache_path'] = self.cache_Path
        # 初始化缓存系统
        self.IMGCache_SYS = BiliImgCache(self.init_args)
        # 初始化交互视频探查系统
        self.iv_init = biliWorker_interact(self.init_args)
        self.iv_init.back_result.connect(self.Slot_Handle)
        # 运行初始化信息查询
        self.iv_init.start()

    # 更新显示信息
    def renew_show(self):
        print(self.treelist_dict)
        # 判断是否需要图片缓存并择机开启图片缓存系统
        if self.cb_showimage.isChecked() and (not self.IMGCache_SYS.busy):
            self.IMGCache_SYS.setRecurDict(self.treelist_dict)
            self.IMGCache_SYS.start()
        # 刷新信息框显示
        self.lab_ivName.setText(self.base_info["vname"])
        self.base_info["curname"] = self.current_path[-1]
        self.lab_curchoose.setText(self.base_info["curname"])
        # 树形图刷新
        self.tw_nodelist.clear()
        self.renew_treelist(self.treelist_dict, self.tw_nodelist)
        self.tw_nodelist.expandAll()
        # 刷新选择视图
        self.renew_chooselist()
        # 显示当前节点
        self.show_current_node()
        # 递归整理节点图输出字典
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
        # print('位置指引' ,self.current_path)

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

    # 字典递归编辑
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
                QMessageBox.critical(self, '对象错误', '请关闭并重新载入本窗口！')
                return -1
            img_cache = False
            if self.cb_showimage.isChecked():
                img_cache = True
            if not self.iv_init.change_method(1, node_id=node_id, img_cache=img_cache):
                return -1
            self.iv_init.start()
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
        _cur = self.current_path[-1]
        self.feedback_dict['baseInfo'] = self.base_info
        self.feedback_dict['indic'] = {}
        self.feedback_dict['indic'][_cur] = self.get_current_list(self.current_path, 1)
        self.feedback_dict['indic'][_cur]['isChoose'] = True
        self.feedback_dict['indic'][_cur].pop('choices')
        self.close()


    # 下载已选择节点
    def dl_all_chooses(self):
        self.feedback_dict['baseInfo'] = self.base_info
        self.feedback_dict['indic'] = self.treelist_dict
        self.close()


    # 开始递归探查
    def st_recursion(self):
        if not self.iv_init:
            QMessageBox.critical(self, '对象错误', '请关闭并重新载入本窗口！')
            return -1
        if self.spinBox.value() == 0:
            return 0
        if self.spinBox.value() < 0:
            recur_warning = QMessageBox.warning(self, '递归警告',
                '当递归深度小于0时将探查直至所有节点结束！\n'
                '1. 若该互动视频存在无限循环节点则会导致溢出；\n'
                '2. 当互动视频节点分支较大时您将会等待很长时间。\n'
                '请谨慎使用无限递归功能！继续请点击确认。', QMessageBox.Yes | QMessageBox.Cancel)
            if recur_warning == QMessageBox.Cancel:
                print('已经取消递归')
                return -1
        # 开始递归操作
        deep = self.spinBox.value()
        nodeID = ''
        mode = 1
        if self.cb_RSaCC.isChecked():
            mode = 2
            nodeID = self.lab_curNID.text()
        self.RTWindow = RecurThreadWindow(mode , self.iv_init, nodeID, deep)
        self.RTWindow._RSignal.connect(self.Recur_Slot_Handle)
        self.RTWindow.show()


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
        elif indict['code'] == -1:
            self.lab_curStatus.setText(indict['data'])
        else:
            pass


    # 递归线程接收槽函数
    def Recur_Slot_Handle(self, indic):
        if indic:
            if indic['status'] == 1:
                self.treelist_dict[self.base_info["vname"]]['choices'] = indic['data']
            elif indic['status'] == 2:
                tmp = self.current_path.copy()
                self.treelist_dict = self.recursion_dict_update(self.treelist_dict, tmp, 'choices', indic['data'])
            self.renew_show()


if __name__ == '__main__':
    args = {
        'Address':'https://www.bilibili.com/video/BV1Kb4y1v79e',
        'useProxy':False,
        'Proxy':{},
        'useCookie':False,
        'cookie':'',
        'Output': 'G:/Cache',
    }
    app = QApplication(sys.argv)
    InteractiveWindow = biliInteractMainWindow(args)
    InteractiveWindow.show()
    sys.exit(app.exec_())
