import re
import os
import glob
import time
import serial
import pygatt

UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"

class Connection():
    def __init__(self, conntype):
        self.type = conntype
        self.id = None
        self.conn = None

    def connect(self, did):
        self.id = did
        if self.type == "SERIAL":
            try:
                self.conn = serial.Serial(did, timeout=1, writeTimeout=1)
                resp = self.sendCmd("T"+str(int(time.time())))
                if "TIME_ACK" not in resp:
                    resp = self.sendCmd("?")
                    if "ID=" not in resp:
                        return False
                    return True
                return True
            except:
                return False

        elif self.type == "BLE_WINDOWS":
            self.adapter = pygatt.BGAPIBackend()

            try:
                self.adapter.start()
                self.conn = adapter.connect(did)
                self.handle = device.get_handle(UUID)
                self.bleMsg = ""
                def getResponse(self, handle, data):
                    if self.handle == handle:
                        self.bleMsg = data.decode("hex")
                self.conn.subscribe(UUID, callback=self.getResponse)
                resp = self.sendCmd("T"+str(int(time.time())))
                if "TIME_ACK" not in resp:
                    resp = self.sendCmd("?")
                    if "ID=" not in resp:
                        return False
                    return True
                return True
            except:
                return False

        elif self.type == "BLE_UNIX":
            self.adapter = pygatt.GATTToolBackend()

            try:
                self.adapter.start()
                self.conn = adapter.connect(did)
                self.handle = device.get_handle(UUID)
                self.bleMsg = ""
                def getResponse(self, handle, data):
                    if self.handle == handle:
                        self.bleMsg = data.decode("hex")
                self.conn.subscribe(UUID, callback=self.getResponse)
                resp = self.sendCmd("T"+str(int(time.time())))
                if "TIME_ACK" not in resp:
                    resp = self.sendCmd("?")
                    if "ID=" not in resp:
                        return False
                    return True
                return True
            except:
                return False
        else:
            return False

    def sendCmd(self, cmd):
        longReturn = "" 

        if self.type == "SERIAL":
            self.conn.write(cmd)
            line = self.conn.readline()
            if "RETURN_DATA" in cmd:
                while "END_TRANSFER" not in line:
                    if line:
                        longReturn += line + '\n'
                    line = self.conn.readline()
                return longReturn
            elif "RESET_DEVICE" in cmd:
                while "RESET_COMPLETE" not in line:
                    if line:
                        longReturn += line + '\n'
                    line = self.conn.readline()
                return longReturn
            else:
                return line
        elif self.type == "BLE_WINDOWS" or self.type == "BLE_UNIX":
            self.bleMsg = ""
            self.conn.char_write_handle(self.handle, [char.encode("hex") for char in cmd])
            if "RETURN_DATA" in cmd:
                while "END_TRANSFER" not in self.bleMsg:
                    if self.bleMsg:
                        longReturn += self.bleMsg + '\n'
                return longReturn
            elif "RESET_DEVICE" in cmd:
                while "RESET_COMPLETE" not in self.bleMsg:
                    if self.bleMsg:
                        longReturn += self.bleMsg + '\n'
                return longReturn
            else:
                ok = self.conn.waitForNotifications(3.0)
                if ok:
                    return self.bleMsg
                else:
                    return None
        else:
            return None

    def close(self):
        if self.type == "SERIAL":
            self.conn.close()
        elif self.type == "BLE_WINDOWS":
            self.adapter.stop()
        elif self.type == "BLE_UNIX":
            self.adapter.stop()


def ScanSerialConnections(platform):
    if platform == "linux" or platform == "linux2": #Linux
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif platform == "darwin": #OSX
        ports = glob.glob('/dev/tty.*')
    elif platform == "win32": #Windows
        ports = ['COM%s' % (i + 1) for i in range(256)]
    else:
        raise EnvironmentError('Unsupported platform')

    activePorts = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            activePorts.append(port)
        except:
            pass
    return activePorts, "Scanned serial devices; "+str(len(activePorts))+" available."


