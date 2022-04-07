# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'biliInteractive_NoUse.ui'
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
        Form.resize(703, 613)
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
        self.mainwidget.setGeometry(QRect(30, 30, 631, 551))
        self.mainwidget.setAutoFillBackground(False)
        self.mainwidget.setStyleSheet(u"")
        self.treeWidget_4 = QTreeWidget(self.mainwidget)
        self.treeWidget_4.setObjectName(u"treeWidget_4")
        self.treeWidget_4.setGeometry(QRect(30, 60, 571, 331))
        self.treeWidget_4.setSelectionMode(QAbstractItemView.SingleSelection)
        self.treeWidget_4.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.btnmax = QPushButton(self.mainwidget)
        self.btnmax.setObjectName(u"btnmax")
        self.btnmax.setGeometry(QRect(560, 20, 16, 16))
        self.btnmax.setFlat(True)
        self.btnmin = QPushButton(self.mainwidget)
        self.btnmin.setObjectName(u"btnmin")
        self.btnmin.setGeometry(QRect(530, 20, 16, 16))
        self.btnmin.setFlat(True)
        self.btnclose = QPushButton(self.mainwidget)
        self.btnclose.setObjectName(u"btnclose")
        self.btnclose.setGeometry(QRect(590, 20, 16, 16))
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
        self.btn_canceldownload = QPushButton(self.mainwidget)
        self.btn_canceldownload.setObjectName(u"btn_canceldownload")
        self.btn_canceldownload.setGeometry(QRect(30, 490, 181, 31))
        self.btn_startdownload = QPushButton(self.mainwidget)
        self.btn_startdownload.setObjectName(u"btn_startdownload")
        self.btn_startdownload.setGeometry(QRect(30, 410, 181, 31))
        self.btn_exportJSON = QPushButton(self.mainwidget)
        self.btn_exportJSON.setObjectName(u"btn_exportJSON")
        self.btn_exportJSON.setGeometry(QRect(30, 450, 181, 31))
        self.groupBox_7 = QGroupBox(self.mainwidget)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setGeometry(QRect(230, 400, 371, 121))
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
        self.btn_adjsize.setGeometry(QRect(150, 30, 91, 31))
        self.label_12 = QLabel(self.groupBox_7)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(20, 30, 31, 31))
        self.label_12.setFont(font1)
        self.btn_save2html = QPushButton(self.groupBox_7)
        self.btn_save2html.setObjectName(u"btn_save2html")
        self.btn_save2html.setGeometry(QRect(150, 70, 201, 31))
        self.btn_nodeview = QPushButton(self.groupBox_7)
        self.btn_nodeview.setObjectName(u"btn_nodeview")
        self.btn_nodeview.setGeometry(QRect(260, 30, 91, 31))

        self.retranslateUi(Form)
        self.btnclose.clicked.connect(Form.close)
        self.btn_canceldownload.clicked.connect(Form.close)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u4e92\u52a8\u89c6\u9891\u4e0b\u8f7d", None))
        ___qtreewidgetitem = self.treeWidget_4.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"CID", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"\u8282\u70b9", None));
        self.btnmax.setText("")
        self.btnmin.setText("")
        self.btnclose.setText("")
        self.label_10.setText(QCoreApplication.translate("Form", u"\u4e92\u52a8\u89c6\u9891\u4e0b\u8f7d", None))
        self.btn_canceldownload.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88\u4e0b\u8f7d", None))
        self.btn_startdownload.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u4e0b\u8f7d", None))
        self.btn_exportJSON.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa\u8282\u70b9JSON", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Form", u"\u8282\u70b9\u56fe", None))
        self.lineEdit_height.setText(QCoreApplication.translate("Form", u"420", None))
        self.lineEdit_width.setText(QCoreApplication.translate("Form", u"670", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u9ad8\u5ea6", None))
        self.btn_adjsize.setText(QCoreApplication.translate("Form", u"\u8c03\u6574\u8282\u70b9\u56fe", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u5bbd\u5ea6", None))
        self.btn_save2html.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u4e3a\u7f51\u9875", None))
        self.btn_nodeview.setText(QCoreApplication.translate("Form", u"\u67e5\u770b\u8282\u70b9\u56fe", None))
    # retranslateUi

