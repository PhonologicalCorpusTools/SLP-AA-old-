from .imports import *
import itertools

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
        forearmButton = QCheckBox('1. Forearm')
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

        self.indexWidget = FingerConfigurationComboBox()#('4.Index finger')
        self.addWidget(self.indexWidget)

        self.middleWidget = FingerConfigurationComboBox()#('5.Middle finger')
        self.addWidget(self.middleWidget)

        self.ringWidget = FingerConfigurationComboBox()#('6.Ring finger')
        self.addWidget(self.ringWidget)

        self.pinkyWidget = FingerConfigurationComboBox()#('7.Pinky finger')
        self.addWidget(self.pinkyWidget)

    def fingers(self):
        return {'globalWidget': self.globalWidget.currentText(),
                'thumbWidget': self.thumbWidget.currentText(),
                'thumbAndFingerWidget': self.thumbAndFingerWidget.currentText(),
                'indexWidget': self.indexWidget.currentText(),
                'middleWidget': self.middleWidget.currentText(),
                'ringWidget': self.ringWidget.currentText(),
                'pinkyWidget': self.pinkyWidget.currentText()}

    def fingerWidgets(self):
        return [self.indexWidget, self.middleWidget, self.ringWidget, self.pinkyWidget]

class FingerConfigurationComboBox(QComboBox):

    def __init__(self, first=None):
        QCheckBox.__init__(self)
        if first is not None:
            self.addItem(first)
        self.symbols = ['H','h','E','e','F', 'f', 'i']
        triples = [triple for triple in itertools.product(self.symbols, self.symbols, self.symbols)]


        marked = list()
        for n in range(len(triples)):
            # Constraint - no medial joint can be 'H'
            if triples[n][1] == 'H':
                marked.append(n)
            # Constraint - distal joint must match medial join in flexion
            distal = triples[n][2]
            medial = triples[n][1]
            if (distal == 'f' and medial=='F') or (distal =='F' and medial == 'f'):
                marked.append(n)
        triples = [triples[n] for n in range(len(triples)) if not n in marked]

        # marked = list()
        # for n in range(len(triples)):
        #     distal = triples[n][2]
        #     medial = triples[n][1]
        #     if (distal == 'f' and medial=='F') or (distal =='F' and medial == 'f'):
        #         marked.append(n)
        # triples = [triples[n] for n in range(len(triples)) if not n in marked]


        for t in triples:
            self.addItem(','.join(t))


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
    def __init__(self, parent = None, comboBoxes = None):
        QBoxLayout.__init__(self, QBoxLayout.TopToBottom, parent=parent)

        defaultFont = QFont("Arial", 12)
        fontMetric = QFontMetricsF(defaultFont)
        self.setContentsMargins(-1,-1,-1,0)
        self.glossEdit = QLineEdit()
        self.glossEdit.setPlaceholderText('Gloss')
        self.glossEdit.setFont(defaultFont)
        self.addWidget(self.glossEdit)
        self.lineLayout = QHBoxLayout()
        self.lineLayout.setContentsMargins(-1,0,-1,-1)

        #SLOT 1
        self.lineLayout.addWidget(QLabel('['))
        self.slot1 = QLineEdit()
        self.slot1.setMaxLength(1)
        self.slot1.setFont(defaultFont)
        width = fontMetric.boundingRect('_ '*(self.slot1.maxLength()+1)).width()
        self.slot1.setFixedWidth(width)
        self.slot1.setPlaceholderText('_'*self.slot1.maxLength())
        self.lineLayout.addWidget(self.slot1)
        self.lineLayout.addWidget(QLabel(']1'))
        self.addLayout(self.lineLayout)

        #SLOT 2
        self.lineLayout.addWidget(QLabel('['))
        self.slot2 = QLineEdit()
        self.slot2.setMaxLength(4)
        self.slot2.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot2.maxLength() + 1)).width()
        self.slot2.setFixedWidth(width)
        self.slot2.setPlaceholderText('_ '*self.slot2.maxLength())
        self.lineLayout.addWidget(self.slot2)
        self.lineLayout.addWidget(QLabel(']2'))

        #SLOT 3
        self.lineLayout.addWidget(QLabel('['))
        self.slot3a = QLineEdit()
        self.slot3a.setMaxLength(2)
        self.slot3a.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot3a.maxLength() + 1)).width()
        self.slot3a.setFixedWidth(width)
        self.slot3a.setPlaceholderText('_ '*self.slot3a.maxLength())
        self.lineLayout.addWidget(self.slot3a)
        self.lineLayout.addWidget(QLabel(u'\u2205/'))
        self.slot3b = QLineEdit()
        self.slot3b.setMaxLength(6)
        self.slot3b.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot3b.maxLength() + 1)).width()
        self.slot3b.setFixedWidth(width)
        self.slot3b.setPlaceholderText('_ '*self.slot3b.maxLength())
        self.lineLayout.addWidget(self.slot3b)
        self.lineLayout.addWidget(QLabel(']3'))

        #SLOT 4
        self.lineLayout.addWidget(QLabel('[1'))
        self.slot4 = QLineEdit()
        self.slot4.setMaxLength(3)
        self.slot4.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot4.maxLength() + 1)).width()
        self.slot4.setFixedWidth(width)
        self.slot4.setPlaceholderText('_ '*self.slot4.maxLength())
        self.lineLayout.addWidget(self.slot4)
        self.lineLayout.addWidget(QLabel(']4'))

        #SLOT 5
        self.lineLayout.addWidget(QLabel('['))
        self.slot5a = QLineEdit()
        self.slot5a.setMaxLength(1)
        self.slot5a.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot5a.maxLength() + 1)).width()
        self.slot5a.setFixedWidth(width)
        self.slot5a.setPlaceholderText(('_'*self.slot5a.maxLength()))
        self.lineLayout.addWidget(self.slot5a)
        self.lineLayout.addWidget(QLabel('2'))
        self.slot5b = QLineEdit()
        self.slot5b.setMaxLength(3)
        self.slot5b.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot5b.maxLength() + 1)).width()
        self.slot5b.setFixedWidth(width)
        self.slot5b.setPlaceholderText('_ '*self.slot5b.maxLength())
        self.lineLayout.addWidget(self.slot5b)
        self.lineLayout.addWidget(QLabel(']5'))

        #SLOT 6
        self.lineLayout.addWidget(QLabel('['))
        self.slot6a = QLineEdit()
        self.slot6a.setMaxLength(1)
        self.slot6a.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot6a.maxLength() + 1)).width()
        self.slot6a.setFixedWidth(width)
        self.slot6a.setPlaceholderText('_ '*self.slot6a.maxLength())
        self.lineLayout.addWidget(self.slot6a)
        self.lineLayout.addWidget(QLabel('3'))
        self.slot6b = QLineEdit()
        self.slot6b.setMaxLength(3)
        self.slot6b.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot6b.maxLength() + 1)).width()
        self.slot6b.setFixedWidth(width)
        self.slot6b.setPlaceholderText('_ '*self.slot6b.maxLength())
        self.lineLayout.addWidget(self.slot6b)
        self.lineLayout.addWidget(QLabel(']6'))

        #SLOT 7
        self.lineLayout.addWidget(QLabel('['))
        self.slot7a = QLineEdit()
        self.slot7a.setMaxLength(1)
        self.slot7a.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot7a.maxLength() + 1)).width()
        self.slot7a.setFixedWidth(width)
        self.slot7a.setPlaceholderText('_'*self.slot7a.maxLength())
        self.lineLayout.addWidget(self.slot7a)
        self.lineLayout.addWidget(QLabel('4'))
        self.slot7b = QLineEdit()
        self.slot7b.setMaxLength(3)
        self.slot7b.setFont(defaultFont)
        width = fontMetric.boundingRect('_ ' * (self.slot7b.maxLength() + 1)).width()
        self.slot7b.setFixedWidth(width)
        self.slot7b.setPlaceholderText('_ '*self.slot7b.maxLength())
        self.lineLayout.addWidget(self.slot7b)
        self.lineLayout.addWidget(QLabel(']7'))

        #Update button
        self.updateButton = QPushButton()
        self.updateButton.setText('Update from drop-down boxes')
        self.updateButton.clicked.connect(self.updateFromComboBoxes)
        self.lineLayout.addWidget(self.updateButton)

    def setComboBoxes(self, boxes):
        print(boxes)
        self.indexBox, self.middleBox, self.ringBox, self.pinkBox = boxes

    def updateFromComboBoxes(self):
        indexText = self.indexBox.currentText().replace(',','')
        self.slot4.setText(indexText)
        middleText = self.middleBox.currentText().replace(',','')
        self.slot5a.setText(middleText[0])
        self.slot5b.setText(middleText[1:])
        ringText = self.ringBox.currentText().replace(',','')
        self.slot6a.setText(ringText[0])
        self.slot6b.setText(ringText[1:])
        pinkyText = self.pinkBox.currentText().replace(',','')
        self.slot7a.setText(pinkText[0])
        self.slot7b.setText(pinkyText[1:])

class HandConfigurationNames(QVBoxLayout):

    def __init__(self):
        QVBoxLayout.__init__(self)
        self.addWidget(QLabel('1. Global'))
        self.addWidget(QLabel('2. Thumb'))
        self.addWidget(QLabel('3. Thumb/Finger'))
        self.addWidget(QLabel('4. Index'))
        self.addWidget(QLabel('5. Middle'))
        self.addWidget(QLabel('6. Ring'))
        self.addWidget(QLabel('7. Pinky'))

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
        handNames = HandConfigurationNames()
        handsLayout.addLayout(handNames, 0, 0)
        hand1 = HandShapeLayout(handsLayout, 'Hand 1')
        handsLayout.addLayout(hand1, 0, 1)
        hand2 = SecondHandShapeLayout(handsLayout, 'Hand 2', hand1)
        handsLayout.addLayout(hand2, 0, 2)

        self.gloss.setComboBoxes(hand1.fingerWidgets())

        configLayout = ConfigLayout(1, handsLayout, hand2)
        layout.addLayout(configLayout)

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