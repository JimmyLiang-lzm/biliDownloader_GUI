# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bilidLive.ui'
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
        Form.resize(878, 760)
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
"QFrame#live{\n"
"	background-image: url(:/title/images/title_live_s.png);\n"
"	border: none;\n"
"}\n"
"\n"
"/* \u5206\u7ec4\u6846\u6837\u5f0f */\n"
"QGroupBox{\n"
"	"
                        "border: 2px solid rgb(255, 153, 153);\n"
"	border-radius: 15px;\n"
"	margin-top: 2ex;\n"
"}\n"
"QGroupBox::title{\n"
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
        self.mainwidget.setGeometry(QRect(30, 30, 811, 701))
        self.btnmax = QPushButton(self.mainwidget)
        self.btnmax.setObjectName(u"btnmax")
        self.btnmax.setGeometry(QRect(740, 20, 16, 16))
        self.btnmax.setFlat(True)
        self.btnclose = QPushButton(self.mainwidget)
        self.btnclose.setObjectName(u"btnclose")
        self.btnclose.setGeometry(QRect(770, 20, 16, 16))
        self.btnclose.setFlat(True)
        self.btnmin = QPushButton(self.mainwidget)
        self.btnmin.setObjectName(u"btnmin")
        self.btnmin.setGeometry(QRect(710, 20, 16, 16))
        self.btnmin.setFlat(True)
        self.live = QFrame(self.mainwidget)
        self.live.setObjectName(u"live")
        self.live.setGeometry(QRect(30, 15, 221, 61))
        self.live.setFrameShape(QFrame.StyledPanel)
        self.live.setFrameShadow(QFrame.Raised)
        self.groupBox = QGroupBox(self.mainwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 130, 511, 151))
        self.btn_record = QPushButton(self.groupBox)
        self.btn_record.setObjectName(u"btn_record")
        self.btn_record.setGeometry(QRect(10, 110, 71, 31))
        self.btn_pause = QPushButton(self.groupBox)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setGeometry(QRect(90, 110, 71, 31))
        self.btn_stop = QPushButton(self.groupBox)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(170, 110, 71, 31))
        self.cb_codec = QComboBox(self.groupBox)
        self.cb_codec.setObjectName(u"cb_codec")
        self.cb_codec.setGeometry(QRect(90, 30, 151, 31))
        self.label_32 = QLabel(self.groupBox)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setGeometry(QRect(20, 30, 72, 31))
        self.cb_vqulity = QComboBox(self.groupBox)
        self.cb_vqulity.setObjectName(u"cb_vqulity")
        self.cb_vqulity.setGeometry(QRect(90, 70, 151, 31))
        self.label_33 = QLabel(self.groupBox)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setGeometry(QRect(20, 70, 72, 31))
        self.sb_autorecord = QCheckBox(self.groupBox)
        self.sb_autorecord.setObjectName(u"sb_autorecord")
        self.sb_autorecord.setGeometry(QRect(280, 70, 181, 31))
        self.btn_setting = QPushButton(self.groupBox)
        self.btn_setting.setObjectName(u"btn_setting")
        self.btn_setting.setGeometry(QRect(260, 110, 111, 31))
        self.btn_vlcaddress = QPushButton(self.groupBox)
        self.btn_vlcaddress.setObjectName(u"btn_vlcaddress")
        self.btn_vlcaddress.setGeometry(QRect(392, 110, 111, 31))
        self.le_savedir = QLineEdit(self.groupBox)
        self.le_savedir.setObjectName(u"le_savedir")
        self.le_savedir.setGeometry(QRect(330, 30, 141, 31))
        self.label_34 = QLabel(self.groupBox)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setGeometry(QRect(260, 30, 72, 31))
        self.btn_selectdir = QPushButton(self.groupBox)
        self.btn_selectdir.setObjectName(u"btn_selectdir")
        self.btn_selectdir.setGeometry(QRect(442, 30, 61, 31))
        self.groupBox_2 = QGroupBox(self.mainwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(550, 80, 231, 341))
        self.btn_inroom = QPushButton(self.groupBox_2)
        self.btn_inroom.setObjectName(u"btn_inroom")
        self.btn_inroom.setGeometry(QRect(10, 300, 101, 31))
        self.btn_upinfo = QPushButton(self.groupBox_2)
        self.btn_upinfo.setObjectName(u"btn_upinfo")
        self.btn_upinfo.setGeometry(QRect(120, 300, 101, 31))
        self.lab_roomimg = QLabel(self.groupBox_2)
        self.lab_roomimg.setObjectName(u"lab_roomimg")
        self.lab_roomimg.setGeometry(QRect(20, 30, 191, 91))
        self.formLayoutWidget = QWidget(self.groupBox_2)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 130, 211, 157))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.lab_roomtitle = QLabel(self.formLayoutWidget)
        self.lab_roomtitle.setObjectName(u"lab_roomtitle")
        self.lab_roomtitle.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lab_roomtitle)

        self.label_6 = QLabel(self.formLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.lab_uid = QLabel(self.formLayoutWidget)
        self.lab_uid.setObjectName(u"lab_uid")
        self.lab_uid.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lab_uid)

        self.label_8 = QLabel(self.formLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_8)

        self.lab_livestatus = QLabel(self.formLayoutWidget)
        self.lab_livestatus.setObjectName(u"lab_livestatus")
        self.lab_livestatus.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lab_livestatus)

        self.label_10 = QLabel(self.formLayoutWidget)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_10)

        self.lab_startime = QLabel(self.formLayoutWidget)
        self.lab_startime.setObjectName(u"lab_startime")
        self.lab_startime.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lab_startime)

        self.label_22 = QLabel(self.formLayoutWidget)
        self.label_22.setObjectName(u"label_22")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_22)

        self.lab_livetag = QLabel(self.formLayoutWidget)
        self.lab_livetag.setObjectName(u"lab_livetag")
        self.lab_livetag.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lab_livetag)

        self.lab_roomid = QLabel(self.formLayoutWidget)
        self.lab_roomid.setObjectName(u"lab_roomid")
        self.lab_roomid.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lab_roomid)

        self.pte_infobox = QPlainTextEdit(self.mainwidget)
        self.pte_infobox.setObjectName(u"pte_infobox")
        self.pte_infobox.setGeometry(QRect(30, 480, 511, 191))
        self.pte_infobox.setUndoRedoEnabled(False)
        self.pte_infobox.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.pte_infobox.setReadOnly(True)
        self.pte_infobox.setOverwriteMode(False)
        self.pte_infobox.setBackgroundVisible(False)
        self.pte_infobox.setCenterOnScroll(False)
        self.groupBox_3 = QGroupBox(self.mainwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(550, 430, 231, 241))
        self.formLayoutWidget_2 = QWidget(self.groupBox_3)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 20, 211, 211))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_27 = QLabel(self.formLayoutWidget_2)
        self.label_27.setObjectName(u"label_27")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_27)

        self.lab_recordstatus = QLabel(self.formLayoutWidget_2)
        self.lab_recordstatus.setObjectName(u"lab_recordstatus")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lab_recordstatus)

        self.label_11 = QLabel(self.formLayoutWidget_2)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_11)

        self.lab_chunk = QLabel(self.formLayoutWidget_2)
        self.lab_chunk.setObjectName(u"lab_chunk")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lab_chunk)

        self.label_14 = QLabel(self.formLayoutWidget_2)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_14)

        self.lab_size = QLabel(self.formLayoutWidget_2)
        self.lab_size.setObjectName(u"lab_size")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.lab_size)

        self.label_16 = QLabel(self.formLayoutWidget_2)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_16)

        self.lab_retime = QLabel(self.formLayoutWidget_2)
        self.lab_retime.setObjectName(u"lab_retime")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.lab_retime)

        self.label_17 = QLabel(self.formLayoutWidget_2)
        self.label_17.setObjectName(u"label_17")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_17)

        self.lab_transpeed = QLabel(self.formLayoutWidget_2)
        self.lab_transpeed.setObjectName(u"lab_transpeed")

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.lab_transpeed)

        self.label_19 = QLabel(self.formLayoutWidget_2)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_19)

        self.lab_cpu = QLabel(self.formLayoutWidget_2)
        self.lab_cpu.setObjectName(u"lab_cpu")

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.lab_cpu)

        self.label_23 = QLabel(self.formLayoutWidget_2)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_23)

        self.lab_ram = QLabel(self.formLayoutWidget_2)
        self.lab_ram.setObjectName(u"lab_ram")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.lab_ram)

        self.label_25 = QLabel(self.formLayoutWidget_2)
        self.label_25.setObjectName(u"label_25")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.label_25)

        self.lab_spaces = QLabel(self.formLayoutWidget_2)
        self.lab_spaces.setObjectName(u"lab_spaces")

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.lab_spaces)

        self.groupBox_4 = QGroupBox(self.mainwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(30, 290, 511, 181))
        self.frame_speed = QFrame(self.groupBox_4)
        self.frame_speed.setObjectName(u"frame_speed")
        self.frame_speed.setGeometry(QRect(10, 50, 161, 121))
        self.frame_speed.setFrameShape(QFrame.StyledPanel)
        self.frame_speed.setFrameShadow(QFrame.Raised)
        self.frame_sys = QFrame(self.groupBox_4)
        self.frame_sys.setObjectName(u"frame_sys")
        self.frame_sys.setGeometry(QRect(175, 50, 161, 121))
        self.frame_sys.setFrameShape(QFrame.StyledPanel)
        self.frame_sys.setFrameShadow(QFrame.Raised)
        self.frame_space = QFrame(self.groupBox_4)
        self.frame_space.setObjectName(u"frame_space")
        self.frame_space.setGeometry(QRect(340, 50, 161, 121))
        self.frame_space.setFrameShape(QFrame.StyledPanel)
        self.frame_space.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 151, 31))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(self.groupBox_4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(175, 20, 161, 31))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_5 = QLabel(self.groupBox_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(350, 20, 151, 31))
        self.label_5.setAlignment(Qt.AlignCenter)
        self.le_address = QLineEdit(self.mainwidget)
        self.le_address.setObjectName(u"le_address")
        self.le_address.setGeometry(QRect(30, 90, 451, 31))
        self.btn_roomenter = QPushButton(self.mainwidget)
        self.btn_roomenter.setObjectName(u"btn_roomenter")
        self.btn_roomenter.setGeometry(QRect(450, 90, 93, 31))

        self.retranslateUi(Form)
        self.btnclose.clicked.connect(Form.close)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btnmax.setText("")
        self.btnclose.setText("")
        self.btnmin.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u5f55\u5236\u64cd\u4f5c", None))
        self.btn_record.setText(QCoreApplication.translate("Form", u"\u5f55\u5236", None))
        self.btn_pause.setText(QCoreApplication.translate("Form", u"\u6682\u505c", None))
        self.btn_stop.setText(QCoreApplication.translate("Form", u"\u505c\u6b62", None))
        self.label_32.setText(QCoreApplication.translate("Form", u"\u7f16\u7801\u9009\u62e9", None))
        self.label_33.setText(QCoreApplication.translate("Form", u"\u6e05\u6670\u5ea6", None))
        self.sb_autorecord.setText(QCoreApplication.translate("Form", u"\u7b49\u5f85\u76f4\u64ad\u5f00\u59cb\u5e76\u81ea\u52a8\u5f55\u5236", None))
        self.btn_setting.setText(QCoreApplication.translate("Form", u"\u5f55\u5236\u8bbe\u7f6e", None))
        self.btn_vlcaddress.setText(QCoreApplication.translate("Form", u"VLC\u6d41\u5730\u5740", None))
        self.label_34.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u8def\u5f84", None))
        self.btn_selectdir.setText(QCoreApplication.translate("Form", u"\u6d4f\u89c8", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u76f4\u64ad\u4fe1\u606f", None))
        self.btn_inroom.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u76f4\u64ad\u95f4", None))
        self.btn_upinfo.setText(QCoreApplication.translate("Form", u"\u4e3b\u64ad\u4fe1\u606f", None))
        self.lab_roomimg.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"\u76f4\u64ad\u95f4ID:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u76f4\u64ad\u540d\u79f0:", None))
        self.lab_roomtitle.setText(QCoreApplication.translate("Form", u"Unknown", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u4e3b\u64adID:", None))
        self.lab_uid.setText(QCoreApplication.translate("Form", u"Unknown", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u76f4\u64ad\u72b6\u6001:", None))
        self.lab_livestatus.setText(QCoreApplication.translate("Form", u"Unknown", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u65f6\u95f4:", None))
        self.lab_startime.setText(QCoreApplication.translate("Form", u"Unknown", None))
        self.label_22.setText(QCoreApplication.translate("Form", u"\u76f4\u64ad\u6807\u7b7e:", None))
        self.lab_livetag.setText(QCoreApplication.translate("Form", u"Unknown", None))
        self.lab_roomid.setText(QCoreApplication.translate("Form", u"Unknown", None))
        self.pte_infobox.setPlainText(QCoreApplication.translate("Form", u"\u6b22\u8fce\u4f7f\u7528Bili Live\u5f55\u5236\u7a0b\u5e8f\n"
"\u7248\u672c\uff1aV1.0\n"
"Release Date\uff1a2021/11/07.....", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"\u5f55\u5236\u4fe1\u606f", None))
        self.label_27.setText(QCoreApplication.translate("Form", u"\u5f55\u5236\u72b6\u6001:", None))
        self.lab_recordstatus.setText(QCoreApplication.translate("Form", u"\u5f85\u547d", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u5df2\u4f20\u8f93\u5757\u6570:", None))
        self.lab_chunk.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"\u5df2\u4f20\u8f93\u5927\u5c0f:", None))
        self.lab_size.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"\u5f55\u5236\u65f6\u95f4:", None))
        self.lab_retime.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"\u4f20\u8f93\u901f\u7387:", None))
        self.lab_transpeed.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"CPU\u8d1f\u8f7d:", None))
        self.lab_cpu.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_23.setText(QCoreApplication.translate("Form", u"\u5185\u5b58\u5360\u7528:", None))
        self.lab_ram.setText(QCoreApplication.translate("Form", u"0", None))
        self.label_25.setText(QCoreApplication.translate("Form", u"\u78c1\u76d8\u5269\u4f59:", None))
        self.lab_spaces.setText(QCoreApplication.translate("Form", u"0", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"\u72b6\u6001\u66f2\u7ebf", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d\u901f\u7387", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u7cfb\u7edf\u8d1f\u8f7d", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u78c1\u76d8\u7a7a\u95f4", None))
        self.le_address.setPlaceholderText(QCoreApplication.translate("Form", u"\u8f93\u5165\u76f4\u64ad\u95f4HTTP/HTTPS\u5730\u5740", None))
        self.btn_roomenter.setText(QCoreApplication.translate("Form", u"\u8fdb\u5165\u76f4\u64ad\u95f4", None))
    # retranslateUi