def ScanBLEConnections(platform):
    if platform == "linux" or platform == "linux2" or platform == "darwin": #Unix
        adapter = pygatt.GATTToolBackend()
        try:
            adapter.start()
            devs = adapter.scan()

            activeDevices = [dev["address"] for dev in devs]
            return activeDevices, "Scanned BLE devices; "+str(len(activeDevices))+" available."
        except pygatt.exceptions.NotConnectedError, e:
            return [], "No BLE capability on this machine."
        except:
            return [], "Unable to scan: "+str(e)

    elif platform == "win32": #Windows
        adapter = pygatt.BGAPIBackend()
        try:
            adapter.start()
            devs = adapter.scan()

            activeDevices = [dev["address"] for dev in devs]
            return activeDevices, "Scanned BLE devices; "+str(len(activeDevices))+" available."
        except pygatt.exceptions.NotConnectedError, e:
            return [], "No BLE capability on this machine."
        except:
            return [], "Unable to scan: "+str(e)
    else:
        raise EnvironmentError('Unsupported platform')


def ParseResp(resp):
    params = {}
    params["STATE"] = resp.split(" ")[0]
    params["ID"] = resp.split(" ID=")[1].split(" LOC=")[0]
    params["LOC"] = resp.split(" LOC=")[1].split(" DIR=")[0]
    params["DIR"] = resp.split(" DIR=")[1].split("COMMENT=")[0]
    params["COMMENT"] = resp.split("COMMENT=")[1].split('\r')[0]
    return params


def ConnectSerial(device):
    conn = Connection("SERIAL")
    ok = conn.connect(device)
    if ok:
        resp = conn.sendCmd("?")
        return conn, ParseResp(resp)
    else:
        return None, None


def ConnectBLEWindows(device):
    conn = CONNECTION("BLE_WINDOWS")
    ok = conn.connect(device)
    if ok:
        resp = conn.sendCmd("?")
        return conn, ParseResp(resp)
    else:
        return None, None


def ConnectBLEUnix(device):
    conn = CONNECTION("BLE_UNIX")
    ok = conn.connect(device)
    if ok:
        resp = conn.sendCmd("?")
        return conn, ParseResp(resp)
    else:
        return None, None


def SetParams(conn, params):
    conn.sendCmd("SET_VARS")
    time.sleep(1)
    conn.sendCmd("ID="+params["ID"])
    conn.sendCmd("LOC="+params["LOC"])
    conn.sendCmd("DIR="+params["DIR"])
    conn.sendCmd("COMMENT="+params["COMMENT"])
    resp = conn.sendCmd("?")

    if resp:
        return ParseResp(resp)
    else:
        return None


def Start(conn):
    resp = conn.sendCmd("START_RUNNING")
    if "ACK" not in resp:
        return None

    resp = conn.sendCmd("?")

    if resp:
        return ParseResp(resp)
    else:
        return None


def Stop(conn):
    resp = conn.sendCmd("STOP_RUNNING")
    if "ACK" not in resp:
        return None

    resp = conn.sendCmd("?")

    if resp:
        return ParseResp(resp)
    else:
        return None


def ParseData(resp, did):
    fileName = None
    inFile = False
    parsedData = {}
    for line in resp.split('\n'):
        if "BEGIN_FILE=" in line:
            fileName = did+"_"+line.split("BEGIN_FILE=")[1]
            parsedData[fileName] = []
            inFile = True
        elif "END_FILE" in line:
            inFile = False
            fileName = None
        elif inFile:
            parsedData[fileName].append(line)
    return parsedData


def SaveData(conn, path, did):
    resp = conn.sendCmd("RETURN_DATA")
    if "ACK" not in resp:
        return None
    else:
        parsedData = ParseData(resp, did)
        dirPath = os.path.join(path, did);
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        for fileName in parsedData:
            with open(os.path.join(dirPath, fileName), 'w') as f:
                f.writelines(parsedData[fileName])

    resp = conn.sendCmd("?")

    if resp:
        return ParseResp(resp)
    else:
        return None


def Reset(conn):
    resp = conn.sendCmd("RESET_DEVICE")
    if "ACK" not in resp:
        return None
    resp = conn.sendCmd("?")

    if resp:
        return ParseResp(resp)
    else:
        return None