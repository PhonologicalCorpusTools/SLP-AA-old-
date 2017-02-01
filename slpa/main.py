import traceback
import itertools
import os
import sys
from enum import Enum
from .imports import *
from .handshapes import *
from .lexicon import Corpus
from .binary import *
from .transcriptions import *
from .settings import Settings
from slpa import __version__ as currentSLPAversion

FONT_NAME = 'Arial'
FONT_SIZE = 12

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
        self.major = QComboBox()
        self.major.addItem('Major Location')
        for location in Locations:
            self.major.addItem(location.name)
        self.major.currentIndexChanged.connect(self.changeMinorLocation)
        self.minor = QComboBox()
        self.minor.addItem('Minor Location')
        self.movement = QComboBox()
        self.movement.addItem('Movement')
        for movement in Movements:
            self.movement.addItem(movement.name)
        self.orientation = QComboBox()
        self.orientation.addItem('Orientation')
        self.addWidget(self.major)
        self.addWidget(self.minor)
        self.addWidget(self.movement)
        self.addWidget(self.orientation)

    def changeMinorLocation(self):
        majorText = self.major.currentText()
        self.minor.clear()
        try:
            minors = Locations[majorText].value
            for location in minors:
                self.minor.addItem(location)
        except KeyError:
            self.minor.addItem('Minor Location')

    def reset(self):
        self.major.setCurrentIndex(0)
        self.movement.setCurrentIndex(0)
        self.orientation.setCurrentIndex(0)

class ConfigLayout(QGridLayout):

    def __init__(self, n, handshapes, hand2):
        QGridLayout.__init__(self)
        self.setSpacing(0)
        self.setContentsMargins(0,0,0,0)

        # self.forearmButton = QCheckBox('1. Forearm')
        # self.addWidget(self.forearmButton, 0, 1)
        self.addLayout(handshapes, 0, 2)
        self.handShapeMatch = QPushButton('Make Hand 2 = Hand 1')
        self.addWidget(self.handShapeMatch, 1, 0)
        self.hand2 = hand2
        self.handShapeMatch.clicked.connect(self.hand2.match)


class HandShapeLayout(QVBoxLayout):

    def __init__(self, parent = None, hand = None, transcription = None):
        QVBoxLayout.__init__(self)#, parent)
        self.handTitle = QLabel(hand)
        self.addWidget(self.handTitle)
        self.transcription = transcription
        self.defineWidgets()
        self.updateButton = QPushButton('Update from transcription')
        self.updateButton.clicked.connect(self.updateFromTranscription)
        self.addWidget(self.updateButton)

    def defineWidgets(self):

        for finger in Fingers:
            setattr(self, finger.name+'Widget', QComboBox())
            w = getattr(self, finger.name+'Widget')
            if finger.features is None:
                w.addItem(finger.name, 'Alternative')
            else:
                for triple in finger.features:
                    triple = ','.join(triple)
                    w.addItem(triple)
            self.addWidget(w)

    def updateFromTranscription(self):
        problems = list()
        indexConfig = self.transcription.slot4.text()
        indexConfig = ','.join(indexConfig)
        search = self.indexWidget.findText(indexConfig)
        if search == -1:
            problems.append('index (slot 4)')
        else:
            self.indexWidget.setCurrentText(indexConfig)

        middleConfig = self.transcription.slot5b.text()
        middleConfig = ','.join(middleConfig)
        search = self.middleWidget.findText(middleConfig)
        if search == -1:
            problems.append('middle (slot 5)')
        else:
            self.middleWidget.setCurrentText(middleConfig)

        ringConfig = self.transcription.slot6b.text()
        ringConfig = ','.join(ringConfig)
        search = self.ringWidget.findText(ringConfig)
        if search == -1:
            problems.append('ring (slot 6)')
        else:
            self.ringWidget.setCurrentText(ringConfig)

        pinkyConfig = self.transcription.slot7b.text()
        pinkyConfig = ','.join(pinkyConfig)
        search = self.pinkyWidget.findText(pinkyConfig)
        if search == -1:
            problems.append('pinky (slot 7)')
        else:
            self.pinkyWidget.setCurrentText(pinkyConfig)

        if problems:
            alert = QMessageBox()
            alert.setWindowTitle('Transcription error')
            alert.setText(('There was a problem trying to update your dropdown boxes for the following fingers on '
                    'the {} hand:\n\n'
                    '{}\n\n'
                    'There are several reasons why this problem may have occured:\n\n'
                    '1.Non-standard symbols\n\n'
                    '2.Impossible combinations\n\n'
                    '3.Blank transcriptions\n\n'
                    'Transcription slots without any problems have been properly updated.'.format(
                                 'second' if isinstance(self, SecondHandShapeLayout) else 'first',
                                 ', '.join(problems))))
            alert.exec_()


    def fingers(self):
        return {'global_Widget': self.global_Widget.currentText(),
                'thumbWidget': self.thumbWidget.currentText(),
                'thumbAndFingerWidget': self.thumbAndFingerWidget.currentText(),
                'indexWidget': self.indexWidget.currentText(),
                'middleWidget': self.middleWidget.currentText(),
                'ringWidget': self.ringWidget.currentText(),
                'pinkyWidget': self.pinkyWidget.currentText()}

    def fingerWidgets(self):
        return [self.indexWidget, self.middleWidget, self.ringWidget, self.pinkyWidget]

