#!/usr/bin/python3

import json, socket, sys, zmq
from PyQt4 import QtCore, QtGui
from time import sleep, strftime

class dxLite():
    def __init__(self):
        context = zmq.Context()
        self.dxsocket = context.socket(zmq.SUBSCRIBE)
        self.dxsocket.connect("tcp://clublog.org:7373")

    def read(self):
        try:
            message = self.dxsocket.recv() # Wait for and accept ZMQ data
            message = message.decode() # Decode to a string
            data = json.loads(message) # Decode JSON data into list
        except UnicodeDecodeError:
            data = False # allows use of "if dxLite.read():" to test valid
        except:
            raise
        return data

class winTest():
    def __init__(self, address='192.168.0.255', port=9871, name=""):
        self.broadcast_address = address
        self.broadcast_port = port
        self.station_name = name
        self.wt_net=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.wt_net.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self, data): # Generic 'send' function
        self.wt_net.sendto(self.chk(data),(self.broadcast_address,self.broadcast_port)) # Broadcast to Win-Test

    def telnet(self, data):
        self.send('RCVDPKT: "TELNET" "" "' + data + '\n"')

    def chk(self, message): # Generate Win-Test checksum
        checksum = 0
        message = str(message)
        for c in message:
           checksum += ord(c)
        checksum = (checksum | 128)
        checksum = bytearray.fromhex(hex(checksum)[-2:])# + chr(0).encode()
        payload = message.encode() + checksum
        return payload

class mainUI(QtGui.QMainWindow):
    def __init__(self,  parent=None):
        super(mainUI, self).__init__()
        self.initUI()

    def initUI(self):
		
        smallFont = QtGui.QFont()
        smallFont.setPointSize(8)
        smallFont.setFamily("monospace")

        self.txt0 = QtGui.QTextEdit(self)
        self.txt0.setReadOnly(True)
        self.txt0.setFixedWidth(540)
        self.txt0.setFixedHeight(220)
        self.txt0.setFont(smallFont)
        self.txt0.move(5,5)

        text, ok = QtGui.QInputDialog.getText(self, 'Broadcast Address', 'Enter the broadcast address:', text='192.168.0.255');
        if ok:
            broadcast_address = text
        else:
            exit(0)

        self.spots_thread = getSpots(broadcast_address)
        self.connect(self.spots_thread, QtCore.SIGNAL("updateScreen(QString)"), self.updateScreen)
        self.spots_thread.start()

        # Print a header - 1) because we can; 2) shows the user something has happened.
        self.updateScreen('                ~~')
        self.updateScreen(' DX Cluster powered by DXLite 0MQ')
        self.updateScreen('     http://dxlite.g7vjr.org     ')
        self.updateScreen('                ~~')

#        self.resize(550,230)
        self.setFixedSize(550,230)
        self.center()
        self.setWindowTitle('wtDxLite ['+text+']')
        self.setWindowIcon(QtGui.QIcon('web.png'))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def updateScreen(self, content):
        self.txt0.append(content)

class getSpots(QtCore.QThread):
    def __init__(self, broadcast_address=''):
        QtCore.QThread.__init__(self)
        self.cluster = dxLite()
        self.win_test = winTest(address=broadcast_address)

    def run(self):
        while True:
            data = self.cluster.read()
            if data:
                # DXLite doesn't include '.0', but wtDxTelnet does ...
                #   ... probably doesn't matter, but this is intended to replicate behaviour exactly.
                frequency = str(data["Freq"])
                if '.' not in frequency:
                    frequency = frequency + ".0"

                string = 'DX de ' + (data["Spotter"][:9]+":").ljust(9) + ' ' \
                                  + frequency.rjust(8) + '  ' \
                                  + data["Call"][:12].ljust(12) + ' ' \
                                  + data["Comment"][:29].ljust(30) + ' ' \
                                  + str(data["Date"])[11:13] + str(data["Date"])[14:16] + 'Z'

                self.emit(QtCore.SIGNAL('updateScreen(QString)'), string ) # Send to GUI
                self.win_test.telnet(string) # Broadcast to Win-Test

def main():
    global app, ex
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    app = QtGui.QApplication(sys.argv)
    ex = mainUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

