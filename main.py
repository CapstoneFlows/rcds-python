import os
import sys
from PyQt4 import QtCore, QtGui
from rcdsWindow import Ui_MainWindow
import sensorControl as sc
import dataFiltering as df
import dataVisualization as dv

class RCDSTool(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(RCDSTool, self).__init__(parent)

        # Check what OS we are on
        self.platform = sys.platform

        if self.platform == "linux" or self.platform == "linux2" \
            or self.platform == "darwin": #Unix
            self.winunix = '/'
        elif self.platform == "win32": #Windows
            self.winunix = '\\'

        # Set up UI
        self.ui = Ui_MainWindow()
        self.setWindowFlags(self.windowFlags() |
                              QtCore.Qt.WindowSystemMenuHint |
                              QtCore.Qt.WindowMinMaxButtonsHint)
        self.ui.setupUi(self)

        # Set up function bindings and tab-based variables
        self.conn = None
        self.ui.SerialRadioButton.toggled.connect(self.ClearDeviceList)
        self.ui.BLERadioButton.toggled.connect(self.ClearDeviceList)
        self.ui.ScanDevicesButton.clicked.connect(self.ScanDevices)
        self.ui.DeviceConnectButton.clicked.connect(self.ConnectToDevice)
        self.ui.SetButton.clicked.connect(self.SetParameters)
        self.ui.StartButton.clicked.connect(self.StartRunning)
        self.ui.StopButton.clicked.connect(self.StopRunning)
        self.ui.SaveButton.clicked.connect(self.SaveRawData)
        self.ui.ResetButton.clicked.connect(self.ResetDevice)

        self.ui.FilterSelectFolderButton.clicked.connect(self.SelectFilterFolder)
        self.ui.ShowDataButton.clicked.connect(self.ShowFilteredData)
        self.ui.SavetoFileButton.clicked.connect(self.SaveFilteredData)

        self.ui.SelectFolderButton.clicked.connect(self.SelectVisualizationFolder)
        self.ui.DataShowButton.clicked.connect(self.GraphData)
        self.ui.SaveImageButton.clicked.connect(self.SaveGraph)

###############################################################################

    # Sensor Control Functions

    # TODO: Find way to make live terminal

    def WriteTerminal(self, msg):
        self.ui.TerminalTextEdit.insertPlainText(msg)

    def ClearDeviceList(self):
        self.ui.DeviceListComboBox.clear()
        self.ui.DeviceConnectButton.setDisabled(True)

    def ScanDevices(self):
        if self.ui.SerialRadioButton.isChecked():
            devices = sc.ScanSerialConnections(self.platform)
        elif self.ui.BLERadioButton.isChecked():
            devices = sc.ScanBLEConnections()

        if devices:
            self.ui.DeviceListComboBox.addItems(devices)
            self.ui.DeviceConnectButton.setDisabled(False)
        else:
            self.ui.DeviceConnectButton.setDisabled(True)

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
            self.WriteTerminal("\nConnected to " + device)
            self.WriteTerminal("\n" + info)

            if "ERROR" in info["STATE"]:
                self.WriteTerminal("\nDevice is in error state: " + info["STATE"])
                self.WriteTerminal("\nAddress error before continuing.")
                self.conn.close()
                self.conn = None
                self.ButtonsSetDisabled(True)
            elif "NEED_VARS" in info["STATE"]:
                self.WriteTerminal("\nDevice needs parameters.")
                self.WriteTerminal("\nSet new parameters before continuing.")
                self.ButtonsSetDisabled(True)
                self.ui.SetButton.setDisabled(False)
            else:
                self.conn = conn
                self.ButtonsSetDisabled(False)
        else:
            self.WriteTerminal("\nUnable to connect to " + device)
            self.conn.close()
            self.conn = None
            self.ButtonsSetDisabled(True)

    def HandleInfo(self, info, okmsg, errmsg):
        if info:
            self.GetSetParams(info)
            self.WriteTerminal("\n" + okmsg)
            self.WriteTerminal("\n" + info)

            if "ERROR" in info["STATE"]:
                self.WriteTerminal("\nDevice is in error state: " + info["STATE"])
                self.WriteTerminal("\nAddress error before continuing.")
                self.conn.close()
                self.conn = None
                self.ButtonsSetDisabled(True)
            elif "NEED_VARS" in info["STATE"]:
                self.WriteTerminal("\nDevice needs parameters.")
                self.WriteTerminal("\nSet new parameters before continuing.")
                self.ButtonsSetDisabled(True)
                self.ui.SetButton.setDisabled(False)
        else:
            self.WriteTerminal("\n" + errmsg)
            self.conn.close()
            self.conn = None
            self.ButtonsSetDisabled(True)

    def SetParameters(self):
        params = GetSetParams()

        info = sc.SetParams(self.conn, params)
        self.HandleInfo(info, "Updated parameters.", "Error setting new parameters.")

    def StartRunning(self):
        info = sc.Start(self.conn)
        self.HandleInfo(info, "Started device.", "Error starting device.")

    def StopRunning(self):
        info = sc.Stop(self.conn)
        self.HandleInfo(info, "Stopped device.", "Error stopping device.")

    def SaveRawData(self):
        path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", os.getcwd()))
        if path:
            os.chdir(path)
            self.WriteTerminal("\nGetting data from device, please wait.")
            info = sc.SaveData(self.conn, path, self.winunix)
            self.HandleInfo(info, "Saved data from device.", "Error saving data.")
        else:
            self.WriteTerminal("\nNo path selected, cannot save.")

    def ResetDevice(self):
        self.WriteTerminal("\nResetting device, please wait.")
        info = sc.Reset(self.conn)
        self.HandleInfo(info, "Reset device successfully.", "Error resetting device.")

###############################################################################
    # Data Filtering Functions

    def SelectFilterFolder(self):
        pass

    def ShowFilteredData(self):
        pass

    def SaveFilteredData(self):
        pass

###############################################################################
    # Data Visualization Functions

    def SelectVisualizationFolder(self):
        pass

    def GraphData(self):
        pass

    def SaveGraph(self):
        pass

###############################################################################

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = RCDSTool()
    myapp.show()
    sys.exit(app.exec_())