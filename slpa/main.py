from .imports import *

class QApplicationMessaging(QApplication):
    messageFromOtherInstance = Signal(bytes)

    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self._key = 'SLPA'
        self._timeout = 1000
        self._locked = False
        socket = QLocalSocket(self)
        socket.connectToServer(self._key, QIODevice.WriteOnly)
        if not socket.waitForConnected(self._timeout):
            self._server = QLocalServer(self)
            # noinspection PyUnresolvedReferences
            self._server.newConnection.connect(self.handleMessage)
            self._server.listen(self._key)
        else:
            self._locked = True
        socket.disconnectFromServer()

    def __del__(self):
        if not self._locked:
            self._server.close()

    def event(self, e):
        if e.type() == QEvent.FileOpen:
            self.messageFromOtherInstance.emit(bytes(e.file(), 'UTF-8'))
            return True
        else:
            return QApplication.event(self, e)

    def isRunning(self):
        return self._locked

    def handleMessage(self):
        socket = self._server.nextPendingConnection()
        if socket.waitForReadyRead(self._timeout):
            self.messageFromOtherInstance.emit(socket.readAll().data())

    def sendMessage(self, message):
        socket = QLocalSocket(self)
        socket.connectToServer(self._key, QIODevice.WriteOnly)
        socket.waitForConnected(self._timeout)
        socket.write(bytes(message, 'UTF-8'))
        socket.waitForBytesWritten(self._timeout)
        socket.disconnectFromServer()

class MajorFeatureLayout(QVBoxLayout):

    def __init__(self):
        QVBoxLayout.__init__(self)
        self.majorLocation = QComboBox()
        self.majorLocation.addItem('Major Location')
        self.minorLocation = QComboBox()
        self.minorLocation.addItem('Minor Location')
        self.movement = QComboBox()
        self.movement.addItem('Movement')
        self.orientation = QComboBox()
        self.orientation.addItem('Orientation')
        self.addWidget(self.majorLocation)
        self.addWidget(self.minorLocation)
        self.addWidget(self.movement)
        self.addWidget(self.orientation)

class ConfigLayout(QGridLayout):

    def __init__(self, n, handshapes, hand2):
        QGridLayout.__init__(self)
        self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)

        if n == 1:
            number = '1st'
        elif n == 2:
            number = '2nd'
        elif n == 3:
            number = '3rd'
        else:
            number = str(n)+'th'
        configLabel = QLabel('{} config'.format(number))
        self.addWidget(configLabel, 0, 0)
        forearmButton = QRadioButton('1. Forearm')
        self.addWidget(forearmButton, 0, 1)
        self.addLayout(handshapes, 0, 2)
        self.handShapeMatch = QPushButton('Make Hand 2 = Hand 1')
        self.addWidget(self.handShapeMatch, 1, 0)
        self.hand2 = hand2
        self.handShapeMatch.clicked.connect(self.hand2.match)

    @Slot(int)
    def changeMatched(self, checked):
        if self.handShapeMatch.isChecked():
            self.handShapeMatch.setChecked(False)

class HandShapeLayout(QVBoxLayout):
    def __init__(self, parent = None, hand = None):
        QVBoxLayout.__init__(self)#, parent)
        self.handTitle = QLabel(hand)
        self.addWidget(self.handTitle)
        self.globalWidget = QComboBox()
        self.globalWidget.addItem('Global')
        self.globalWidget.addItem('Alternative')
        self.addWidget(self.globalWidget)

        self.thumbWidget = QComboBox()
        self.thumbWidget.addItem('2.Thumb')
        self.thumbWidget.addItem('Alternative')
        self.addWidget(self.thumbWidget)

        self.thumbAndFingerWidget = QComboBox()
        self.thumbAndFingerWidget.addItem('3.Thumb/Finger')
        self.thumbAndFingerWidget.addItem('Alternative')
        self.addWidget(self.thumbAndFingerWidget)

        self.indexWidget = QComboBox()
        self.indexWidget.addItem('4.Index finger')
        self.indexWidget.addItem('Alternative')
        self.addWidget(self.indexWidget)

        self.middleWidget = QComboBox()
        self.middleWidget.addItem('5.Middle finger')
        self.middleWidget.addItem('Alternative')
        self.addWidget(self.middleWidget)

        self.ringWidget = QComboBox()
        self.ringWidget.addItem('6.Ring finger')
        self.ringWidget.addItem('Alternative')
        self.addWidget(self.ringWidget)

        self.pinkyWidget = QComboBox()
        self.pinkyWidget.addItem('7.Pinky finger')
        self.pinkyWidget.addItem('Alternative')
        self.addWidget(self.pinkyWidget)

    def fingers(self):
        return {'globalWidget': self.globalWidget.currentText(),
                'thumbWidget': self.thumbWidget.currentText(),
                'thumbAndFingerWidget': self.thumbAndFingerWidget.currentText(),
                'indexWidget': self.indexWidget.currentText(),
                'middleWidget': self.middleWidget.currentText(),
                'ringWidget': self.ringWidget.currentText(),
                'pinkyWidget': self.pinkyWidget.currentText()}

