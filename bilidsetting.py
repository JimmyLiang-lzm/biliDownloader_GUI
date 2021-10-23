# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bilidsetting.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import images_dl_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(518, 288)
        icon = QIcon()
        icon.addFile(u":/Icon/images/bilidownloader.ico", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(u"*{\n"
"	font: 14px \"Microsoft YaHei\";\n"
"}\n"
"/* \u4e3b\u4f53\u989c\u8272\n"
".QWidget#centralwidget{\n"
"	background-color: rgb(156, 156, 156);\n"
"	border-radius:20px;\n"
"} */\n"
".QWidget#mainwidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"	border-radius:20px;\n"
"}\n"
"\n"
"/* \u7f16\u8f91\u6846\u6837\u5f0f */\n"
"QLineEdit{\n"
"	border-radius: 15px;\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	padding-left: 5px;\n"
"	padding-right: 27px;\n"
"}\n"
"QLineEdit:hover{\n"
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
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 153, 153, 255), stop:1 rgba(255, 136, 136, 255));\n"
"}\n"
"QPushButton:pressed{\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,"
                        " stop:0 rgba(190, 115, 115, 255), stop:1 rgba(255, 153, 153, 255));\n"
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
"	color: rgb(0, 0, 0);\n"
"}\n"
"QProgressBar::chunk{\n"
"	background-color: rgb(255, 204, 153);\n"
"	border-radius:6px;\n"
"}\n"
"\n"
"/* \u9009\u62e9\u8868\u6837\u5f0f */\n"
"QListWi"
                        "dget{\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	border-radius:15px;\n"
"	padding: 5px;\n"
"}\n"
"QListWidget::item{\n"
"	border: 1px dashed rgb(255, 204, 153);\n"
"	border-radius: 5px\n"
"}\n"
"QListWidget::item:hover{\n"
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
"}\n"
"QComboBox:hover{\n"
"	background: rgb(255, 238, 238)\n"
"}\n"
"QComboBox QAbstractItemView{\n"
"	border: 2px solid rgb(255, 153, 153);\n"
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
"	image: url(:/combo/images/dd1.png);"
                        "\n"
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
"}\n"
"\n"
"/* Title Frame\u6837\u5f0f */\n"
"QFrame#title{\n"
"	background-image: url(:/title/images/title.png);\n"
"}\n"
"\n"
"/* \u5206\u7ec4\u6846\u6837\u5f0f */\n"
"QGroupBox{\n"
"	border: 2px solid rgb(255, 153, 153);\n"
"	border-radius: 15px;\n"
"	margin-top: 2ex;\n"
"}\n"
"QGroupBox::title{\n"
"	subcontrol-origin: margin;\n"
"	subcontrol-position: top center;\n"
"	padding: 0 3px;\n"
"}\n"
"\n"
"/* \u7ec4\u5408\u6846\u6837\u5f0f */\n"
"/*QCheckBox{}*/\n"
"QFrame#title{\n"
"	border: none\n"
"}")
        self.mainwidget = QWidget(Form)
        self.mainwidget.setObjectName(u"mainwidget")
        self.mainwidget.setGeometry(QRect(20, 30, 471, 231))
        self.btnmax = QPushButton(self.mainwidget)
        self.btnmax.setObjectName(u"btnmax")
        self.btnmax.setGeometry(QRect(400, 20, 16, 16))
        self.btnmax.setFlat(True)
        self.btnclose = QPushButton(self.mainwidget)
        self.btnclose.setObjectName(u"btnclose")
        self.btnclose.setGeometry(QRect(430, 20, 16, 16))
        self.btnclose.setFlat(True)
        self.btnmin = QPushButton(self.mainwidget)
        self.btnmin.setObjectName(u"btnmin")
        self.btnmin.setGeometry(QRect(370, 20, 16, 16))
        self.btnmin.setFlat(True)
        self.label = QLabel(self.mainwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 10, 111, 41))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet(u"*{\n"
"	font: 18px \"\u5fae\u8f6f\u96c5\u9ed1\";\n"
"}\n"
"")
        self.edit_cookies = QPlainTextEdit(self.mainwidget)
        self.edit_cookies.setObjectName(u"edit_cookies")
        self.edit_cookies.setGeometry(QRect(30, 60, 411, 101))
        self.btn_editcookie = QPushButton(self.mainwidget)
        self.btn_editcookie.setObjectName(u"btn_editcookie")
        self.btn_editcookie.setGeometry(QRect(30, 180, 111, 31))
        self.btn_wherecookie = QPushButton(self.mainwidget)
        self.btn_wherecookie.setObjectName(u"btn_wherecookie")
        self.btn_wherecookie.setGeometry(QRect(180, 180, 111, 31))
        self.btn_cleanplain = QPushButton(self.mainwidget)
        self.btn_cleanplain.setObjectName(u"btn_cleanplain")
        self.btn_cleanplain.setGeometry(QRect(330, 180, 111, 31))

        self.retranslateUi(Form)
        self.btnclose.clicked.connect(Form.close)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u4fee\u6539Cookie", None))
        self.btnmax.setText("")
        self.btnclose.setText("")
        self.btnmin.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"\u4fee\u6539Cookie", None))
        self.edit_cookies.setPlaceholderText(QCoreApplication.translate("Form", u"\u8bf7\u5728\u6b64\u8f93\u5165\u60a8\u5728\u6d4f\u89c8\u5668\u4e2d\u590d\u5236\u7684Cookie", None))
        self.btn_editcookie.setText(QCoreApplication.translate("Form", u"\u4fee\u6539Cookie", None))
        self.btn_wherecookie.setText(QCoreApplication.translate("Form", u"Cookie\u5728\u54ea\uff1f", None))
        self.btn_cleanplain.setText(QCoreApplication.translate("Form", u"\u6e05\u7a7a", None))
    # retranslateUi

