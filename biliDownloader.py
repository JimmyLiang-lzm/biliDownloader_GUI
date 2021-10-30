# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'biliDownloader.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import images_dl_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(924, 676)
        icon = QIcon()
        icon.addFile(u":/Icon/images/bilidownloader.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"*{\n"
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
"QLineEdit:focus{\n"
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
"	background-color: qlineargradient(spread:p"
                        "ad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(190, 115, 115, 255), stop:1 rgba(255, 153, 153, 255));\n"
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
"/* \u9009\u62e9\u8868"
                        "\u6837\u5f0f */\n"
"QListWidget{\n"
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
"	image: u"
                        "rl(:/combo/images/dd1.png);\n"
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
"	border: none;\n"
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
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainwidget = QWidget(self.centralwidget)
        self.mainwidget.setObjectName(u"mainwidget")
        self.mainwidget.setGeometry(QRect(20, 20, 881, 631))
        self.source_search = QLineEdit(self.mainwidget)
        self.source_search.setObjectName(u"source_search")
        self.source_search.setGeometry(QRect(40, 100, 691, 31))
        self.progressBar = QProgressBar(self.mainwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(40, 580, 801, 31))
        self.progressBar.setMaximum(1000000)
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(Qt.Horizontal)
        self.btn_search = QPushButton(self.mainwidget)
        self.btn_search.setObjectName(u"btn_search")
        self.btn_search.setEnabled(True)
        self.btn_search.setGeometry(QRect(700, 100, 141, 31))
        self.btnclose = QPushButton(self.mainwidget)
        self.btnclose.setObjectName(u"btnclose")
        self.btnclose.setGeometry(QRect(840, 20, 16, 16))
        self.btnclose.setFlat(True)
        self.btnmax = QPushButton(self.mainwidget)
        self.btnmax.setObjectName(u"btnmax")
        self.btnmax.setGeometry(QRect(810, 20, 16, 16))
        self.btnmax.setFlat(True)
        self.btnmin = QPushButton(self.mainwidget)
        self.btnmin.setObjectName(u"btnmin")
        self.btnmin.setGeometry(QRect(780, 20, 16, 16))
        self.btnmin.setFlat(True)
        self.plainTextEdit = QPlainTextEdit(self.mainwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(40, 380, 801, 191))
        self.plainTextEdit.setReadOnly(True)
        self.groupBox = QGroupBox(self.mainwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setEnabled(True)
        self.groupBox.setGeometry(QRect(40, 140, 801, 231))
        self.btn_download = QPushButton(self.groupBox)
        self.btn_download.setObjectName(u"btn_download")
        self.btn_download.setGeometry(QRect(20, 180, 131, 31))
        self.checkBox_sym = QCheckBox(self.groupBox)
        self.checkBox_sym.setObjectName(u"checkBox_sym")
        self.checkBox_sym.setGeometry(QRect(300, 30, 131, 31))
        self.combo_vq = QComboBox(self.groupBox)
        self.combo_vq.setObjectName(u"combo_vq")
        self.combo_vq.setGeometry(QRect(110, 30, 151, 31))
        self.combo_aq = QComboBox(self.groupBox)
        self.combo_aq.setObjectName(u"combo_aq")
        self.combo_aq.setGeometry(QRect(110, 80, 151, 31))
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 30, 51, 31))
        self.media_list = QListWidget(self.groupBox)
        self.media_list.setObjectName(u"media_list")
        self.media_list.setGeometry(QRect(460, 61, 321, 151))
        self.media_list.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.media_list.setTabKeyNavigation(False)
        self.media_list.setDragEnabled(False)
        self.media_list.setMovement(QListView.Static)
        self.media_list.setViewMode(QListView.ListMode)
        self.media_list.setSelectionRectVisible(False)
        self.media_list.setSortingEnabled(False)
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 80, 81, 31))
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(470, 20, 111, 31))
        self.lineEdit_dir = QLineEdit(self.groupBox)
        self.lineEdit_dir.setObjectName(u"lineEdit_dir")
        self.lineEdit_dir.setGeometry(QRect(110, 130, 281, 31))
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 130, 81, 31))
        self.btn_dir = QPushButton(self.groupBox)
        self.btn_dir.setObjectName(u"btn_dir")
        self.btn_dir.setGeometry(QRect(360, 130, 71, 31))
        self.btn_pause = QPushButton(self.groupBox)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setGeometry(QRect(160, 180, 131, 31))
        self.btn_stop = QPushButton(self.groupBox)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(300, 180, 131, 31))
        self.btn_selectALL = QPushButton(self.groupBox)
        self.btn_selectALL.setObjectName(u"btn_selectALL")
        self.btn_selectALL.setGeometry(QRect(710, 20, 71, 31))
        self.checkBox_usecookie = QCheckBox(self.groupBox)
        self.checkBox_usecookie.setObjectName(u"checkBox_usecookie")
        self.checkBox_usecookie.setGeometry(QRect(300, 60, 141, 31))
        self.btn_changeconfig = QPushButton(self.groupBox)
        self.btn_changeconfig.setObjectName(u"btn_changeconfig")
        self.btn_changeconfig.setGeometry(QRect(300, 90, 131, 31))
        self.title = QFrame(self.mainwidget)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(40, 20, 371, 61))
        self.title.setFrameShape(QFrame.StyledPanel)
        self.title.setFrameShadow(QFrame.Raised)
        self.btn_about = QPushButton(self.mainwidget)
        self.btn_about.setObjectName(u"btn_about")
        self.btn_about.setGeometry(QRect(700, 60, 61, 31))
        self.btn_help = QPushButton(self.mainwidget)
        self.btn_help.setObjectName(u"btn_help")
        self.btn_help.setGeometry(QRect(780, 60, 61, 31))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.btnclose.clicked.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bili Downloader", None))
        self.source_search.setText("")
        self.source_search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8bf7\u586b\u5165\u89c6\u9891\u9875\u9762HTTP/HTTPS\u5730\u5740", None))
        self.progressBar.setFormat(QCoreApplication.translate("MainWindow", u"biliDownloader\u5c31\u7eea", None))
        self.btn_search.setText(QCoreApplication.translate("MainWindow", u"\u8d44\u6e90\u63a2\u67e5", None))
        self.btnclose.setText("")
        self.btnmax.setText("")
        self.btnmin.setText("")
        self.plainTextEdit.setPlainText(QCoreApplication.translate("MainWindow", u"\u6b22\u8fce\u4f7f\u7528Bili Downloader V1.2.20211005\n"
"Release at 2021/10/06 ......", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c\u6846", None))
        self.btn_download.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u8d44\u6e90", None))
        self.checkBox_sym.setText(QCoreApplication.translate("MainWindow", u"FFMPEG\u5408\u6210", None))
        self.combo_vq.setCurrentText("")
        self.combo_aq.setCurrentText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u6670\u5ea6", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u9891\u6e05\u6670\u5ea6", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5a92\u4f53\u4e0b\u8f7d\u9009\u62e9", None))
        self.lineEdit_dir.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u76ee\u5f55", None))
        self.btn_dir.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8", None))
        self.btn_pause.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c\u4e0b\u8f7d", None))
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u4e0b\u8f7d", None))
        self.btn_selectALL.setText(QCoreApplication.translate("MainWindow", u"\u5168\u9009", None))
        self.checkBox_usecookie.setText(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528VIP Cookie", None))
        self.btn_changeconfig.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u7ea7\u8bbe\u7f6e", None))
        self.btn_about.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.btn_help.setText(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