class SecondHandShapeLayout(HandShapeLayout):

    def __init__(self, parent = None, hand = None, otherHand = None):
        HandShapeLayout.__init__(self, parent, hand)
        self.otherHand = otherHand

    def setConfigLayout(self, configLayout):
        self.configLayout = configLayout
        self.globalWidget.currentIndexChanged.connect(self.configLayout.changeMatched)
        self.thumbWidget.currentIndexChanged.connect(self.configLayout.changeMatched)
        self.thumbAndFingerWidget.currentIndexChanged.connect(self.configLayout.changeMatched)
        self.indexWidget.currentIndexChanged.connect(self.configLayout.changeMatched)
        self.middleWidget.currentIndexChanged.connect(self.configLayout.changeMatched)
        self.ringWidget.currentIndexChanged.connect(self.configLayout.changeMatched)
        self.pinkyWidget.currentIndexChanged.connect(self.configLayout.changeMatched)

    @Slot(bool)
    def match(self, clicked):
        for finger,value in self.otherHand.fingers().items():
            widget = getattr(self, finger)
            widget.setCurrentText(value)

class GlossLayout(QBoxLayout):
    def __init__(self, parent = None):
        QBoxLayout.__init__(self, QBoxLayout.TopToBottom, parent=parent)

        self.setContentsMargins(-1,-1,-1,0)
        self.glossEdit = QLineEdit()
        self.glossEdit.setPlaceholderText('Gloss')
        self.addWidget(self.glossEdit)
        self.lineLayout = QHBoxLayout()
        self.lineLayout.setContentsMargins(-1,0,-1,-1)

        #SLOT 1
        self.lineLayout.addWidget(QLabel('['))
        slot1 = QLineEdit()
        slot1.setMaxLength(1)
        slot1.setFixedWidth(slot1.maxLength()*12)
        slot1.setPlaceholderText('_'*slot1.maxLength())
        self.lineLayout.addWidget(slot1)
        self.lineLayout.addWidget(QLabel(']1'))
        self.addLayout(self.lineLayout)

        #SLOT 2
        self.lineLayout.addWidget(QLabel('['))
        slot2 = QLineEdit()
        slot2.setMaxLength(4)
        slot2.setFixedWidth(slot2.maxLength()*12)
        slot2.setPlaceholderText('_ '*slot2.maxLength())
        self.lineLayout.addWidget(slot2)
        self.lineLayout.addWidget(QLabel(']2'))

        #SLOT 3
        self.lineLayout.addWidget(QLabel('['))
        slot3a = QLineEdit()
        slot3a.setMaxLength(2)
        slot3a.setFixedWidth(slot3a.maxLength()*12)
        slot3a.setPlaceholderText('_ '*slot3a.maxLength())
        self.lineLayout.addWidget(slot3a)
        self.lineLayout.addWidget(QLabel(u'\u2205/'))
        slot3b = QLineEdit()
        slot3b.setMaxLength(6)
        slot3b.setFixedWidth(slot3b.maxLength()*12)
        slot3b.setPlaceholderText('_ '*slot3b.maxLength())
        self.lineLayout.addWidget(slot3b)
        self.lineLayout.addWidget(QLabel(']3'))

        #SLOT 4
        self.lineLayout.addWidget(QLabel('[1'))
        slot4 = QLineEdit()
        slot4.setMaxLength(3)
        slot4.setFixedWidth(slot4.maxLength()*12)
        slot4.setPlaceholderText('_ '*slot4.maxLength())
        self.lineLayout.addWidget(slot4)
        self.lineLayout.addWidget(QLabel(']4'))

        #SLOT 5
        self.lineLayout.addWidget(QLabel('['))
        slot5a = QLineEdit()
        slot5a.setMaxLength(1)
        slot5a.setFixedWidth(slot5a.maxLength()*12)
        slot5a.setPlaceholderText(('_'*slot5a.maxLength()))
        self.lineLayout.addWidget(slot5a)
        self.lineLayout.addWidget(QLabel('2'))
        slot5b = QLineEdit()
        slot5b.setMaxLength(3)
        slot5b.setFixedWidth(slot5b.maxLength()*12)
        slot5b.setPlaceholderText('_ '*slot5b.maxLength())
        self.lineLayout.addWidget(slot5b)
        self.lineLayout.addWidget(QLabel(']5'))

        #SLOT 6
        self.lineLayout.addWidget(QLabel('['))
        slot6a = QLineEdit()
        slot6a.setMaxLength(1)
        slot6a.setFixedWidth(slot6a.maxLength()*12)
        slot6a.setPlaceholderText('_'*slot6a.maxLength())
        self.lineLayout.addWidget(slot6a)
        self.lineLayout.addWidget(QLabel('3'))
        slot6b = QLineEdit()
        slot6b.setMaxLength(3)
        slot6b.setFixedWidth(slot6b.maxLength()*12)
        slot6b.setPlaceholderText('_ '*slot6b.maxLength())
        self.lineLayout.addWidget(slot6b)
        self.lineLayout.addWidget(QLabel(']6'))

        #SLOT 7
        self.lineLayout.addWidget(QLabel('['))
        slot7a = QLineEdit()
        slot7a.setMaxLength(1)
        slot7a.setFixedWidth(slot7a.maxLength()*12)
        slot7a.setPlaceholderText('_'*slot7a.maxLength())
        self.lineLayout.addWidget(slot7a)
        self.lineLayout.addWidget(QLabel('4'))
        slot7b = QLineEdit()
        slot7b.setMaxLength(3)
        slot7b.setFixedWidth(slot7b.maxLength()*12)
        slot7b.setPlaceholderText('_ '*slot7b.maxLength())
        self.lineLayout.addWidget(slot7b)
        self.lineLayout.addWidget(QLabel(']7'))

