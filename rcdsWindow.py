# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rcdsWindow.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.SensorTab = QtGui.QWidget()
        self.SensorTab.setObjectName(_fromUtf8("SensorTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.SensorTab)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.SensorGroupBox = QtGui.QGroupBox(self.SensorTab)
        self.SensorGroupBox.setFlat(True)
        self.SensorGroupBox.setCheckable(False)
        self.SensorGroupBox.setObjectName(_fromUtf8("SensorGroupBox"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.SensorGroupBox)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.SerialRadioButton = QtGui.QRadioButton(self.SensorGroupBox)
        self.SerialRadioButton.setChecked(True)
        self.SerialRadioButton.setObjectName(_fromUtf8("SerialRadioButton"))
        self.verticalLayout_3.addWidget(self.SerialRadioButton)
        self.BLERadioButton = QtGui.QRadioButton(self.SensorGroupBox)
        self.BLERadioButton.setChecked(False)
        self.BLERadioButton.setObjectName(_fromUtf8("BLERadioButton"))
        self.verticalLayout_3.addWidget(self.BLERadioButton)
        self.verticalLayout_2.addWidget(self.SensorGroupBox)
        self.ScanDevicesButton = QtGui.QPushButton(self.SensorTab)
        self.ScanDevicesButton.setObjectName(_fromUtf8("ScanDevicesButton"))
        self.verticalLayout_2.addWidget(self.ScanDevicesButton)
        self.DeviceListComboBox = QtGui.QComboBox(self.SensorTab)
        self.DeviceListComboBox.setObjectName(_fromUtf8("DeviceListComboBox"))
        self.verticalLayout_2.addWidget(self.DeviceListComboBox)
        self.DeviceConnectButton = QtGui.QPushButton(self.SensorTab)
        self.DeviceConnectButton.setEnabled(False)
        self.DeviceConnectButton.setObjectName(_fromUtf8("DeviceConnectButton"))
        self.verticalLayout_2.addWidget(self.DeviceConnectButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_6 = QtGui.QGridLayout()
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.IDLabel = QtGui.QLabel(self.SensorTab)
        self.IDLabel.setObjectName(_fromUtf8("IDLabel"))
        self.gridLayout_6.addWidget(self.IDLabel, 0, 0, 1, 1)
        self.IDLineEdit = QtGui.QLineEdit(self.SensorTab)
        self.IDLineEdit.setObjectName(_fromUtf8("IDLineEdit"))
        self.gridLayout_6.addWidget(self.IDLineEdit, 0, 1, 1, 1)
        self.LocLabel = QtGui.QLabel(self.SensorTab)
        self.LocLabel.setObjectName(_fromUtf8("LocLabel"))
        self.gridLayout_6.addWidget(self.LocLabel, 1, 0, 1, 1)
        self.LocLineEdit = QtGui.QLineEdit(self.SensorTab)
        self.LocLineEdit.setObjectName(_fromUtf8("LocLineEdit"))
        self.gridLayout_6.addWidget(self.LocLineEdit, 1, 1, 1, 1)
        self.DirLabel = QtGui.QLabel(self.SensorTab)
        self.DirLabel.setObjectName(_fromUtf8("DirLabel"))
        self.gridLayout_6.addWidget(self.DirLabel, 2, 0, 1, 1)
        self.DirLineEdit = QtGui.QLineEdit(self.SensorTab)
        self.DirLineEdit.setObjectName(_fromUtf8("DirLineEdit"))
        self.gridLayout_6.addWidget(self.DirLineEdit, 2, 1, 1, 1)
        self.CommentLabel = QtGui.QLabel(self.SensorTab)
        self.CommentLabel.setObjectName(_fromUtf8("CommentLabel"))
        self.gridLayout_6.addWidget(self.CommentLabel, 3, 0, 1, 1)
        self.CommentLineEdit = QtGui.QLineEdit(self.SensorTab)
        self.CommentLineEdit.setObjectName(_fromUtf8("CommentLineEdit"))
        self.gridLayout_6.addWidget(self.CommentLineEdit, 3, 1, 1, 1)
        self.StateLabel = QtGui.QLabel(self.SensorTab)
        self.StateLabel.setObjectName(_fromUtf8("StateLabel"))
        self.gridLayout_6.addWidget(self.StateLabel, 4, 0, 1, 1)
        self.StateLineEdit = QtGui.QLineEdit(self.SensorTab)
        self.StateLineEdit.setReadOnly(True)
        self.StateLineEdit.setObjectName(_fromUtf8("StateLineEdit"))
        self.gridLayout_6.addWidget(self.StateLineEdit, 4, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_6)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.SetButton = QtGui.QPushButton(self.SensorTab)
        self.SetButton.setEnabled(False)
        self.SetButton.setObjectName(_fromUtf8("SetButton"))
        self.verticalLayout_5.addWidget(self.SetButton)
        self.StartButton = QtGui.QPushButton(self.SensorTab)
        self.StartButton.setEnabled(False)
        self.StartButton.setObjectName(_fromUtf8("StartButton"))
        self.verticalLayout_5.addWidget(self.StartButton)
        self.StopButton = QtGui.QPushButton(self.SensorTab)
        self.StopButton.setEnabled(False)
        self.StopButton.setObjectName(_fromUtf8("StopButton"))
        self.verticalLayout_5.addWidget(self.StopButton)
        self.SaveButton = QtGui.QPushButton(self.SensorTab)
        self.SaveButton.setEnabled(False)
        self.SaveButton.setObjectName(_fromUtf8("SaveButton"))
        self.verticalLayout_5.addWidget(self.SaveButton)
        self.ResetButton = QtGui.QPushButton(self.SensorTab)
        self.ResetButton.setEnabled(False)
        self.ResetButton.setObjectName(_fromUtf8("ResetButton"))
        self.verticalLayout_5.addWidget(self.ResetButton)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.TerminalLabel = QtGui.QLabel(self.SensorTab)
        self.TerminalLabel.setObjectName(_fromUtf8("TerminalLabel"))
        self.verticalLayout_7.addWidget(self.TerminalLabel)
        self.TerminalPlainTextEdit = QtGui.QPlainTextEdit(self.SensorTab)
        self.TerminalPlainTextEdit.setReadOnly(True)
        self.TerminalPlainTextEdit.setObjectName(_fromUtf8("TerminalPlainTextEdit"))
        self.verticalLayout_7.addWidget(self.TerminalPlainTextEdit)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 0, 1, 1, 1)
        self.tabWidget.addTab(self.SensorTab, _fromUtf8(""))
        self.FilterTab = QtGui.QWidget()
        self.FilterTab.setObjectName(_fromUtf8("FilterTab"))
        self.gridLayout_7 = QtGui.QGridLayout(self.FilterTab)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.FilterSelectFolderButton = QtGui.QPushButton(self.FilterTab)
        self.FilterSelectFolderButton.setObjectName(_fromUtf8("FilterSelectFolderButton"))
        self.verticalLayout_8.addWidget(self.FilterSelectFolderButton)
        self.FilterFileListWidget = QtGui.QListWidget(self.FilterTab)
        self.FilterFileListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.FilterFileListWidget.setObjectName(_fromUtf8("FilterFileListWidget"))
        self.verticalLayout_8.addWidget(self.FilterFileListWidget)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.ETLabel = QtGui.QLabel(self.FilterTab)
        self.ETLabel.setObjectName(_fromUtf8("ETLabel"))
        self.gridLayout_5.addWidget(self.ETLabel, 0, 0, 1, 1)
        self.EDateTimeEdit = QtGui.QDateTimeEdit(self.FilterTab)
        self.EDateTimeEdit.setCalendarPopup(True)
        self.EDateTimeEdit.setObjectName(_fromUtf8("EDateTimeEdit"))
        self.gridLayout_5.addWidget(self.EDateTimeEdit, 0, 1, 1, 1)
        self.LTLabel = QtGui.QLabel(self.FilterTab)
        self.LTLabel.setObjectName(_fromUtf8("LTLabel"))
        self.gridLayout_5.addWidget(self.LTLabel, 1, 0, 1, 1)
        self.LDateTimeEdit = QtGui.QDateTimeEdit(self.FilterTab)
        self.LDateTimeEdit.setDate(QtCore.QDate(2099, 12, 31))
        self.LDateTimeEdit.setTime(QtCore.QTime(0, 0, 0))
        self.LDateTimeEdit.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(7999, 12, 30), QtCore.QTime(23, 59, 59)))
        self.LDateTimeEdit.setCalendarPopup(True)
        self.LDateTimeEdit.setObjectName(_fromUtf8("LDateTimeEdit"))
        self.gridLayout_5.addWidget(self.LDateTimeEdit, 1, 1, 1, 1)
        self.MinTOLabel = QtGui.QLabel(self.FilterTab)
        self.MinTOLabel.setObjectName(_fromUtf8("MinTOLabel"))
        self.gridLayout_5.addWidget(self.MinTOLabel, 2, 0, 1, 1)
        self.MaxTOLabel = QtGui.QLabel(self.FilterTab)
        self.MaxTOLabel.setObjectName(_fromUtf8("MaxTOLabel"))
        self.gridLayout_5.addWidget(self.MaxTOLabel, 3, 0, 1, 1)
        self.MinCMHLabel = QtGui.QLabel(self.FilterTab)
        self.MinCMHLabel.setObjectName(_fromUtf8("MinCMHLabel"))
        self.gridLayout_5.addWidget(self.MinCMHLabel, 4, 0, 1, 1)
        self.MinCMHSpinBox = QtGui.QSpinBox(self.FilterTab)
        self.MinCMHSpinBox.setMinimum(10)
        self.MinCMHSpinBox.setMaximum(40)
        self.MinCMHSpinBox.setObjectName(_fromUtf8("MinCMHSpinBox"))
        self.gridLayout_5.addWidget(self.MinCMHSpinBox, 4, 1, 1, 1)
        self.MaxCMHLabel = QtGui.QLabel(self.FilterTab)
        self.MaxCMHLabel.setObjectName(_fromUtf8("MaxCMHLabel"))
        self.gridLayout_5.addWidget(self.MaxCMHLabel, 5, 0, 1, 1)
        self.MaxCMHSpinBox = QtGui.QSpinBox(self.FilterTab)
        self.MaxCMHSpinBox.setMinimum(10)
        self.MaxCMHSpinBox.setMaximum(40)
        self.MaxCMHSpinBox.setProperty("value", 40)
        self.MaxCMHSpinBox.setObjectName(_fromUtf8("MaxCMHSpinBox"))
        self.gridLayout_5.addWidget(self.MaxCMHSpinBox, 5, 1, 1, 1)
        self.MinCMLLabel = QtGui.QLabel(self.FilterTab)
        self.MinCMLLabel.setObjectName(_fromUtf8("MinCMLLabel"))
        self.gridLayout_5.addWidget(self.MinCMLLabel, 6, 0, 1, 1)
        self.MinCMLSpinBox = QtGui.QSpinBox(self.FilterTab)
        self.MinCMLSpinBox.setObjectName(_fromUtf8("MinCMLSpinBox"))
        self.gridLayout_5.addWidget(self.MinCMLSpinBox, 6, 1, 1, 1)
        self.MaxCMLLabel = QtGui.QLabel(self.FilterTab)
        self.MaxCMLLabel.setObjectName(_fromUtf8("MaxCMLLabel"))
        self.gridLayout_5.addWidget(self.MaxCMLLabel, 7, 0, 1, 1)
        self.MaxCMLSpinBox = QtGui.QSpinBox(self.FilterTab)
        self.MaxCMLSpinBox.setMaximum(9999)
        self.MaxCMLSpinBox.setProperty("value", 9999)
        self.MaxCMLSpinBox.setObjectName(_fromUtf8("MaxCMLSpinBox"))
        self.gridLayout_5.addWidget(self.MaxCMLSpinBox, 7, 1, 1, 1)
        self.MinSLabel = QtGui.QLabel(self.FilterTab)
        self.MinSLabel.setObjectName(_fromUtf8("MinSLabel"))
        self.gridLayout_5.addWidget(self.MinSLabel, 8, 0, 1, 1)
        self.MaxSLabel = QtGui.QLabel(self.FilterTab)
        self.MaxSLabel.setObjectName(_fromUtf8("MaxSLabel"))
        self.gridLayout_5.addWidget(self.MaxSLabel, 9, 0, 1, 1)
        self.MinSSpinBox = QtGui.QSpinBox(self.FilterTab)
        self.MinSSpinBox.setObjectName(_fromUtf8("MinSSpinBox"))
        self.gridLayout_5.addWidget(self.MinSSpinBox, 8, 1, 1, 1)
        self.MaxSSpinBox = QtGui.QSpinBox(self.FilterTab)
        self.MaxSSpinBox.setProperty("value", 99)
        self.MaxSSpinBox.setObjectName(_fromUtf8("MaxSSpinBox"))
        self.gridLayout_5.addWidget(self.MaxSSpinBox, 9, 1, 1, 1)
        self.MinTSpinBox = QtGui.QSpinBox(self.FilterTab)
        self.MinTSpinBox.setMaximum(99999)
        self.MinTSpinBox.setObjectName(_fromUtf8("MinTSpinBox"))
        self.gridLayout_5.addWidget(self.MinTSpinBox, 2, 1, 1, 1)
        self.MaxTSpinBox = QtGui.QSpinBox(self.FilterTab)
        self.MaxTSpinBox.setMaximum(99999)
        self.MaxTSpinBox.setProperty("value", 99999)
        self.MaxTSpinBox.setObjectName(_fromUtf8("MaxTSpinBox"))
        self.gridLayout_5.addWidget(self.MaxTSpinBox, 3, 1, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_5)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.ShowDataButton = QtGui.QPushButton(self.FilterTab)
        self.ShowDataButton.setEnabled(False)
        self.ShowDataButton.setObjectName(_fromUtf8("ShowDataButton"))
        self.horizontalLayout_4.addWidget(self.ShowDataButton)
        self.SavetoFileButton = QtGui.QPushButton(self.FilterTab)
        self.SavetoFileButton.setEnabled(False)
        self.SavetoFileButton.setObjectName(_fromUtf8("SavetoFileButton"))
        self.horizontalLayout_4.addWidget(self.SavetoFileButton)
        self.verticalLayout_9.addLayout(self.horizontalLayout_4)
        self.DataPlainTextEdit = QtGui.QPlainTextEdit(self.FilterTab)
        self.DataPlainTextEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.DataPlainTextEdit.setReadOnly(True)
        self.DataPlainTextEdit.setObjectName(_fromUtf8("DataPlainTextEdit"))
        self.verticalLayout_9.addWidget(self.DataPlainTextEdit)
        self.horizontalLayout_5.addLayout(self.verticalLayout_9)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)
        self.horizontalLayout_5.setStretch(2, 4)
        self.gridLayout_7.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.FilterTab, _fromUtf8(""))
        self.DataTab = QtGui.QWidget()
        self.DataTab.setObjectName(_fromUtf8("DataTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.DataTab)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.SelectFolderButton = QtGui.QPushButton(self.DataTab)
        self.SelectFolderButton.setObjectName(_fromUtf8("SelectFolderButton"))
        self.verticalLayout_4.addWidget(self.SelectFolderButton)
        self.GraphFileListWidget = QtGui.QListWidget(self.DataTab)
        self.GraphFileListWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.GraphFileListWidget.setObjectName(_fromUtf8("GraphFileListWidget"))
        self.verticalLayout_4.addWidget(self.GraphFileListWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.DataGraphicsView = PlotWidget(self.DataTab)
        self.DataGraphicsView.setObjectName(_fromUtf8("DataGraphicsView"))
        self.horizontalLayout_3.addWidget(self.DataGraphicsView)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 3)
        self.gridLayout_4.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.DataComboBox = QtGui.QComboBox(self.DataTab)
        self.DataComboBox.setObjectName(_fromUtf8("DataComboBox"))
        self.horizontalLayout_2.addWidget(self.DataComboBox)
        self.DataShowButton = QtGui.QPushButton(self.DataTab)
        self.DataShowButton.setEnabled(False)
        self.DataShowButton.setObjectName(_fromUtf8("DataShowButton"))
        self.horizontalLayout_2.addWidget(self.DataShowButton)
        self.SaveImageButton = QtGui.QPushButton(self.DataTab)
        self.SaveImageButton.setEnabled(False)
        self.SaveImageButton.setObjectName(_fromUtf8("SaveImageButton"))
        self.horizontalLayout_2.addWidget(self.SaveImageButton)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.tabWidget.addTab(self.DataTab, _fromUtf8(""))
        self.MapTab = QtGui.QWidget()
        self.MapTab.setObjectName(_fromUtf8("MapTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.MapTab)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label = QtGui.QLabel(self.MapTab)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.tabWidget.addTab(self.MapTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSerial_Connection = QtGui.QAction(MainWindow)
        self.actionSerial_Connection.setObjectName(_fromUtf8("actionSerial_Connection"))
        self.actionBLE_Connection = QtGui.QAction(MainWindow)
        self.actionBLE_Connection.setObjectName(_fromUtf8("actionBLE_Connection"))
        self.actionDownload = QtGui.QAction(MainWindow)
        self.actionDownload.setObjectName(_fromUtf8("actionDownload"))
        self.actionUpload = QtGui.QAction(MainWindow)
        self.actionUpload.setObjectName(_fromUtf8("actionUpload"))
        self.actionSet_Up = QtGui.QAction(MainWindow)
        self.actionSet_Up.setObjectName(_fromUtf8("actionSet_Up"))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "RCDS Tool", None))
        self.SensorGroupBox.setTitle(_translate("MainWindow", "Sensor Connection", None))
        self.SerialRadioButton.setText(_translate("MainWindow", "Serial USB", None))
        self.BLERadioButton.setText(_translate("MainWindow", "Bluetooth", None))
        self.ScanDevicesButton.setText(_translate("MainWindow", "Scan Devices", None))
        self.DeviceConnectButton.setText(_translate("MainWindow", "Connect", None))
        self.IDLabel.setText(_translate("MainWindow", "ID", None))
        self.LocLabel.setText(_translate("MainWindow", "Location", None))
        self.DirLabel.setText(_translate("MainWindow", "Direction", None))
        self.CommentLabel.setText(_translate("MainWindow", "Comment", None))
        self.StateLabel.setText(_translate("MainWindow", "State", None))
        self.SetButton.setText(_translate("MainWindow", "Set Parameters", None))
        self.StartButton.setText(_translate("MainWindow", "Start Running", None))
        self.StopButton.setText(_translate("MainWindow", "Stop Running", None))
        self.SaveButton.setText(_translate("MainWindow", "Save Data", None))
        self.ResetButton.setText(_translate("MainWindow", "Reset Device", None))
        self.TerminalLabel.setText(_translate("MainWindow", "Terminal", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SensorTab), _translate("MainWindow", "Sensor Control", None))
        self.FilterSelectFolderButton.setText(_translate("MainWindow", "Select Folder", None))
        self.ETLabel.setText(_translate("MainWindow", "Earliest Data", None))
        self.LTLabel.setText(_translate("MainWindow", "Latest Data", None))
        self.MinTOLabel.setText(_translate("MainWindow", "Min Milliseconds", None))
        self.MaxTOLabel.setText(_translate("MainWindow", "Max Milliseconds", None))
        self.MinCMHLabel.setText(_translate("MainWindow", "Min Car Height (cm)", None))
        self.MaxCMHLabel.setText(_translate("MainWindow", "Max Car Height (cm)", None))
        self.MinCMLLabel.setText(_translate("MainWindow", "Min Car Length (cm)", None))
        self.MaxCMLLabel.setText(_translate("MainWindow", "Max Car Length (cm)", None))
        self.MinSLabel.setText(_translate("MainWindow", "Min Speed (mph)", None))
        self.MaxSLabel.setText(_translate("MainWindow", "Max Speed (mph)", None))
        self.ShowDataButton.setText(_translate("MainWindow", "Show Data", None))
        self.SavetoFileButton.setText(_translate("MainWindow", "Save to File", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.FilterTab), _translate("MainWindow", "Filtering and Compilation", None))
        self.SelectFolderButton.setText(_translate("MainWindow", "Select Folder", None))
        self.DataShowButton.setText(_translate("MainWindow", "Show Data", None))
        self.SaveImageButton.setText(_translate("MainWindow", "Save Image", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DataTab), _translate("MainWindow", "Data Visualization", None))
        self.label.setText(_translate("MainWindow", "To be integrated!", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MapTab), _translate("MainWindow", "Map Layout", None))
        self.actionSerial_Connection.setText(_translate("MainWindow", "Serial Connection", None))
        self.actionBLE_Connection.setText(_translate("MainWindow", "BLE Connection", None))
        self.actionDownload.setText(_translate("MainWindow", "Download", None))
        self.actionUpload.setText(_translate("MainWindow", "Upload", None))
        self.actionSet_Up.setText(_translate("MainWindow", "Set Up", None))

from pyqtgraph import PlotWidget
