import re
import os
import glob
import time
import serial
import pygatt

#cmdAcks = {
#    "ID=":"ID_ACK",
#    "LOC=":"LOC_ACK",
#    "DIR=":"DIR_ACK",
#    "COMMENT=":"COMMENT_ACK",
#    "START_RUNNING":"START_ACK",
#    "STOP_RUNNING":"STOP_ACK",
#    "RETURN_DATA":"RETURN_ACK",
#    "SET_VARS":"SET_ACK",
#    "RESET_DEVICE":"RESET_ACK"
#}

class Connection():
    def __init__(self, conntype):
        self.type = conntype
        self.id = None
        self.conn = None

    def connect(self, did):
        self.id = did
        if self.type == "SERIAL":
            try:
                self.conn = serial.Serial(did, timeout=2)
                resp = self.sendCmd("T"+str(int(time.time())))
                if "TIME_ACK" not in resp:
                    for tries in range(2):
                        resp = self.sendCmd("?")
                        if "ID=" not in resp:
                            return False
                        return True
                return True
            except:
                return False
            '''
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
                resp = self.sendCmd("T"+str(int(time.time())))
                if "TIME_ACK" not in resp:
                    resp = self.sendCmd("?")
                    if "ID=" not in resp:
                        return False
                    return True
                return True
            except:
                return False
            '''
        else:
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
                while "RESET_COMPLETE" not in line:
                    longReturn += line + '\n'
                    line = self.conn.readline()
                return longReturn
            else:
                return line
            '''
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
                while "RESET_COMPLETE" not in self.bleMsg:
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
            '''
        else:
            return None

    def close(self):
        if self.type == "SERIAL":
            self.conn.close()
            '''
        elif self.type == "BLE":
            self.conn.disconnect()
            '''


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


def ScanBLEConnections():
    return [], "BLE not supported yet."
    '''
    scanner = bluepy.btle.Scanner()
    try:
        devices = scanner.scan(1.0)

        activeDevices = []
        for dev in devices:
            if dev.connectable:
                activeDevices.append(dev.addr)
        return activeDevices, "Scanned BLE devices; "+str(len(activeDevices))+" available."
    except bluepy.btle.BTLEException, e:
        if "le on" in str(e):
            return [], "No BLE capability on this machine."
        else:
            return [], "Unable to scan: "+str(e)
    '''

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


def ConnectBLE(device):
    '''
    conn = Connection("BLE")
    ok = conn.connect(device)
    if ok:
        resp = conn.sendCmd("?")
        return conn, ParseResp(resp)
    else:
        return None, None
    '''
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