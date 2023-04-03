from websocket_server import WebsocketServer
import datetime
import random
import json
import sys
from PyQt5 import QtGui, QtCore
from wsGui import Ui_Dialog

class WebSocket(QtCore.QThread):
    GotMsg = QtCore.pyqtSignal(list)    
    server = WebsocketServer(9000, "127.0.0.1")
    awaitingResult = True
    result = 'fail'
    
    def new_client(self, client, server):
        self.server.send_message_to_all(json.dumps({u'result': u'new'}))
    
    def client_msg(self, client, server, message):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        name = message
        self.GotMsg.emit([client, message])
        greeting = "Hello {0}! at {1}".format(name, now)
        #self.server.send_message(client, greeting)
        
        while self.awaitingResult:
            pass
        
        self.server.send_message(client, self.result)
        self.awaitingResult = True

        
    # Called for every client disconnecting
    def client_left(self, client, server):
        self.server.server_close()
        print("Client(%d) disconnected" % client['id'])

    def run(self):
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_message_received(self.client_msg)
        self.server.set_fn_client_left(self.client_left)
        self.server.run_forever()

        
class ServerGui(QtGui.QDialog, Ui_Dialog):
  sendResult = QtCore.pyqtSignal(str)
  def __init__(self, ws = None):
    # exec_() method deletes the object instance on close
    # select as 'modal' in designer to freeze background window
    super().__init__()
    self.setupUi(self)
    
    self.WebSocketThread = WebSocket()
    self.WebSocketThread.moveToThread(self.WebSocketThread)
    
    self.LogModel  = QtGui.QStandardItemModel() #Stores lines of log messages
    self.rxList.setModel(self.LogModel)
    self.startBtn.clicked.connect(self.startServer)
    self.passBtn.clicked.connect(self.txResultPass)
    self.failBtn.clicked.connect(self.txResultFail)
    self.WebSocketThread.GotMsg.connect(self.msgPass)
    #self.sendResult.connect(self.WebSocketThread.sendMsg)
    
  def startServer(self):
    self.WebSocketThread.start()
    print('started server')

  def txResultPass(self):
    self.sendResult.emit(json.dumps({u'result': u'pass'}))
    print('GUI', json.dumps({u'result': u'pass'}))
  
  def txResultFail(self):
    self.sendResult.emit(json.dumps({u'result': u'fail'}))
    print('GUI', json.dumps({u'result': u'fail'}))
    
  def closeEvent(self, *args, **kwargs):
    #self.WebSocketThread.eventloop.stop()
    pass
    
  def msgPass(self, msgList):
    print(msgList)
    item = QtGui.QStandardItem(msgList)
    self.LogModel.appendRow([item])
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = ServerGui()
    main.show()
    sys.exit(app.exec_())