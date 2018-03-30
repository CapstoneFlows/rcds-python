import os
import sys
import json
import numpy as np
from PyQt4 import QtCore, QtGui

from rcdsWindow import Ui_MainWindow, _translate
import rcds_res_rc

import sensorControl as sc
import dataFiltering as df
import dataVisualization as dv
import trafficDirection as td

###############################################################################

class RCDSTool(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(RCDSTool, self).__init__(parent)

        # Check what OS we are on
        self.platform = sys.platform

        # Set up UI
        self.ui = Ui_MainWindow()
        self.setWindowFlags(self.windowFlags() |
                              QtCore.Qt.WindowSystemMenuHint |
                              QtCore.Qt.WindowMinMaxButtonsHint)
        self.ui.setupUi(self)

        # Set up function bindings and tab-based variables
        self.conn = None
        self.raw_path = os.getcwd()
        self.ui.SerialRadioButton.toggled.connect(self.ClearDeviceList)
        self.ui.BLERadioButton.toggled.connect(self.ClearDeviceList)
        self.ui.ScanDevicesButton.clicked.connect(self.ScanDevices)
        self.ui.DeviceConnectButton.clicked.connect(self.ConnectToDevice)
        self.ui.SetButton.clicked.connect(self.SetParameters)
        self.ui.StartButton.clicked.connect(self.StartRunning)
        self.ui.StopButton.clicked.connect(self.StopRunning)
        self.ui.SaveButton.clicked.connect(self.SaveRawData)
        self.ui.ResetButton.clicked.connect(self.ResetDevice)

        self.filter_path = os.getcwd()
        self.ui.UnitsComboBox.addItem("SI")
        self.ui.UnitsComboBox.addItem("Imperial")
        self.ChangeUnits()
        self.ui.UnitsComboBox.currentIndexChanged.connect(self.ChangeUnits)
        self.ui.FilterSelectFolderButton.clicked.connect(self.SelectFilterFolder)
        self.ui.ShowDataButton.clicked.connect(self.ShowFilteredData)
        self.ui.SavetoFileButton.clicked.connect(self.SaveFilteredData)

        self.data_path = os.getcwd()
        for key in dv.graph_handles.keys():
            self.ui.DataComboBox.addItem(key)
        self.ui.SelectFolderButton.clicked.connect(self.SelectVisualizationFolder)
        self.ui.DataShowButton.clicked.connect(self.GraphData)
        self.ui.SaveImageButton.clicked.connect(self.SaveGraph)
        self.ui.GraphSlider.sliderMoved.connect(self.ChangeGraphFrame)

        self.map_path = os.getcwd()
        self.idsIn = {}
        self.idsOut = {}
        self.orderData = None
        self.ui.nInComboBox.currentIndexChanged.connect(lambda: self.SensorSelect('NIn'))
        self.ui.eInComboBox.currentIndexChanged.connect(lambda: self.SensorSelect('EIn'))
        self.ui.sInComboBox.currentIndexChanged.connect(lambda: self.SensorSelect('SIn'))
        self.ui.wInComboBox.currentIndexChanged.connect(lambda: self.SensorSelect('WIn'))
        self.ui.nOutComboBox.currentIndexChanged.connect(lambda: self.SensorSelect('NOut'))
        self.ui.eOutComboBox.currentIndexChanged.connect(lambda: self.SensorSelect('EOut'))
        self.ui.sOutComboBox.currentIndexChanged.connect(lambda: self.SensorSelect('SOut'))
        self.ui.wOutComboBox.currentIndexChanged.connect(lambda: self.SensorSelect('WOut'))
        self.ui.CompileButton.clicked.connect(self.CompileDirections)
        self.ui.MapSaveButton.clicked.connect(self.SaveOrderData)
        self.ui.ClearButton.clicked.connect(self.ClearDevices)

###############################################################################

    # Sensor Control Functions

    # TODO: Find way to make live terminal

    def WriteTerminal(self, msg):
        self.ui.TerminalPlainTextEdit.appendPlainText(msg)

    def ClearDeviceList(self):
        self.ui.DeviceListComboBox.clear()
        self.ui.DeviceConnectButton.setDisabled(True)

    def ClearParams(self):
            self.ui.IDLineEdit.clear()
            self.ui.LocLineEdit.clear()
            self.ui.DirLineEdit.clear()
            self.ui.CommentLineEdit.clear()
            self.ui.StateLineEdit.clear()

    def ScanDevices(self):
        self.ui.DeviceListComboBox.clear()
        self.ClearParams()
        if self.ui.SerialRadioButton.isChecked():
            devices, info = sc.ScanSerialConnections(self.platform)
        elif self.ui.BLERadioButton.isChecked():
            devices, info = sc.ScanBLEConnections(self.platform)

        if devices:
            self.ui.DeviceListComboBox.addItems(devices)
            self.ui.DeviceConnectButton.setDisabled(False)
            self.WriteTerminal(str(info))
        else:
            self.ui.DeviceConnectButton.setDisabled(True)
            self.WriteTerminal(str(info))

    def ButtonsSetDisabled(self, state):
        self.ui.SetButton.setDisabled(state)
        self.ui.StartButton.setDisabled(state)
        self.ui.StopButton.setDisabled(state)
        self.ui.SaveButton.setDisabled(state)
        self.ui.ResetButton.setDisabled(state)

    def GetSetParams(self, info=None):
        if info:
            self.ui.IDLineEdit.setText(info["ID"])
            self.ui.LocLineEdit.setText(info["LOC"])
            self.ui.DirLineEdit.setText(info["DIR"])
            self.ui.CommentLineEdit.setText(info["COMMENT"])
            self.ui.StateLineEdit.setText(info["STATE"])
        else:
            params = {}
            params["ID"] = str(self.ui.IDLineEdit.text())
            params["LOC"] = str(self.ui.LocLineEdit.text())
            params["DIR"] = str(self.ui.DirLineEdit.text())
            params["COMMENT"] = str(self.ui.CommentLineEdit.text())
            return params

    def ConnectToDevice(self):
        device = str(self.ui.DeviceListComboBox.currentText())
        if self.ui.SerialRadioButton.isChecked():
            conn, info = sc.ConnectSerial(device)
        elif self.ui.BLERadioButton.isChecked():
            conn, info = sc.ConnectBLE(device)

        if info:
            self.GetSetParams(info)
            self.WriteTerminal("Connected to " + device)
            self.WriteTerminal(str(info))

            if "ERROR" in info["STATE"]:
                self.WriteTerminal("Device is in error state: " + info["STATE"])
                self.WriteTerminal("Address error before continuing.")
                self.conn.close()
                self.conn = None
                self.ButtonsSetDisabled(True)
            elif "NEED_VARS" in info["STATE"]:
                self.WriteTerminal("Device needs parameters.")
                self.WriteTerminal("Set new parameters before continuing.")
                self.conn = conn
                self.ButtonsSetDisabled(True)
                self.ui.SetButton.setDisabled(False)
            else:
                self.conn = conn
                self.ButtonsSetDisabled(False)
        else:
            self.WriteTerminal("Unable to connect to " + device)
            self.conn = None
            self.ButtonsSetDisabled(True)

    def HandleInfo(self, info, okmsg, errmsg):
        if info:
            self.GetSetParams(info)
            self.WriteTerminal(okmsg)
            self.WriteTerminal(str(info))

            if "ERROR" in info["STATE"]:
                self.WriteTerminal("Device is in error state: " + info["STATE"])
                self.WriteTerminal("Address error before continuing.")
                self.conn.close()
                self.conn = None
                self.ButtonsSetDisabled(True)
            elif "NEED_VARS" in info["STATE"]:
                self.WriteTerminal("Device needs parameters.")
                self.WriteTerminal("Set new parameters before continuing.")
                self.ButtonsSetDisabled(True)
                self.ui.SetButton.setDisabled(False)
            else:
                self.ButtonsSetDisabled(False)
        else:
            self.WriteTerminal(errmsg)
            self.conn.close()
            self.conn = None
            self.ButtonsSetDisabled(True)

    def SetParameters(self):
        params = self.GetSetParams()

        info = sc.SetParams(self.conn, params)
        self.HandleInfo(info, "Updated parameters.", "Error setting new parameters.")

    def StartRunning(self):
        info = sc.Start(self.conn)
        self.HandleInfo(info, "Started device.", "Error starting device.")

    def StopRunning(self):
        info = sc.Stop(self.conn)
        self.HandleInfo(info, "Stopped device.", "Error stopping device.")

    def SaveRawData(self):
        self.raw_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Save Directory", self.raw_path))
        if self.raw_path:
            self.WriteTerminal("Getting data from device, please wait.")
            info = sc.SaveData(self.conn, self.raw_path, str(self.ui.IDLineEdit.text()))
            self.HandleInfo(info, "Saved data from device.", "Error saving data.")
        else:
            self.WriteTerminal("No path selected, cannot save.")

    def ResetDevice(self):
        self.WriteTerminal("Resetting device, please wait.")
        info = sc.Reset(self.conn)
        self.HandleInfo(info, "Reset device successfully.", "Error resetting device.")

###############################################################################
    # Data Filtering Functions

    def ChangeUnits(self):
        if str(self.ui.UnitsComboBox.currentText()) == "Imperial":
            self.ui.MinCMHLabel.setText(_translate("MainWindow", "Min Car Height (in)", None))
            self.ui.MaxCMHLabel.setText(_translate("MainWindow", "Max Car Height (in)", None))
            self.ui.MinCMLLabel.setText(_translate("MainWindow", "Min Car Length (in)", None))
            self.ui.MaxCMLLabel.setText(_translate("MainWindow", "Max Car Length (in)", None))
            self.ui.MinSLabel.setText(_translate("MainWindow", "Min Speed (mph)", None))
            self.ui.MaxSLabel.setText(_translate("MainWindow", "Max Speed (mph)", None))
        else:
            self.ui.MinCMHLabel.setText(_translate("MainWindow", "Min Car Height (cm)", None))
            self.ui.MaxCMHLabel.setText(_translate("MainWindow", "Max Car Height (cm)", None))
            self.ui.MinCMLLabel.setText(_translate("MainWindow", "Min Car Length (cm)", None))
            self.ui.MaxCMLLabel.setText(_translate("MainWindow", "Max Car Length (cm)", None))
            self.ui.MinSLabel.setText(_translate("MainWindow", "Min Speed (kmh)", None))
            self.ui.MaxSLabel.setText(_translate("MainWindow", "Max Speed (kmh)", None))

    def SelectFilterFolder(self):
        self.filter_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Filter Directory", self.filter_path))
        if self.filter_path:
            files = [f for f in os.listdir(self.filter_path) if (os.path.isfile(os.path.join(self.filter_path, f)) and '.csv' in f)]
            if files:
                self.ui.FilterFileListWidget.addItems(files)
                self.ui.ShowDataButton.setDisabled(False)
                self.ui.SavetoFileButton.setDisabled(False)
            else:
                self.ui.ShowDataButton.setDisabled(True)
                self.ui.SavetoFileButton.setDisabled(True)
        else:
            self.ui.ShowDataButton.setDisabled(True)
            self.ui.SavetoFileButton.setDisabled(True)

    def GetFilters(self):
        filters = {}
        filters["EDateTime"] = int(self.ui.EDateTimeEdit.dateTime().toTime_t())
        filters["LDateTime"] = int(self.ui.LDateTimeEdit.dateTime().toTime_t())
        filters["MinTO"] = self.ui.MinTSpinBox.value()
        filters["MaxTO"] = self.ui.MaxTSpinBox.value()
        if str(self.ui.UnitsComboBox.currentText()) == "Imperial":
            filters["MinCMH"] = int(float(self.ui.MinCMHSpinBox.value()) * 2.54)
            filters["MaxCMH"] = int(float(self.ui.MaxCMHSpinBox.value()) * 2.54)
            filters["MinCML"] = int(float(self.ui.MinCMLSpinBox.value()) * 2.54)
            filters["MaxCML"] = int(float(self.ui.MaxCMLSpinBox.value()) * 2.54)
            filters["MinS"] = int(float(self.ui.MinSSpinBox.value()) * 1.60934)
            filters["MaxS"] = int(float(self.ui.MaxSSpinBox.value()) * 1.60934)
        else:
            filters["MinCMH"] = int(self.ui.MinCMHSpinBox.value())
            filters["MaxCMH"] = int(self.ui.MaxCMHSpinBox.value())
            filters["MinCML"] = int(self.ui.MinCMLSpinBox.value())
            filters["MaxCML"] = int(self.ui.MaxCMLSpinBox.value())
            filters["MinS"] = int(self.ui.MinSSpinBox.value())
            filters["MaxS"] = int(self.ui.MaxSSpinBox.value())
        return filters

    def ShowFilteredData(self):
        selectedFiles = [str(x.text()) for x in self.ui.FilterFileListWidget.selectedItems()]
        filterData = df.ProcessData(self.filter_path, selectedFiles, self.GetFilters())
        self.ui.DataPlainTextEdit.setPlainText(filterData)

    def SaveFilteredData(self):
        name = str(QtGui.QFileDialog.getSaveFileName(self, "Save Filtered Data File", self.filter_path, selectedFilter='*.csv'))
        df.SaveData(name, str(self.ui.DataPlainTextEdit.toPlainText()))

###############################################################################
    # Data Visualization Functions

    def SelectVisualizationFolder(self):
        self.data_path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Data Directory", self.data_path))
        if self.data_path:
            files = [f for f in os.listdir(self.data_path) if (os.path.isfile(os.path.join(self.data_path, f)) and '.csv' in f)]
            if files:
                self.ui.GraphFileListWidget.addItems(files)
                self.ui.DataShowButton.setDisabled(False)
                self.ui.SaveImageButton.setDisabled(False)
            else:
                self.ui.DataShowButton.setDisabled(True)
                self.ui.SaveImageButton.setDisabled(True)
        else:
            self.ui.DataShowButton.setDisabled(True)
            self.ui.SaveImageButton.setDisabled(True)

    def GraphData(self):
        self.ui.DataGraphicsView.getPlotItem().clear()
        graph_func = str(self.ui.DataComboBox.currentText())
        selectedFiles = [os.path.join(self.data_path, str(x.text())) for x in self.ui.GraphFileListWidget.selectedItems()]
        dv.graph_handles[graph_func](selectedFiles, self.ui.DataGraphicsView)

    def SaveGraph(self):
        name = str(QtGui.QFileDialog.getSaveFileName(self, "Save Graph as Image", self.data_path, selectedFilter='*.png'))
        dv.SaveGraph(name, self.ui.DataGraphicsView)

    def ChangeGraphFrame(self):
        pass

###############################################################################
    # Data Visualization Functions

    def SensorFileSelect(self, buttonstr):
        if buttonstr == 'NIn':
            self.idsIn['NIn'] = str(QtGui.QFileDialog.getOpenFileName(self, "Open File for North In Sensor", self.data_path, selectedFilter='*.csv'))
        elif buttonstr == 'NOut':
            self.idsOut['NOut'] = str(QtGui.QFileDialog.getOpenFileName(self, "Open File for North Out Sensor", self.data_path, selectedFilter='*.csv'))
        elif buttonstr == 'EIn':
            self.idsIn['EIn'] = str(QtGui.QFileDialog.getOpenFileName(self, "Open File for East In Sensor", self.data_path, selectedFilter='*.csv'))
        elif buttonstr == 'EOut':
            self.idsOut['EOut'] = str(QtGui.QFileDialog.getOpenFileName(self, "Open File for East Out Sensor", self.data_path, selectedFilter='*.csv'))
        elif buttonstr == 'SIn':
            self.idsIn['SIn'] = str(QtGui.QFileDialog.getOpenFileName(self, "Open File for South In Sensor", self.data_path, selectedFilter='*.csv'))
        elif buttonstr == 'SOut':
            self.idsOut['SOut'] = str(QtGui.QFileDialog.getOpenFileName(self, "Open File for South Out Sensor", self.data_path, selectedFilter='*.csv'))
        elif buttonstr == 'WIn':
            self.idsIn['WIn'] = str(QtGui.QFileDialog.getOpenFileName(self, "Open File for West In Sensor", self.data_path, selectedFilter='*.csv'))
        elif buttonstr == 'WOut':
            self.idsOut['WOut'] = str(QtGui.QFileDialog.getOpenFileName(self, "Open File for West Out Sensor", self.data_path, selectedFilter='*.csv'))
        self.UpdateChecks(buttonstr)

    def UpdateChecks(self, buttonstr):
        if buttonstr == 'NIn' or buttonstr == 'NOut':
            if self.ui.nCheck.checkState() == QtCore.Qt.PartiallyChecked:
                self.ui.nCheck.setCheckState(QtCore.Qt.Checked)
            else:
                self.ui.nCheck.setCheckState(QtCore.Qt.PartiallyChecked)
        elif buttonstr == 'EIn' or buttonstr == 'EOut':
            if self.ui.eCheck.checkState() == QtCore.Qt.PartiallyChecked:
                self.ui.eCheck.setCheckState(QtCore.Qt.Checked)
            else:
                self.ui.eCheck.setCheckState(QtCore.Qt.PartiallyChecked)
        elif buttonstr == 'SIn' or buttonstr == 'SOut':
            if self.ui.sCheck.checkState() == QtCore.Qt.PartiallyChecked:
                self.ui.sCheck.setCheckState(QtCore.Qt.Checked)
            else:
                self.ui.sCheck.setCheckState(QtCore.Qt.PartiallyChecked)
        elif buttonstr == 'WIn' or buttonstr == 'WOut':
            if self.ui.wCheck.checkState() == QtCore.Qt.PartiallyChecked:
                self.ui.wCheck.setCheckState(QtCore.Qt.Checked)
            else:
                self.ui.wCheck.setCheckState(QtCore.Qt.PartiallyChecked)

        if len(self.idsIn.keys()) > 0 and len(self.idsOut.keys()) > 0:
            self.ui.CompileButton.setDisabled(False)

    def CompileDirections(self):
        self.orderData = td.getTrafficFlow(self.idsIn, self.idsOut)
        if self.orderData:
            self.ui.MapSaveButton.setDisabled(False)

    def SaveOrderData(self):
        name = str(QtGui.QFileDialog.getSaveFileName(self, "Save Order Data File", self.data_path, selectedFilter='*.csv'))
        np.savetxt(name, self.orderData, fmt='%i', delimiter=",")

    def ClearDevices(self):
        self.idsIn = {}
        self.idsOut = {}
        self.ui.nCheck.setCheckState(QtCore.Qt.Unchecked)
        self.ui.eCheck.setCheckState(QtCore.Qt.Unchecked)
        self.ui.sCheck.setCheckState(QtCore.Qt.Unchecked)
        self.ui.wCheck.setCheckState(QtCore.Qt.Unchecked)
        self.ui.CompileButton.setDisabled(True)
        self.ui.MapSaveButton.setDisabled(True)

###############################################################################

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = RCDSTool()
    myapp.show()
    sys.exit(app.exec_())