# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'biliInteractive_new.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from UI import images_dl_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1083, 728)
        icon = QIcon()
        icon.addFile(u":/Icon/images/bilidownloader.ico", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(u"*{\n"
"	font: 14px \"Microsoft YaHei\";\n"
"	color:rgb(0, 0, 0);\n"
"}\n"
"/* \u4e3b\u4f53\u989c\u8272\n"
".QWidget#centralwidget{\n"
"	background-color: rgb(156, 156, 156);\n"
"	border-radius:20px;\n"
"} */\n"
"QLabel{\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"\n"
".QWidget#mainwidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"	border-radius:20px;\n"
"}\n"
"\n"
"/* \u7f16\u8f91\u6846\u6837\u5f0f */\n"
"QLineEdit{\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 255, 255);\n"
"	border-radius: 15px;\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"}\n"
"QLineEdit:hover{\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 238, 238);\n"
"}\n"
"\n"
"/* \u6309\u94ae\u6837\u5f0f */\n"
"QPushButton[flat=\"false\"]{\n"
"	background-color: rgb(255, 153, 153);\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 15px;\n"
"	font: 15px \"Microsoft YaHei\";\n"
"}\n"
"QPushButton:hover{\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop"
                        ":0 rgba(255, 153, 153, 255), stop:1 rgba(255, 136, 136, 255));\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(190, 115, 115, 255), stop:1 rgba(255, 153, 153, 255));\n"
"}\n"
"QPushButton#btnclose{\n"
"	background-color: rgb(255, 102, 102);\n"
"	border-radius:8px;\n"
"}\n"
"QPushButton#btnclose:pressed{\n"
"	background-color: rgb(200, 80, 80);\n"
"}\n"
"QPushButton#btnmax{\n"
"	background-color: rgb(255, 255, 102);\n"
"	border-radius:8px;\n"
"}\n"
"QPushButton#btnmax:pressed{\n"
"	background-color: rgb(195, 195, 78);\n"
"}\n"
"QPushButton#btnmin{\n"
"	background-color: rgb(153, 204, 102);\n"
"	border-radius:8px;\n"
"}\n"
"QPushButton#btnmin:pressed{\n"
"	background-color: rgb(126, 168, 83);\n"
"}\n"
"\n"
"/* \u8fdb\u5ea6\u6761\u6837\u5f0f */\n"
"QProgressBar{\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	height: 10px;\n"
"	background-color: rgb(255, 255, 255);\n"
"	font: 16px \"Microsoft YaHei\";\n"
"	border-radius:6px;\n"
"	color: rgb(0, "
                        "0, 0);\n"
"}\n"
"QProgressBar::chunk{\n"
"	background-color: rgb(255, 204, 153);\n"
"	border-radius:6px;\n"
"}\n"
"\n"
"/* \u9009\u62e9\u8868\u6837\u5f0f */\n"
"QListWidget{\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	border-radius:15px;\n"
"	padding: 5px;\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"QListWidget::item{\n"
"	border: 1px dashed rgb(255, 204, 153);\n"
"	border-radius: 5px;\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"QListWidget::item:hover{\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 204, 153);\n"
"}\n"
"QListWidget::item:focus{\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"/* \u9009\u62e9\u6846\u6837\u5f0f */\n"
"QComboBox{\n"
"	border-radius: 15px;\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"QComboBox:hover{\n"
"	color: rgb(0, 0, 0);\n"
"	background: rgb(255, 238, 238)\n"
"}\n"
"QComboBox QAbstractItemView{\n"
"	bo"
                        "rder: 2px solid rgb(255, 153, 153);\n"
"	selection-background-color: rgb(255, 204, 153)\n"
"}\n"
"QComboBox::drop-down {\n"
"     subcontrol-origin: padding;\n"
"     subcontrol- position :  top  left;\n"
"     width :  28px ;\n"
"     border: none;\n"
"}\n"
"QComboBox::down-arrow{\n"
"	image: url(:/combo/images/dd.png);\n"
"}\n"
"QComboBox::down-arrow:hover{\n"
"	image: url(:/combo/images/dd1.png);\n"
"}\n"
"QComboBox::down-arrow:pressed{\n"
"	image: url(:/combo/images/dd2.png);\n"
"}\n"
"\n"
"/* \u6587\u672c\u6846\u6837\u5f0f */\n"
"QPlainTextEdit{\n"
"	border-radius: 15px;\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	padding: 5px;\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* Title Frame\u6837\u5f0f */\n"
"QFrame#title{\n"
"	background-image: url(:/title/images/title.png);\n"
"	border: none;\n"
"}\n"
"\n"
"/* \u5206\u7ec4\u6846\u6837\u5f0f */\n"
"QGroupBox{\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	border-radius: 15px;\n"
"	margin-top: 2ex;\n"
"}\n"
"QGroupB"
                        "ox::title{\n"
"	subcontrol-origin: margin;\n"
"	subcontrol-position: top center;\n"
"	padding: 0 3px;\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"/* \u7ec4\u5408\u6846\u6837\u5f0f */\n"
"QCheckBox{\n"
"	color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"\n"
"/* \u6811\u5f62\u6846\u6837\u5f0f */\n"
"QTreeWidget{\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 255, 255);\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	border-radius: 15px;\n"
"	padding: 5px;\n"
"}\n"
"QTreeWidget::item{\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 255, 255);\n"
"	border: 1px dashed rgb(255, 204, 153);\n"
"	border-radius: 5px;\n"
"}\n"
"QTreeWidget::item:hover{\n"
"	color: rgb(0, 0, 0);\n"
"	background-color: rgb(255, 204, 153);\n"
"}\n"
"")
        self.mainwidget = QWidget(Form)
        self.mainwidget.setObjectName(u"mainwidget")
        self.mainwidget.setGeometry(QRect(30, 30, 1011, 661))
        self.mainwidget.setAutoFillBackground(False)
        self.mainwidget.setStyleSheet(u"")
        self.tw_nodelist = QTreeWidget(self.mainwidget)
        self.tw_nodelist.setObjectName(u"tw_nodelist")
        self.tw_nodelist.setGeometry(QRect(750, 260, 231, 371))
        self.tw_nodelist.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tw_nodelist.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.btnmax = QPushButton(self.mainwidget)
        self.btnmax.setObjectName(u"btnmax")
        self.btnmax.setGeometry(QRect(940, 20, 16, 16))
        self.btnmax.setFlat(True)
        self.btnmin = QPushButton(self.mainwidget)
        self.btnmin.setObjectName(u"btnmin")
        self.btnmin.setGeometry(QRect(910, 20, 16, 16))
        self.btnmin.setFlat(True)
        self.btnclose = QPushButton(self.mainwidget)
        self.btnclose.setObjectName(u"btnclose")
        self.btnclose.setGeometry(QRect(970, 20, 16, 16))
        self.btnclose.setFlat(True)
        self.label_10 = QLabel(self.mainwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(30, 10, 141, 41))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"*{\n"
"	font: 18px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"}\n"
"")
        self.groupBox_7 = QGroupBox(self.mainwidget)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(750, 50, 231, 201))
        self.lineEdit_height = QLineEdit(self.groupBox_7)
        self.lineEdit_height.setObjectName(u"lineEdit_height")
        self.lineEdit_height.setGeometry(QRect(60, 70, 61, 31))
        self.lineEdit_height.setAlignment(Qt.AlignCenter)
        self.lineEdit_width = QLineEdit(self.groupBox_7)
        self.lineEdit_width.setObjectName(u"lineEdit_width")
        self.lineEdit_width.setGeometry(QRect(60, 30, 61, 31))
        self.lineEdit_width.setInputMethodHints(Qt.ImhNone)
        self.lineEdit_width.setAlignment(Qt.AlignCenter)
        self.label_11 = QLabel(self.groupBox_7)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 70, 31, 31))
        font1 = QFont()
        font1.setFamily(u"Microsoft YaHei")
        font1.setBold(False)
        font1.setItalic(False)
        font1.setWeight(50)
        self.label_11.setFont(font1)
        self.btn_adjsize = QPushButton(self.groupBox_7)
        self.btn_adjsize.setObjectName(u"btn_adjsize")
        self.btn_adjsize.setGeometry(QRect(130, 70, 91, 31))
        self.label_12 = QLabel(self.groupBox_7)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(20, 30, 31, 31))
        self.label_12.setFont(font1)
        self.btn_nodeview = QPushButton(self.groupBox_7)
        self.btn_nodeview.setObjectName(u"btn_nodeview")
        self.btn_nodeview.setGeometry(QRect(130, 30, 91, 31))
        self.btn_exportJSON = QPushButton(self.groupBox_7)
        self.btn_exportJSON.setObjectName(u"btn_exportJSON")
        self.btn_exportJSON.setGeometry(QRect(10, 150, 211, 31))
        self.btn_save2html = QPushButton(self.groupBox_7)
        self.btn_save2html.setObjectName(u"btn_save2html")
        self.btn_save2html.setGeometry(QRect(10, 110, 211, 31))
        self.groupBox = QGroupBox(self.mainwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 50, 711, 581))
        self.list_NodeChoose = QListWidget(self.groupBox)
        QListWidgetItem(self.list_NodeChoose)
        QListWidgetItem(self.list_NodeChoose)
        self.list_NodeChoose.setObjectName(u"list_NodeChoose")
        self.list_NodeChoose.setGeometry(QRect(0, 60, 711, 351))
        self.list_NodeChoose.setAutoFillBackground(False)
        self.list_NodeChoose.setDragEnabled(False)
        self.list_NodeChoose.setFlow(QListView.LeftToRight)
        self.list_NodeChoose.setResizeMode(QListView.Fixed)
        self.list_NodeChoose.setLayoutMode(QListView.SinglePass)
        self.list_NodeChoose.setSpacing(20)
        self.list_NodeChoose.setViewMode(QListView.IconMode)
        self.list_NodeChoose.setModelColumn(0)
        self.list_NodeChoose.setUniformItemSizes(False)
        self.list_NodeChoose.setWordWrap(False)
        self.btn_canceldownload = QPushButton(self.groupBox)
        self.btn_canceldownload.setObjectName(u"btn_canceldownload")
        self.btn_canceldownload.setGeometry(QRect(560, 460, 141, 31))
        self.btn_downALLChoose = QPushButton(self.groupBox)
        self.btn_downALLChoose.setObjectName(u"btn_downALLChoose")
        self.btn_downALLChoose.setGeometry(QRect(560, 540, 141, 31))
        self.btn_back = QPushButton(self.groupBox)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(10, 420, 141, 31))
        self.btn_next = QPushButton(self.groupBox)
        self.btn_next.setObjectName(u"btn_next")
        self.btn_next.setGeometry(QRect(560, 420, 141, 31))
        self.le_nodeway = QLineEdit(self.groupBox)
        self.le_nodeway.setObjectName(u"le_nodeway")
        self.le_nodeway.setGeometry(QRect(160, 420, 391, 31))
        self.le_nodeway.setAlignment(Qt.AlignCenter)
        self.le_nodeway.setReadOnly(True)
        self.btn_downCurChoose = QPushButton(self.groupBox)
        self.btn_downCurChoose.setObjectName(u"btn_downCurChoose")
        self.btn_downCurChoose.setGeometry(QRect(560, 500, 141, 31))
        self.formLayoutWidget = QWidget(self.groupBox)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 460, 351, 111))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lab_ivName = QLabel(self.formLayoutWidget)
        self.lab_ivName.setObjectName(u"lab_ivName")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lab_ivName)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.lab_curchoose = QLabel(self.formLayoutWidget)
        self.lab_curchoose.setObjectName(u"lab_curchoose")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lab_curchoose)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.lab_curCID = QLabel(self.formLayoutWidget)
        self.lab_curCID.setObjectName(u"lab_curCID")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lab_curCID)

        self.label_7 = QLabel(self.formLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.lab_curStatus = QLabel(self.formLayoutWidget)
        self.lab_curStatus.setObjectName(u"lab_curStatus")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lab_curStatus)

        self.spinBox = QSpinBox(self.groupBox)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(450, 470, 81, 31))
        self.spinBox.setMinimum(-10)
        self.spinBox.setValue(-1)
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(380, 470, 72, 31))
        self.cb_RSaCC = QCheckBox(self.groupBox)
        self.cb_RSaCC.setObjectName(u"cb_RSaCC")
        self.cb_RSaCC.setGeometry(QRect(380, 510, 151, 19))
        self.cb_RSaCC.setCheckable(True)
        self.cb_RSaCC.setChecked(False)
        self.cb_RSaCC.setTristate(False)
        self.btn_stRecu = QPushButton(self.groupBox)
        self.btn_stRecu.setObjectName(u"btn_stRecu")
        self.btn_stRecu.setGeometry(QRect(380, 540, 151, 31))
        self.cb_showimage = QCheckBox(self.groupBox)
        self.cb_showimage.setObjectName(u"cb_showimage")
        self.cb_showimage.setGeometry(QRect(590, 20, 101, 31))
        self.cb_showimage.setChecked(True)
        self.btn_refreash = QPushButton(self.groupBox)
        self.btn_refreash.setObjectName(u"btn_refreash")
        self.btn_refreash.setGeometry(QRect(470, 20, 93, 31))

        self.retranslateUi(Form)
        self.btnclose.clicked.connect(Form.close)
        self.btn_canceldownload.clicked.connect(Form.close)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u4e92\u52a8\u89c6\u9891\u4e0b\u8f7d", None))
        ___qtreewidgetitem = self.tw_nodelist.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"CID", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"\u8282\u70b9", None));
        self.btnmax.setText("")
        self.btnmin.setText("")
        self.btnclose.setText("")
        self.label_10.setText(QCoreApplication.translate("Form", u"\u4e92\u52a8\u89c6\u9891\u4e0b\u8f7d", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Form", u"\u8282\u70b9\u56fe", None))
        self.lineEdit_height.setText(QCoreApplication.translate("Form", u"420", None))
        self.lineEdit_width.setText(QCoreApplication.translate("Form", u"670", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u9ad8\u5ea6", None))
        self.btn_adjsize.setText(QCoreApplication.translate("Form", u"\u8c03\u6574\u8282\u70b9\u56fe", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u5bbd\u5ea6", None))
        self.btn_nodeview.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u8282\u70b9\u56fe", None))
        self.btn_exportJSON.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa\u8282\u70b9JSON", None))
        self.btn_save2html.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u4e3a\u7f51\u9875", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u624b\u52a8\u8282\u70b9\u9009\u62e9\u89c6\u56fe", None))

        __sortingEnabled = self.list_NodeChoose.isSortingEnabled()
        self.list_NodeChoose.setSortingEnabled(False)
        ___qlistwidgetitem = self.list_NodeChoose.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"ssss", None));
        ___qlistwidgetitem1 = self.list_NodeChoose.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Form", u"gggg", None));
        self.list_NodeChoose.setSortingEnabled(__sortingEnabled)

        self.btn_canceldownload.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88\u4e0b\u8f7d", None))
        self.btn_downALLChoose.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d\u5df2\u9009\u62e9\u8282\u70b9", None))
        self.btn_back.setText(QCoreApplication.translate("Form", u"\u4e0a\u4e00\u4e2a\u8282\u70b9", None))
        self.btn_next.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u4e2a\u8282\u70b9", None))
        self.le_nodeway.setPlaceholderText(QCoreApplication.translate("Form", u"\u6b64\u5904\u663e\u793a\u8282\u70b9\u8def\u5f84", None))
        self.btn_downCurChoose.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d\u5f53\u524d\u8282\u70b9", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u4e92\u52a8\u89c6\u9891\u540d\u79f0\uff1a", None))
        self.lab_ivName.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u6240\u5728\u9009\u9879\uff1a", None))
        self.lab_curchoose.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u89c6\u9891CID\uff1a", None))
        self.lab_curCID.setText(QCoreApplication.translate("Form", u"None", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u72b6\u6001\uff1a", None))
        self.lab_curStatus.setText(QCoreApplication.translate("Form", u"\u6b63\u5728\u52a0\u8f7d\u2026\u2026", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u9012\u5f52\u6df1\u5ea6", None))
        self.cb_RSaCC.setText(QCoreApplication.translate("Form", u"\u4ece\u5f53\u524d\u8282\u70b9\u5f00\u59cb\u9012\u5f52", None))
        self.btn_stRecu.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u9012\u5f52", None))
        self.cb_showimage.setText(QCoreApplication.translate("Form", u"\u663e\u793a\u7f29\u7565\u56fe", None))
        self.btn_refreash.setText(QCoreApplication.translate("Form", u"\u5237\u65b0\u663e\u793a", None))
    # retranslateUi

