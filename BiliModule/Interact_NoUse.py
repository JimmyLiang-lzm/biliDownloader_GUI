import json, webbrowser
from etc import *
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect, QFileDialog, QTreeWidgetItem
from PySide2.QtCore import Qt, QPoint, Signal
from PySide2.QtGui import QIntValidator
from pyecharts import options as opts
from pyecharts.charts import Tree
from UI.biliInteractive_NoUse import Ui_Form


############################################################################################
# 交互视频下载窗口类
class InteractWindow(QWidget, Ui_Form):
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
        self.m_Position = QPoint(0, 0)
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
        self.info_Init(full_iv, self.treeWidget_4)
        self.treeWidget_4.expandToDepth(2)
        self.draw_chart("670", "420", self.chartdict)

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

    # 定义关闭事件
    def closeEvent(self, QCloseEvent):
        # print(self.feedback_dict)
        self._Signal.emit(self.feedback_dict)

    # ######################### BS PART #############################
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
    def download_list_make(self, tree_widget_obj):
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
        directory = QFileDialog.getSaveFileName(None, "选择JSON保存路径", init_path, 'JSON(*.json)')
        if directory[0] != '':
            with open(directory[0], 'w') as f:
                f.write(json.dumps(self.full_json, ensure_ascii=False))

    # Save node picture to HTML
    def save2html(self):
        init_path = indict["Output"] + "/" + self.ivideo_name + ".html"
        directory = QFileDialog.getSaveFileName(None, '选择节点图保存路径', init_path, 'HTML(*.html)')
        if directory[0] != '':
            self.node_chart.set_global_opts(title_opts=opts.TitleOpts(
                title=self.ivideo_name,
                subtitle="Made By BiliDownloader")) \
                .render(directory[0])

    # Re-size node picture.
    def re_show(self):
        w = self.lineEdit_width.text()
        h = self.lineEdit_height.text()
        self.draw_chart(w, h, self.chartdict)

    # File name conflict replace
    def name_replace(self, name):
        vn = name.replace(' ', '_').replace('\\', '').replace('/', '')
        vn = vn.replace('*', '').replace(':', '').replace('?', '').replace('<', '')
        vn = vn.replace('>', '').replace('\"', '').replace('|', '').replace('\x08', '')
        return vn

    # 显示节点图
    def show_chart(self):
        dir_address = self.html_Path.replace("\\", "/") + "/temp"
        if not os.path.exists(dir_address):
            os.makedirs(dir_address)
        self.node_chart.render(dir_address + "/node_temp.html")
        access_url = self.url_maker(dir_address + "/node_temp.html")
        webbrowser.open(access_url)

    # 跨系统平台节点文件路径生成函数
    def url_maker(self, in_dir):
        if indict["sys"] == "win32":
            return "file:///" + in_dir
        else:
            return "file://" + in_dir

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

    # 初始数据字典转化为树形图递归函数
    def info_Init(self, in_dict, root):
        for ch in in_dict:
            item = QTreeWidgetItem(root)
            item.setText(0, ch)
            item.setCheckState(0, Qt.Checked)
            item.setText(1, in_dict[ch]["cid"])
            item.addChild(self.info_Init(in_dict[ch]["choices"], item))

    # 初始数据字典转化图像专用JSON递归函数
    def recursion_for_chart(self, in_json):
        temp = []
        for ch in in_json:
            stemp = {
                "name": ch,
                "children": self.recursion_for_chart(in_json[ch]["choices"])
            }
            temp.append(stemp)
        return temp

    # 自动选择
    def onTreeClicked(self, item, num):
        # 如果是顶部节点，只考虑Child：
        if item.childCount() and not item.parent():  # 判断是顶部节点，也就是根节点
            if item.checkState(0) == Qt.Unchecked:  # 规定点击根节点只有两态切换，没有中间态
                for i in range(item.childCount()):  # 遍历子节点进行状态切换
                    item.child(i).setCheckState(0, Qt.Unchecked)
            elif item.checkState(0) == Qt.Checked:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(0, Qt.Checked)

        # 如果是底部节点，只考虑Parent
        if item.parent() and not item.childCount():
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

        # 中间层需要全面考虑
        if item.parent() and item.childCount():
            if item.checkState(0) == Qt.Unchecked:  # 规定点击根节点只有两态切换，没有中间态
                for i in range(item.childCount()):  # 遍历子节点进行状态切换
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