class SecondHandShapeLayout(HandShapeLayout):

    def __init__(self, parent = None, hand = None, transcription = None, otherHand = None, otherTranscription = None):
        HandShapeLayout.__init__(self, parent, hand, transcription)
        self.otherHand = otherHand
        self.transcription = transcription
        self.otherTranscription = otherTranscription

    @Slot(bool)
    def match(self, clicked):
        for finger,value in self.otherHand.fingers().items():
            widget = getattr(self, finger)
            widget.setCurrentText(value)

        values = self.otherTranscription.values()
        self.transcription.slot1.setChecked(values[0])
        self.transcription.slot2.setText(values[1])
        self.transcription.slot3a.setText(values[2])
        self.transcription.slot3b.setText(values[3])
        self.transcription.slot4.setText(values[4])
        self.transcription.slot5a.setText(values[5])
        self.transcription.slot5b.setText(values[6])
        self.transcription.slot6a.setText(values[7])
        self.transcription.slot6b.setText(values[8])
        self.transcription.slot7a.setText(values[9])
        self.transcription.slot7b.setText(values[10])


class GlossLayout(QHBoxLayout):
    def __init__(self, parent = None, comboBoxes = None):
        QHBoxLayout.__init__(self)
        defaultFont = QFont(FONT_NAME, FONT_SIZE)
        self.setContentsMargins(-1,-1,-1,0)
        self.glossEdit = QLineEdit()
        self.glossEdit.setFont(defaultFont)
        self.glossEdit.setPlaceholderText('Gloss')
        self.addWidget(self.glossEdit)

class HandConfigurationNames(QVBoxLayout):
    def __init__(self):
        QVBoxLayout.__init__(self)
        self.addWidget(QLabel(''))
        self.addWidget(QLabel('1. Global'))
        self.addWidget(QLabel('2. Thumb'))
        self.addWidget(QLabel('3. Thumb/Finger'))
        self.addWidget(QLabel('4. Index'))
        self.addWidget(QLabel('5. Middle'))
        self.addWidget(QLabel('6. Ring'))
        self.addWidget(QLabel('7. Pinky'))

class HandConfigTab(QWidget):

    def __init__(self, hand_number):
        QWidget.__init__(self)

        self.configLayout = QGridLayout()

        self.hand1Transcription = TranscriptionLayout(hand=1)
        self.configLayout.addLayout(self.hand1Transcription, 0, 0)
        self.hand2Transcription = TranscriptionLayout(hand=2)
        self.configLayout.addLayout(self.hand2Transcription, 1, 0)


        self.setLayout(self.configLayout)

    def clearAll(self):
        self.hand1Transcription.slot1.setChecked(False)
        for slot in self.hand1Transcription.slots[1:]:
            slot.transcription.setText('')

        self.hand2Transcription.slot1.setChecked(False)
        for slot in self.hand2Transcription.slots[1:]:
            slot.transcription.setText('')