class MainWindow(QMainWindow):
    def __init__(self,app):
        app.messageFromOtherInstance.connect(self.handleMessage)
        super(MainWindow, self).__init__()
        self.setWindowTitle('SLP-Annotator')
        self.wrapper = QWidget()

        layout = QVBoxLayout()

        self.gloss = GlossLayout(self)
        layout.addLayout(self.gloss)

        handsLayout = QGridLayout()
        hand1 = HandShapeLayout(handsLayout, 'Hand 1')
        handsLayout.addLayout(hand1, 0, 0)
        hand2 = SecondHandShapeLayout(handsLayout, 'Hand 2', hand1)
        handsLayout.addLayout(hand2, 0, 1)
        #layout.addLayout(handsLayout)

        configLayout = ConfigLayout(1, handsLayout, hand2)
        layout.addLayout(configLayout)

        #hand2.setConfigLayout(configLayout)

        featuresLayout = MajorFeatureLayout()
        layout.addLayout(featuresLayout)

        self.wrapper.setLayout(layout)
        self.setCentralWidget(self.wrapper)


    def sizeHint(self):
        sz = QMainWindow.sizeHint(self)
        minWidth = self.menuBar().sizeHint().width()
        if sz.width() < minWidth:
            sz.setWidth(minWidth)
        if sz.height() < 400:
            sz.setHeight(400)
        return sz

    def handleMessage(self):
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        # self.raise_()
        # self.show()
        self.activateWindow()

    def cleanUp(self):
        # Clean up everything
        for i in self.__dict__:
            item = self.__dict__[i]
            clean(item)


def clean(item):
    """Clean up the memory by closing and deleting the item if possible."""
    if isinstance(item, list) or isinstance(item, dict):
        for _ in range(len(item)):
            clean(item.pop())
    else:
        try:
            item.close()
        except (RuntimeError, AttributeError): # deleted or no close method
            pass
        try:
            item.deleteLater()
        except (RuntimeError, AttributeError): # deleted or no deleteLater method
            pass