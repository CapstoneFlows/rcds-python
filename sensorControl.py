import re
import os
import glob
import time
import serial
import bluepy

cmdAcks = {
    "ID=":"ID_ACK",
    "LOC=":"LOC_ACK",
    "DIR=":"DIR_ACK",
    "COMMENT=":"COMMENT_ACK",
    "START_RUNNING":"START_ACK",
    "STOP_RUNNING":"STOP_ACK",
    "RETURN_DATA":"RETURN_ACK",
    "SET_VARS":"SET_ACK",
    "RESET_DEVICE":"RESET_ACK"
}

class Connection():
    def __init__(self, conntype):
        super(Connection, self).__init__(conntype)
        self.type = conntype
        self.id = None
        self.conn = None

    def connect(self, did):
        self.id = did
        if self.type == "SERIAL":
            try:
                self.conn = serial.Serial(did, timeout=5)
                resp = self.sendCmd("?")
                if chr(65) in resp:
                    resp = self.sendCmd("T"+str(int(time.time())))
                    if "TIME_ACK" not in resp:
                        return False
                return True
            except:
                return False
        elif self.type == "BLE":
            try:
                self.conn = bluepy.btle.Peripheral(did)
                self.char = self.conn.getCharacteristics(uuid="0000ffe1-0000-1000-8000-00805f9b34fb")
                self.handle = self.char.getHandle()
                self.bleMsg = ""
                def getResponse(self, cHandle, data):
                    if self.handle == cHandle:
                        self.bleMsg = str(struct.unpack("s", data[1]))
                self.conn.delegate.handleNotification = getResponse
                resp = self.sendCmd("?")
                if chr(65) in resp:
                    resp = self.sendCmd("T"+str(int(time.time())))
                    if "TIME_ACK" not in resp:
                        return False
            except:
                return False

    def sendCmd(self, cmd):
        longReturn = "" 
        
        if self.type == "SERIAL":
            self.conn.write(cmd)
            line = self.conn.readline()
            if "RETURN_DATA" in cmd:
                while "END_TRANSFER" not in line:
                    longReturn += line + '\n'
                    line = self.conn.readline()
                return longReturn
            elif "RESET_DEVICE" in cmd:
                self.conn.setTimeout(60)
                while "NEED_VARS" not in line:
                    longReturn += line + '\n'
                    line = self.conn.readline()
                self.conn.setTimeout(5)
                return longReturn
            else:
                return line

        elif self.type == "BLE":
            self.bleMsg = ""
            self.char.write(cmd)
            if "RETURN_DATA" in cmd:
                while "END_TRANSFER" not in self.bleMsg:
                    ok = self.conn.waitForNotifications(5.0)
                    if not ok:
                        return None
                    longReturn += self.bleMsg + '\n'
                return longReturn
            elif "RESET_DEVICE" in cmd:
                while "NEED_VARS" not in self.bleMsg:
                    ok = self.conn.waitForNotifications(5.0)
                    if not ok:
                        return None
                    longReturn += self.bleMsg + '\n'
                return longReturn
            else:
                ok = self.conn.waitForNotifications(3.0)
                if ok:
                    return self.bleMsg
                else:
                    return None

    def close(self):
        if self.type == "SERIAL":
            self.conn.close()
        elif self.type == "BLE":
            self.conn.disconnect()


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
    return activePorts


def ScanBLEConnections():
    scanner = bluepy.btle.Scanner()
    devices = scanner.scan(1.0)

    activeDevices = []
    for dev in devices:
        if dev.connectable:
            activeDevices.append(dev.addr)
    return activeDevices


def ParseResp(resp):
    params = {}
    params["STATE"] = resp.split(" ")[0]
    self.id = params["ID"] = resp.split(" ID=")[1].split(" LOC=")[0]
    params["LOC"] = resp.split(" LOC=")[1].split(" DIR=")[0]
    params["DIR"] = resp.split(" DIR=")[1].split("COMMENT=")[0]
    params["COMMENT"] = resp.split("COMMENT=")[1]
    return params


def ConnectSerial(device):
    conn = Connection("SERIAL")
    ok = conn.connect(device)
    if ok:
        resp = conn.sendCmd("?")
        return conn, ParseResp(resp)
    else:
        return None, None


def ConnectBLE(device):
    conn = Connection("BLE")
    ok = conn.connect(device)
    if ok:
        resp = conn.sendCmd("?")
        return conn, ParseResp(resp)
    else:
        return None, None


def SetParams(conn, params):
    resp = conn.sendCmd("SET_VARS")
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
    conn.sendCmd("START_RUNNING")
    resp = conn.sendCmd("?")

    if resp:
        return ParseResp(resp)
    else:
        return None


def Stop(conn):
    conn.sendCmd("STOP_RUNNING")
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


def SaveData(conn, path, winunix):
    resp = conn.sendCmd("RETURN_DATA")
    if resp:
        parsedData = ParseData(resp, conn.id)
        dirPath = path+winunix+conn.id;
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        for fileName in parsedData:
            with open(dirPath+winunix+fileName, 'w') as f:
                f.writelines(parsedData[fileName])
    else:
        return None

    resp = conn.sendCmd("?")

    if resp:
        return ParseResp(resp)
    else:
        return None


def Reset(conn):
    conn.sendCmd("RESET_DEVICE")
    resp = conn.sendCmd("?")

    if resp:
        return ParseResp(resp)
    else:
        return None