class VideoPlayer(QWidget):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        #self.setMedia()
        self.looping = False
        self.videoItem = QGraphicsVideoItem()
        self.videoItem.setSize(QSizeF(640, 480))
        scene = QGraphicsScene(self)
        graphicsView = QGraphicsView(scene)
        scene.addItem(self.videoItem)
        self.layout = QVBoxLayout()
        self.layout.addWidget(graphicsView)
        self.makeButtons()
        self.setLayout(self.layout)
        self.mediaPlayer.setVideoOutput(self.videoItem)

    def makeButtons(self):
        self.buttonLayout = QHBoxLayout()

        self.playButton = QPushButton('Play')
        self.playButton.clicked.connect(self.play)
        self.buttonLayout.addWidget(self.playButton)

        self.loopButton = QPushButton('Loop media')
        self.loopButton.clicked.connect(self.loop)
        self.buttonLayout.addWidget(self.loopButton)

        self.pauseButton = QPushButton('Pause')
        self.pauseButton.clicked.connect(self.pause)
        self.buttonLayout.addWidget(self.pauseButton)

        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(self.stop)
        self.buttonLayout.addWidget(self.stopButton)

        self.changeMediaButton = QPushButton('Change media file')
        self.changeMediaButton.clicked.connect(self.changeMedia)
        self.buttonLayout.addWidget(self.changeMediaButton)

        self.layout.addLayout(self.buttonLayout)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            pass
        else:
            path = getMediaFilePath('reasonable-English.mp4')
            file = QMediaContent(QUrl.fromLocalFile(QFileInfo(path).absoluteFilePath()))
            self.mediaPlayer.setMedia(file)
            self.mediaPlayer.play()

    def setMedia(self):
        path = getMediaFilePath('reasonable-English.mp4')
        file = QMediaContent(QUrl.fromLocalFile(QFileInfo(path).absoluteFilePath()))
        self.mediaPlayer.setMedia(file)

    def pause(self):

        if self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            pass
        elif self.mediaPlayer.state() == QMediaPlayer.PausedState:
            self.pauseButton.setText('Pause')
            self.mediaPlayer.play()
        else:
            self.mediaPlayer.pause()
            self.pauseButton.setText('Unpause')

    def stop(self):
        if self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            pass
        else:
            self.mediaPlayer.stop()

    def loop(self):
        if not self.looping:
            self.looping = True
            self.loopButton.setText('Stop looping')
        else:
            self.looping = False
            self.loopButton.setText('Loop media')

    def changeMedia(self):
        pass

class HandShapeImage(QLabel):

    def __init__(self, path, reversed=False, parent=None):
        super().__init__()
        self.image = QPixmap(path)
        self.isReversed = False
        self.setPixmap(self.image)
        self.mapping = {0: 'hand.png',
                        1: 'hand.png',
                        2: 'hand_thumb_selected.png',
                        3: 'hand_thumb_finger_contact.png',
                        4: 'hand_index_selected.png',
                        5: 'hand_middle_selected.png',
                        6: 'hand_ring_selected.png',
                        7: 'hand_pinky_selected.png'}
        self.reversed_mapping = {n:'reversed_'+self.mapping[n] for n in self.mapping}
        self.mappingChoice = self.mapping

    @Slot(int)
    def transcriptionSlotChanged(self, e):
        self.setPixmap(QPixmap(getMediaFilePath(self.mappingChoice[e])))

    @Slot(bool)
    def useReverseImage(self, e):
        self.mappingChoice = self.reversed_mapping

    @Slot(bool)
    def useNormalImage(self, e):
        self.mappingChoice = self.mapping

