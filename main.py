import os
import sys
import json
import numpy as np
from PyQt4 import QtCore, QtGui

from rcdsWindow import Ui_MainWindow, _translate    
import sensorControl as sc
import dataFiltering as df
import dataVisualization as dv

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

        self.ui.nButton.clicked.connect(self.SensorFileSelect)
        self.ui.eButton.clicked.connect(self.SensorFileSelect)
        self.ui.sButton.clicked.connect(self.SensorFileSelect)
        self.ui.wButton.clicked.connect(self.SensorFileSelect)
        self.ui.PlayPauseButton.clicked.connect(self.PlayPauseMap)
        self.ui.MapSaveButton.clicked.connect(self.SaveOrderData)
        self.ui.PlaySlider.sliderMoved.connect(self.ChangeTimePosition)

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

    def SensorFileSelect(self):
        pass

    def PlayPauseMap(self):
        pass

    def SaveOrderData(self):
        pass

    def ChangeTimePosition(self):
        pass

###############################################################################

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = RCDSTool()
    myapp.show()
    sys.exit(app.exec_())