class MainWindow(QMainWindow):
    def __init__(self,app):
        app.messageFromOtherInstance.connect(self.handleMessage)
        super(MainWindow, self).__init__()
        self.setWindowTitle('SLP-Annotator')

        self.settings = Settings()

        self.createActions()
        self.createMenus()

        self.wrapper = QWidget()#placeholder for central widget in QMainWindow
        self.corpus = None
        self.globalLayout = QHBoxLayout()
        # self.videoPlayer = VideoPlayer()
        # self.globalLayout.addWidget(self.videoPlayer)

        layout = QVBoxLayout()

        self.saveButton = QPushButton('Add word to corpus')
        layout.addWidget(self.saveButton)

        self.gloss = GlossLayout(parent=self)
        layout.addLayout(self.gloss)

        self.configTabs = QTabWidget()
        self.configTabs.addTab(HandConfigTab(1), 'Config 1')
        self.configTabs.addTab(HandConfigTab(2), 'Config 2')

        layout.addWidget(self.configTabs)

        self.handImage = HandShapeImage(getMediaFilePath('hand.png'))
        layout.addWidget(self.handImage)

        # for k in [0,1]:
        #     for slot in self.configTabs.widget(k).hand1Transcription.fields[1:]:
        #         #slot = getattr(self.configTabs.widget(k).hand1Transcription, slot_id)
        #         field.transcription.slotSelectionChanged.connect(self.handImage.useNormalImage)
        #         field.transcription.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)
        #     for slot in self.configTabs.widget(k).hand2Transcription.fields[1:]:
        #         #slot = getattr(self.configTabs.widget(k).hand2Transcription, slot_id)
        #         field.transcription.slotSelectionChanged.connect(self.handImage.useReverseImage)
        #         field.transcription.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)

        self.featuresLayout = MajorFeatureLayout()
        layout.addLayout(self.featuresLayout)

        self.globalLayout.addLayout(layout)

        self.wrapper.setLayout(self.globalLayout)
        self.setCentralWidget(self.wrapper)

        self.saveButton.clicked.connect(self.saveCorpus)

        self.makeCorpusDock()

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())


    def makeCorpusDock(self):
        self.corpusDock = QDockWidget()
        self.corpusDock.setWindowTitle('Corpus')
        self.corpusDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.corpusDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dockWrapper = QWidget()
        self.dockLayout = QVBoxLayout()
        self.dockWrapper.setLayout(self.dockLayout)
        self.corpusDock.setWidget(self.dockWrapper)
        self.addDockWidget(Qt.RightDockWidgetArea, self.corpusDock)

    def loadCorpus(self):
        file_path = QFileDialog.getOpenFileName(self,
                'Open Corpus File', os.getcwd(), '*.corpus')
        print(file_path)
        file_path = file_path[0]
        if not file_path:
            return
        self.clearLayout(self.dockLayout)
        self.newGloss(giveWarning=False)
        self.corpus = load_binary(file_path)
        for sign in self.corpus:
            data = sign.data()
            self.addButtonToDock(data)


    def saveCorpus(self):
        if not self.gloss.glossEdit.text():
            alert = QMessageBox()
            alert.setWindowTitle('Missing gloss')
            alert.setText('Please enter a gloss before saving')
            alert.exec_()
            return

        if self.corpus is None:
            kwargs = self.generateKwargs()
            alert = QMessageBox()
            alert.setWindowTitle('No corpus loaded')
            alert.setText('You must have a corpus loaded before you can save words. What would you like to do?')
            alert.addButton('Add this word to an existing corpus', QMessageBox.AcceptRole)
            alert.addButton('Create a new corpus', QMessageBox.RejectRole)
            alert.exec_()
            role = alert.buttonRole(alert.clickedButton())
            if role ==  1:#create new corpus
                savename = QFileDialog.getSaveFileName(self, 'Save Corpus File', os.getcwd(), '*.corpus')

                path = savename[0]
                if not path:
                    return
                if not path.endswith('.corpus'):
                    path = path + '.corpus'
                kwargs['file_mode'] = 'w'
                kwargs['path'] = path
                kwargs['name'] = os.path.split(path)[1].split('.')[0]
                self.corpus = Corpus(kwargs)
                #saveHandShape(kwargs)
                self.addButtonToDock(kwargs)
                self.corpus.addWord(Sign(kwargs))
                save_binary(self.corpus,
                            #os.path.join(self.settings['storage'], 'CORPUS', self.corpus.name + '.corpus'))
                            kwargs['path'])
                QMessageBox.information(self, 'Success', 'Corpus successfully updated!')
                #self.newGloss()

            elif role == 0: #load existing corpus and add to it
                self.loadCorpus()
                self.addButtonToDock(kwargs)
                self.corpus.addWord(Sign(kwargs))
                save_binary(self.corpus,
                            #os.path.join(self.settings['storage'], 'CORPUS', self.corpus.name + '.corpus'))
                            kwargs['path'])

        else: #corpus exists
            kwargs = self.generateKwargs()
            kwargs['path'] = self.corpus.path
            kwargs['file_mode'] = 'a'
            if kwargs['gloss'] in self.corpus.wordlist:
                alert = QMessageBox()
                alert.setWindowTitle('Duplicate entry')
                alert.setText('A word with the gloss {} already exists in your corpus. '
                                'What do you want to do?'.format(kwargs['gloss']))
                alert.addButton('Overwrite exising word', QMessageBox.AcceptRole)
                alert.addButton('Go back and edit the gloss', QMessageBox.RejectRole)
                alert.exec_()
                role = alert.buttonRole(alert.clickedButton())
                if role == 0:#overwrite
                    pass
                elif role == 1:#edit
                    return

            #saveHandShape(kwargs)
            self.addButtonToDock(kwargs)
            self.corpus.addWord(Sign(kwargs))
            QMessageBox.information(self, 'Success', 'Corpus successfully updated!')
            #self.newGloss()

    def addButtonToDock(self, kwargs):
        button = DataButton(kwargs)
        button.sendData.connect(self.loadHandShape)
        self.corpusDock.widget().layout().addWidget(button)

    def newCorpus(self):
        self.corpus = None
        self.newGloss()
        self.clearLayout(self.dockLayout)

    def loadHandShape(self, buttonData):

        self.gloss.glossEdit.setText(buttonData['gloss'])
        config1 = self.configTabs.widget(0)
        config2 = self.configTabs.widget(1)

        config1hand1 = buttonData['config1hand1']
        config1.hand1Transcription.slot1.setChecked(config1hand1.slot1)
        for slot in config1hand1.slots[1:]:
            slot.transcription.setText(value)

        config1hand2 = buttonData['config1hand2']
        config1.hand2Transcription.slot1.setChecked(config1hand2.slot1)
        for slot in config1hand2.slots[1:]:
            slot.transcription.setText(value)

        config2hand1 = buttonData['config2hand1']
        config2.hand2Transcription.slot1.setChecked(config2hand1.slot1)
        for slot in config2hand1.slots[1:]:
            slot.transcription.setText(value)

        config2hand2 = buttonData['config2hand2']
        config2.hand2Transcription.slot1.setChecked(config2hand2.slot1)
        for slot in config2hand2.slots[1:]:
            slot.transcription.setText(value)

        for name in ['major', 'minor', 'movement', 'orientation']:
            widget = getattr(self.featuresLayout, name)
            index = widget.findText(buttonData[name])
            if index == -1:
                index = 0
            widget.setCurrentIndex(index)

    def generateSign(self):
        data = {'config1': None, 'config2': None,
                'major': None, 'minor': None, 'movement': None, 'orientation': None}
        data['config1'] = self.configTabs.widget(0).findChildren(TranscriptionLayout)
        data['config2'] = self.configTabs.widget(1).findChildren(TranscriptionLayout)
        gloss = self.gloss.glossEdit.text().strip()
        data['gloss'] = gloss
        major = self.featuresLayout.major.currentText()
        data['major'] = 'None' if major == 'Major Location' else major
        minor = self.featuresLayout.minor.currentText()
        data['minor'] = 'None' if minor == 'Minor Location' else minor
        movement = self.featuresLayout.movement.currentText()
        data['movement'] = 'None' if movement == 'Movement' else movement
        orientation = self.featuresLayout.orientation.currentText()
        data['orientation'] = 'None' if orientation == 'Orientation' else orientation
        return Sign(data)

    def generateKwargs(self):
        kwargs = {'path': None, 'file_mode': None,
                'config1': None, 'config2': None,
                'major': None, 'minor': None, 'movement': None, 'orientation': None}
        kwargs['config1'] = self.configTabs.widget(0).findChildren(TranscriptionLayout)
        kwargs['config2'] = self.configTabs.widget(1).findChildren(TranscriptionLayout)
        gloss = self.gloss.glossEdit.text().strip()
        kwargs['gloss'] = gloss
        major = self.featuresLayout.major.currentText()
        kwargs['major'] = 'None' if major == 'Major Location' else major
        minor = self.featuresLayout.minor.currentText()
        kwargs['minor'] = 'None' if minor == 'Minor Location' else minor
        movement = self.featuresLayout.movement.currentText()
        kwargs['movement'] = 'None' if movement == 'Movement' else movement
        orientation = self.featuresLayout.orientation.currentText()
        kwargs['orientation'] = 'None' if orientation == 'Orientation' else orientation
        return kwargs

    def printCorpusToConsole(self):
        print(self.corpus.name, len(self.corpus))
        for word in self.corpus:
            print(word.gloss)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&Menu")
        self.fileMenu.addAction(self.newCorpusAct)
        self.fileMenu.addAction(self.loadCorpusAct)
        self.fileMenu.addAction(self.saveCorpusAct)
        self.fileMenu.addAction(self.newGlossAct)
        self.fileMenu.addAction(self.printCorpusToConsoleAct)
        self.fileMenu.addAction(self.quitAct)

    def createActions(self):

        self.printCorpusToConsoleAct = QAction('Print corpus to console', self, triggered=self.printCorpusToConsole)

        self.newCorpusAct = QAction('&New corpus...',
                                    self,
                                    statusTip="Start a new corpus", triggered = self.newCorpus)

        self.loadCorpusAct = QAction( "&Load corpus...",
                self,
                statusTip="Load a corpus", triggered=self.loadCorpus)

        self.saveCorpusAct = QAction( "&Save corpus...",
                self,
                statusTip="Save a corpus", triggered=self.saveCorpus)

        self.newGlossAct = QAction('&New gloss',
                self,
                statusTip='Clear current info and make a new gloss',
                triggered=self.newGloss)

        self.quitAct = QAction( "&Quit",
                self,
                statusTip="Quit", triggered=self.close)


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
        self.activateWindow()

    def cleanUp(self):
        # Clean up everything
        for i in self.__dict__:
            item = self.__dict__[i]
            clean(item)

    def newGloss(self, giveWarning=True):
        if giveWarning:
            alert = QMessageBox()
            alert.setWindowTitle('Warning')
            alert.setText('This will erase the information for the current word, '
                          'and you will lose any unsaved changes.\n What would you like to do?')
            alert.addButton('Continue without saving', QMessageBox.AcceptRole)
            alert.addButton('Go back', QMessageBox.RejectRole)
            alert.exec_()
            role = alert.buttonRole(alert.clickedButton())
            if role == 0:#AcceptRole:
                pass
            elif role == 1:#RejectRole
                return
        self.gloss.glossEdit.setText('')
        self.configTabs.widget(0).clearAll()
        self.configTabs.widget(1).clearAll()
        self.featuresLayout.reset()


class DataButton(QPushButton):

    sendData = Signal(dict)
    def __init__(self, data):
        QPushButton.__init__(self)
        self.gloss = data['gloss']
        self.setText(self.gloss)
        self.config1 = data['config1']
        self.parseConfiguration(self.config1, '1')
        self.config2 = data['config2']
        self.parseConfiguration(self.config2, '2')
        self.major = data['major']
        self.minor = data['minor']
        self.movement = data['movement']
        self.orientation = data['orientation']
        self.setData()
        self.clicked.connect(self.emitData)

    def parseConfiguration(self, config, num):
        hand1,hand2 = config
        info = str(hand1).split(';')
        setattr(self, 'config'+num+'hand1', TranscriptionData(info))
        info = str(hand2).split(';')
        setattr(self, 'config'+num+'hand2', TranscriptionData(info))

    def setData(self):
        self.data ={'major': self.major, 'minor': self.minor,
                    'movement':self.movement, 'orientation': self.orientation,
                    'config1hand1': self.config1hand1, 'config1hand2': self.config1hand2,
                    'config2hand1': self.config2hand1, 'config2hand2': self.config2hand2,
                    'gloss': self.gloss}

    def emitData(self):
        self.sendData.emit(self.data)



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

def sortData(data):
    if data == 'gloss':
        return 0
    elif data == 'config1':
        return 1
    elif data == 'config2':
        return 2
    elif data == 'major':
        return 3
    elif data == 'minor':
        return 4
    elif data == 'movement':
        return 5
    elif data == 'orientation':
        return 6

def saveHandShape(kwargs):
    #see MainWindow.generateKwargs() for where this data comes from in the first place
    path = kwargs.pop('path')
    file_mode = kwargs.pop('file_mode')
    kwargs['config1'] = '&'.join([str(kw) for kw in kwargs['config1']])
    kwargs['config2'] = '&'.join([str(kw) for kw in kwargs['config2']])
    headers = sorted(list(kwargs.keys()), key=sortData)

    with open(path, mode=file_mode, encoding='utf-8') as file:
        if file_mode == 'w':
            print(','.join(headers), file=file)
        line = list()
        for header in headers:
            value = kwargs[header]
            #print(header, value)
            if value is None:
                line.append('None')
            else:
                line.append(str(value))
        line = ','.join(line)
        print(line, file=file)

def loadcsvCorpus(path):
    with open(path, mode='r', encoding='utf-8') as file:
        headers = file.readline().strip().split(',')
        for line in file:
            line = line.split(',')
            data = {headers[n]: line[n] for n in range(len(headers))}
            button = DataButton(data)
            button.sendData.connect(self.loadHandShape)
            self.corpusDock.widget().layout().addWidget(button)

def getMediaFilePath(filename):
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', filename)
    return path