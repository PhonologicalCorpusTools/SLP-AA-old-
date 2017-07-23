import traceback
import itertools
import os
import sys
import subprocess
import collections
import parameters
import decorators
from imports import *
from handshapes import *
from lexicon import *
from binary import *
from transcriptions import *
from constraints import *
from constraintwidgets import *
from notes import *
from parameterwidgets import ParameterDialog, ParameterTreeModel
import anytree
#from slpa import __version__ as currentSLPAversion

__currentSLPAversion__ = 0.1
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

class GlossLayout(QHBoxLayout):
    def __init__(self, parent = None, comboBoxes = None):
        QHBoxLayout.__init__(self)
        defaultFont = QFont(FONT_NAME, FONT_SIZE)
        self.setContentsMargins(-1,-1,-1,0)
        self.glossEdit = QLineEdit()
        self.glossEdit.setFont(defaultFont)
        self.glossEdit.setPlaceholderText('Gloss')
        self.addWidget(self.glossEdit)

    def text(self):
        return self.glossEdit.text()

    def setText(self, newText):
        self.glossEdit.setText(newText)

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

    def clearAll(self, clearFlags=False):
        self.hand1Transcription.clearTranscriptionSlots()
        self.hand1Transcription.clearViolationLabels()
        self.hand1Transcription.fillPredeterminedSlots()

        self.hand2Transcription.clearTranscriptionSlots()
        self.hand2Transcription.clearViolationLabels()
        self.hand2Transcription.fillPredeterminedSlots()

        if clearFlags:
            for n in range(2,35):
                slot = 'slot{}'.format(n)
                getattr(self.hand1Transcription, slot).removeFlags()
                getattr(self.hand2Transcription, slot).removeFlags()

    def hand1(self):
        return self.hand1Transcription.values()

    def hand2(self):
        return self.hand2Transcription.values()

    def hands(self):
        return [self.hand1(), self.hand2()]


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
        file_name = 'hand_slot{}.png'.format(e)
        self.setPixmap(QPixmap(getMediaFilePath(file_name)))

    @Slot(int)
    def useReverseImage(self, e):
        self.mappingChoice = self.reversed_mapping

    @Slot(int)
    def useNormalImage(self, e):
        self.mappingChoice = self.mapping

class BlenderOutputWindow(QDialog):

    def __init__(self, image_name, gloss):
        super().__init__()
        self.setModal(False)
        title = gloss if gloss else 'Transcription visualization'
        self.setWindowTitle(title)
        self.image = QPixmap(getMediaFilePath(image_name))
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.image)
        layout = QHBoxLayout()
        layout.addWidget(self.imageLabel)
        self.setLayout(layout)

class CorpusList(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def mousePressEvent(self, event):
        originalItem =  [i for i in self.selectedItems()][0]
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            if self.parent.autoSave:
                self.parent.saveCorpus(checkForDuplicates=False)
                selectedItem = [i for i in self.selectedItems()][0]
                self.itemClicked.emit(selectedItem)
            elif self.parent.askSaveChanges:
                alert = QMessageBox()
                alert.setWindowTitle('Warning')
                alert.setText('There are unsaved changes to your current entry. What do you want to do?')
                alert.addButton('Continue and save', QMessageBox.YesRole)
                alert.addButton('Continue but don\'t save', QMessageBox.NoRole)
                alert.addButton('Go back', QMessageBox.RejectRole)
                result = alert.exec_()
                if alert.buttonRole(alert.clickedButton()) == QMessageBox.YesRole: #continue and save
                    self.parent.saveCorpus(checkForDuplicates=False)
                    selectedItem = [i for i in self.selectedItems()][0]
                    self.itemClicked.emit(selectedItem)

                elif alert.buttonRole(alert.clickedButton()) == QMessageBox.NoRole:# continue but don't save
                    selectedItem = [i for i in self.selectedItems()][0]
                    self.itemClicked.emit(selectedItem)

                elif alert.buttonRole(alert.clickedButton()) == QMessageBox.RejectRole: #go back and edit the gloss
                    self.setCurrentItem(originalItem)
                    self.itemClicked.emit(originalItem)

class MainWindow(QMainWindow):
    transcriptionRestrictionsChanged = Signal(bool)

    def __init__(self,app):
        app.messageFromOtherInstance.connect(self.handleMessage)
        super(MainWindow, self).__init__()
        self.setWindowTitle('SLP-Annotator')
        self.setWindowIcon(QIcon(getMediaFilePath('slpa_icon.png')))

        #Set "global" variables
        self.askSaveChanges = False
        self.constraints = dict()
        self.clipboard = list()
        self.createActions()
        self.createMenus()
        self.readSettings()

        self.wrapper = QWidget()#placeholder for central widget in QMainWindow
        self.corpus = None
        self.globalLayout = QHBoxLayout()

        #Make video player
        # self.videoPlayer = VideoPlayer()
        # self.globalLayout.addWidget(self.videoPlayer)

        layout = QVBoxLayout()
        topLayout = QHBoxLayout()

        #New gloss button
        self.newGlossButton = QPushButton('New gloss')
        self.newGlossButton.clicked.connect(lambda: self.newGloss(clearFlags=True))
        topLayout.addWidget(self.newGlossButton)

        #Make save button
        self.saveButton = QPushButton('Save word to corpus')
        self.saveButton.clicked.connect(self.saveCorpus)
        topLayout.addWidget(self.saveButton)

        #Make delete button
        self.deleteButton = QPushButton('Delete word from corpus')
        self.deleteButton.clicked.connect(self.deleteFromCorpus)
        topLayout.addWidget(self.deleteButton)

        # Make "check transcription" button
        self.checkTranscriptionButton = QPushButton('Check transcription')
        self.checkTranscriptionButton.clicked.connect(self.checkTranscription)
        topLayout.addWidget(self.checkTranscriptionButton)

        # Render handshape in Blender
        self.openBlenderButton = QPushButton('Visualize transcription')
        self.openBlenderButton.clicked.connect(self.launchBlender)
        topLayout.addWidget(self.openBlenderButton)

        # Copy and paste transcriptions
        self.copyButton = QPushButton('Copy')
        self.pasteButton = QPushButton('Paste')
        self.copyButton.clicked.connect(self.copyTranscription)
        self.pasteButton.clicked.connect(self.pasteTranscription)
        topLayout.addWidget(self.copyButton)
        topLayout.addWidget(self.pasteButton)

        #Add parameters button
        paramButton = QPushButton('View Parameters')
        paramButton.clicked.connect(self.showParameterTree)
        topLayout.addWidget(paramButton)

        layout.addLayout(topLayout)

        #Make gloss entry
        self.gloss = GlossLayout(parent=self)
        self.gloss.glossEdit.textChanged.connect(self.userMadeChanges)
        layout.addLayout(self.gloss)

        #Make tabs for each configuration
        self.configTabs = QTabWidget()
        self.configTabs.addTab(HandConfigTab(1), 'Config 1')
        self.configTabs.addTab(HandConfigTab(2), 'Config 2')
        layout.addWidget(self.configTabs)

        #Add "global" handshape options (as checkboxes)
        self.globalOptionsLayout = QHBoxLayout()
        self.setupGlobalOptions()
        layout.addLayout(self.globalOptionsLayout)

        #Make hand image and accompanying info
        self.infoPanel = QHBoxLayout()
        self.handImage = HandShapeImage(getMediaFilePath('hand.png'))
        self.infoPanel.addWidget(self.handImage)
        self.transcriptionInfo = TranscriptionInfo()
        self.infoPanel.addLayout(self.transcriptionInfo)
        layout.addLayout(self.infoPanel)


        #Connect transcription signals to various main window slots
        for k in [0,1]:
            self.configTabs.widget(k).hand1Transcription.slots[0].stateChanged.connect(self.userMadeChanges)
            for slot in self.configTabs.widget(k).hand1Transcription.slots[1:]:
                slot.slotSelectionChanged.connect(self.handImage.useNormalImage)
                slot.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)
                slot.slotSelectionChanged.connect(self.transcriptionInfo.transcriptionSlotChanged)
                slot.textChanged.connect(self.userMadeChanges)
                slot.slotFlagged.connect(self.userMadeChanges)
                self.transcriptionRestrictionsChanged.connect(slot.changeValidatorState)

            self.configTabs.widget(k).hand2Transcription.slots[0].stateChanged.connect(self.userMadeChanges)
            for slot in self.configTabs.widget(k).hand2Transcription.slots[1:]:
                slot.slotSelectionChanged.connect(self.handImage.useReverseImage)
                slot.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)
                slot.slotSelectionChanged.connect(self.transcriptionInfo.transcriptionSlotChanged)
                slot.textChanged.connect(self.userMadeChanges)
                slot.slotFlagged.connect(self.userMadeChanges)
                self.transcriptionRestrictionsChanged.connect(slot.changeValidatorState)

        self.globalLayout.addLayout(layout)

        self.wrapper.setLayout(self.globalLayout)
        self.setCentralWidget(self.wrapper)

        self.parameterDialog = None
        self.setupParameterDialog(ParameterTreeModel(parameters.defaultParameters))
        self.initCorpusNotes()
        self.initSignNotes()
        self.makeCorpusDock()

        self.showMaximized()
        self.defineTabOrder()

    def setGloss(self, text):
        self.gloss.glossEdit.setText(text)

    def setBlenderPath(self):
        dialog = BlenderPathDialog(self.blenderPath)
        dialog.exec_()
        if dialog.file_path is None:
            self.blenderPath = None
        else:
            self.blenderPath = os.path.dirname(dialog.file_path)

    def deleteFromCorpus(self):
        hs = self.currentHandShape()
        gloss = hs.gloss
        if self.corpus is None or hs is None or not gloss in self.corpus:
            alert = QMessageBox()
            alert.setWindowTitle('Error')
            alert.setText('The current word has not been saved to the corpus yet, so it cannot be deleted. If you '
                          'want to clear the main window, click on "New Gloss".')
            alert.exec_()
        else:
            del self.corpus.wordlist[gloss]
            for n in range(self.corpusList.count()):
                item = self.corpusList.item(n)
                if item.text() == gloss:
                    goodbye = self.corpusList.takeItem(n)
                    del goodbye
                    break
            self.newGloss()


    def setupGlobalOptions(self):
        globalOptionsLabel = QLabel('Global handshape options:')
        globalOptionsLabel.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(globalOptionsLabel)
        self.forearmCheckBox = QCheckBox('Forearm is involved')
        self.forearmCheckBox.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(self.forearmCheckBox)
        self.forearmCheckBox.clicked.connect(self.userMadeChanges)
        self.partialObscurityCheckBox = QCheckBox('This sign is partially obscured')
        self.partialObscurityCheckBox.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.partialObscurityCheckBox.clicked.connect(self.userMadeChanges)
        self.globalOptionsLayout.addWidget(self.partialObscurityCheckBox)
        self.uncertainCodingCheckBox = QCheckBox('The coding for this sign is uncertain')
        self.uncertainCodingCheckBox.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.uncertainCodingCheckBox.clicked.connect(self.userMadeChanges)
        self.globalOptionsLayout.addWidget(self.uncertainCodingCheckBox)
        self.incompleteCodingCheckBox = QCheckBox('The coding for this sign is incomplete')
        self.incompleteCodingCheckBox.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.incompleteCodingCheckBox.clicked.connect(self.userMadeChanges)
        self.globalOptionsLayout.addWidget(self.incompleteCodingCheckBox)
        self.globalOptionsWidgets = [self.forearmCheckBox,
                                     self.partialObscurityCheckBox,
                                     self.uncertainCodingCheckBox,
                                     self.incompleteCodingCheckBox]

    def setupParameterDialog(self, model):
        if self.parameterDialog is None:
            model = ParameterTreeModel(parameters.defaultParameters)
            self.parameterDialog = ParameterDialog(model)
            self.parameterDialog.treeWidget.resetChecks()
        else:
            self.parameterDialog.close()
            self.parameterDialog.deleteLater()
            if self.currentHandShape() is not None:
                model = self.currentHandShape().parameters
                self.parameterDialog = ParameterDialog(model, checkStrategy='load')
                #self.parameterDialog.treeWidget.loadChecks()
            else:
                model = ParameterTreeModel(parameters.defaultParameters)
                self.parameterDialog = ParameterDialog(model)
                self.parameterDialog.treeWidget.resetChecks()


    def currentHandShape(self):
        kwargs = self.generateKwargs()
        sign = Sign(kwargs)
        return sign

    def currentGloss(self):
        return self.gloss.glossEdit.text()

    def showParameterTree(self):
        self.parameterDialog.resize(self.parameterDialog.adjustedWidth, self.parameterDialog.adjustedHeight)
        self.parameterDialog.move(self.parameterDialog.adjustedPos)
        self.parameterDialog.show()

    def keyPressEvent(self, e):
        key = e.key()
        modifiers = e.modifiers()
        if (key == Qt.Key_C) and (modifiers == Qt.ControlModifier):
            self.copyTranscription()
        elif (key == Qt.Key_V) and (modifiers == Qt.ControlModifier):
            self.pasteTranscription()
        else:
            super().keyPressEvent(e)

    def copyTranscription(self):
        transcriptions = list()
        transcriptions.append(self.configTabs.widget(0).hand1Transcription)
        transcriptions.append(self.configTabs.widget(0).hand2Transcription)
        transcriptions.append(self.configTabs.widget(1).hand1Transcription)
        transcriptions.append(self.configTabs.widget(1).hand2Transcription)
        dialog = TranscriptionSelectDialog(transcriptions, mode='copy')
        result = dialog.exec_()
        if result:
            self.clipboard = dialog.selectedTranscription

    def pasteTranscription(self):
        if not self.clipboard:
            alert = QMessageBox()
            alert.setWindowTitle('Error')
            alert.setText('Your transcription clipboard is currently empty. You need to copy a transcription before '
                          'you can paste one.')
            alert.exec_()
            return
        transcriptions = list()
        transcriptions.append(self.configTabs.widget(0).hand1Transcription)
        transcriptions.append(self.configTabs.widget(0).hand2Transcription)
        transcriptions.append(self.configTabs.widget(1).hand1Transcription)
        transcriptions.append(self.configTabs.widget(1).hand2Transcription)
        dialog = TranscriptionPasteDialog(self.clipboard, transcriptions)
        result = dialog.exec_()
        if result:
            if dialog.transcriptionID == 0:
                self.configTabs.widget(0).hand1Transcription.updateFromCopy(self.clipboard)
            elif dialog.transcriptionID == 1:
                self.configTabs.widget(0).hand2Transcription.updateFromCopy(self.clipboard)
            if dialog.transcriptionID == 2:
                self.configTabs.widget(1).hand1Transcription.updateFromCopy(self.clipboard)
            if dialog.transcriptionID == 3:
                self.configTabs.widget(1).hand2Transcription.updateFromCopy(self.clipboard)

    def userMadeChanges(self, e):
        self.askSaveChanges = True

    def defineTabOrder(self):
        self.setTabOrder(self.saveButton, self.checkTranscriptionButton)
        self.setTabOrder(self.checkTranscriptionButton, self.gloss.glossEdit)
        self.setTabOrder(self.gloss.glossEdit, self.configTabs.widget(0))
        self.setTabOrder(self.configTabs.widget(0), self.configTabs.widget(0).hand1Transcription[0])
        for k in range(1,35):
            try:
                self.setTabOrder(self.configTabs.widget(0).hand1Transcription[k],
                                 self.configTabs.widget(0).hand1Transcription[k+1])
            except IndexError:
                pass
        self.setTabOrder(self.configTabs.widget(0).hand1Transcription[-2],
                         self.configTabs.widget(0).hand1Transcription[-1])
        self.setTabOrder(self.configTabs.widget(0).hand1Transcription[-1],
                         self.configTabs.widget(0).hand2Transcription[0])
        for k in range(1,35):
            try:
                self.setTabOrder(self.configTabs.widget(0).hand2Transcription[k],
                                 self.configTabs.widget(0).hand2Transcription[k+1])
            except IndexError:
                pass
        self.setTabOrder(self.configTabs.widget(0).hand2Transcription[-2],
                         self.configTabs.widget(0).hand2Transcription[-1])
        self.setTabOrder(self.configTabs.widget(0).hand2Transcription[-1],
                         self.configTabs.widget(1))
        self.setTabOrder(self.configTabs.widget(1),
                         self.configTabs.widget(1).hand1Transcription[0])
        for k in range(1,35):
            try:
                self.setTabOrder(self.configTabs.widget(1).hand1Transcription[k],
                         self.configTabs.widget(1).hand1Transcription[k+1])
            except IndexError:
                pass
        self.setTabOrder(self.configTabs.widget(1).hand1Transcription[-2],
                         self.configTabs.widget(1).hand1Transcription[-1])
        self.setTabOrder(self.configTabs.widget(1).hand1Transcription[-1],
                         self.configTabs.widget(1).hand2Transcription[0])
        for k in range(1,35):
            try:
                self.setTabOrder(self.configTabs.widget(1).hand2Transcription[k],
                                self.configTabs.widget(1).hand2Transcription[k+1])
            except IndexError:
                pass
        self.setTabOrder(self.configTabs.widget(1).hand2Transcription[-2],
                         self.configTabs.widget(1).hand2Transcription[-1])

    def writeSettings(self):
        self.settings = QSettings('UBC Phonology Tools', application='SLP-Annotator')
        self.settings.beginGroup('constraints')
        for c in MasterConstraintList:
            name = c[0]
            self.settings.setValue(name, self.constraints[name])
        self.settings.endGroup()

        self.settings.beginGroup('parameters')
        self.settings.setValue('parameters', self.parameters)
        self.settings.endGroup()

        self.settings.beginGroup('options')
        self.settings.setValue('askAboutDuplicates', self.askAboutDuplicatesAct.isChecked())
        self.settings.setValue('showSaveAlert', self.alertOnCorpusSaveAct.isChecked())
        self.settings.setValue('parametersAlwaysOnTop', self.keepParametersOnTopAct.isChecked())
        self.settings.setValue('restrictedTranscriptions', self.setRestrictionsAct.isChecked())
        self.settings.setValue('autoSave', self.autoSaveAct.isChecked())
        self.settings.setValue('blenderPath', self.blenderPath)
        self.settings.endGroup()

    def readSettings(self, reset=False):
        self.settings = QSettings('UBC Phonology Tools', application='SLP-Annotator')
        if reset:
            self.settings.clear()

        self.settings.beginGroup('constraints')
        for c in MasterConstraintList:
            name = c[0]
            self.constraints[name] = self.settings.value(name, type=bool)
        self.settings.endGroup()

        self.settings.beginGroup('parameters')
        self.parameters = self.settings.value('parameters', defaultValue=parameters.defaultParameters)
        self.settings.endGroup()

        self.settings.beginGroup('options')
        self.showDuplicateWarning = self.settings.value('showDuplicateWarning', defaultValue=True, type=bool)
        self.askAboutDuplicatesAct.setChecked(self.showDuplicateWarning)
        self.showSaveAlert = self.settings.value('showSaveAlert', defaultValue=True, type=bool)
        self.alertOnCorpusSaveAct.setChecked(self.showSaveAlert)
        self.parametersAlwaysOnTop = self.settings.value('parametersAlwaysOnTop', defaultValue=True, type=bool)
        self.keepParametersOnTopAct.setChecked(self.parametersAlwaysOnTop)
        self.restrictedTranscriptions = self.settings.value('restrictedTranscriptions', type=bool)
        self.setRestrictionsAct.setChecked(self.restrictedTranscriptions)
        self.transcriptionRestrictionsChanged.emit(self.restrictedTranscriptions)
        self.autoSave = self.settings.value('autosave', type=bool)
        self.autoSaveAct.setChecked(self.autoSave)
        self.blenderPath = self.settings.value('blenderPath')
        self.settings.endGroup()

    @decorators.checkForUnsavedChanges
    def closeEvent(self, e):
        self.writeSettings()
        try:
            os.remove(os.path.join(os.getcwd(),'handCode.txt'))
        except FileNotFoundError:
            pass
        #super().closeEvent(QCloseEvent())
        self.close()

    def copyCorpus(self, path):
        newCorpus = Corpus({})
        for word in self.corpus:
            word.flags = Sign.sign_attributes['flags'].copy()
            newCorpus.addWord(word)
        newCorpus.path = path
        save_binary(newCorpus, newCorpus.path)
        self.corpus =  load_binary(newCorpus.path)


    def checkBackwardsComptibility(self):

        for attribute, default_value in Corpus.corpus_attributes.items():
            if not hasattr(self.corpus, attribute):
                setattr(self.corpus, attribute, Corpus.copyValue(Corpus, default_value))

        word = self.corpus.randomWord()
        for attribute, default_value in Sign.sign_attributes.items():
            if not hasattr(word, attribute):
                break
        else:
            return

        for word in self.corpus:
            for attribute, default_value in Sign.sign_attributes.items():
                if not hasattr(word, attribute):
                    setattr(word, attribute, Sign.copyValue(Sign, default_value))
                # if attribute == 'parameters' and not isinstance(getattr(word, attribute), anytree.Node):
                #     setattr(word, attribute, default_value)

            if hasattr(word, 'movement'):
                setattr(word, 'oneHandMovement', word.movement)
                del word.movement

        #self.corpus.path = self.getOrCreateCorpusPath()
        save_binary(self.corpus, self.corpus.path)
        self.corpus = load_binary(self.corpus.path)

    def getOrCreateCorpusPath(self):
        if os.path.exists(self.corpus.path):
            return self.corpus.path
        else:
            return os.path.join(os.getcwd(), self.corpus.name)

    def checkTranscription(self):
        dialog = ConstraintCheckMessageBox(self.constraints, self.configTabs)
        dialog.exec_()

        if not dialog.violations:
            return

        for j in [1,2]:
            for k in [1,2]:
                transcription = getattr(self.configTabs.widget(j - 1), 'hand{}Transcription'.format(k))
                results = [(s,v) for (s,v) in dialog.violations['config{}hand{}'.format(j,k)].items() if v]
                slots = [x[0] for x in results]
                violations = [x[1] for x in results]
                tooltips = collections.defaultdict(set)
                for slot in transcription.slots:
                    n = slot.num
                    violationLabel = getattr(transcription, 'violation{}'.format(n))
                    if n in slots:
                        violationLabel.setText('   *')
                        violation_names = violations[slots.index(slot.num)]
                        tooltips[slot.num].update(violation_names)
                    else:
                        violationLabel.setText(' ')
                        violationLabel.setToolTip('')

                for slot in tooltips:
                    violationLabel = getattr(transcription, 'violation{}'.format(slot))
                    tip = ['Slot {}'.format(slot)]
                    tip.extend(sorted(tooltips[slot]))
                    violationLabel.setToolTip('\n'.join(tip))
        return

    def launchBlender(self):

        transcriptions = list()
        transcriptions.append(self.configTabs.widget(0).hand1Transcription)
        transcriptions.append(self.configTabs.widget(0).hand2Transcription)
        transcriptions.append(self.configTabs.widget(1).hand1Transcription)
        transcriptions.append(self.configTabs.widget(1).hand2Transcription)
        dialog = TranscriptionSelectDialog(transcriptions, mode='blender')
        dialog.exec_()
        if not dialog.selectedTranscription:
            return

        if self.blenderPath is not None:
            blenderPath = os.path.join(self.blenderPath, 'blender.exe')
            blenderPlayerPath = os.path.join(self.blenderPath, 'blenderplayer.exe')
            if os.path.exists(blenderPath):
                foundPath = True
            else:
                foundPath = False
        else:
            foundPath = False
            if os.path.exists(r'C:\Program Files\Blender Foundation\Blender\blender.exe'):
                blenderPath = r'C:\Program Files\Blender Foundation\Blender\blender.exe'
                blenderPlayerPath = r'C:\Program Files\Blender Foundation\Blender\blenderplayer.exe'
                foundPath = True
            elif os.path.exists(r'C:\Program Files (x86)\Blender Foundation\Blender\blender.exe'):
                blenderPath = r'C:\Program Files (x86)\Blender Foundation\Blender\blender.exe'
                blenderPlayerPath = r'C:\Program Files (x86)\Blender Foundation\Blender\blenderplayer.exe'
                foundPath = True
            elif os.path.exists('/Applications/blender.app'):
                blenderPath = '/Applications/blender.app'
                blenderPlayerPath = '/Applications/blenderplayer.app'
                foundPath = True
            elif os.path.exists(os.path.expanduser('/Applications/blender.app')):
                blenderPath = os.path.expanduser('/Applications/blender.app')
                blenderPlayerPath = os.path.expanduser('/Applications/blenderplayer.app')
                foundPath = True

        if not foundPath:
            alert = QMessageBox()
            alert.setWindowTitle('Error')
            alert.setText('Unfortunately, SLPA could not detect an installation of Blender on your computer. Blender '
                          'is 3rd party software that SLPA uses to generate 3D models of hand shapes. You can '
                          'download Blender for free at www.blender.org/download \n'
                          'If you already have Blender installed, go to the Transcriptions menu, and click on '
                          '"Set path to Blender" to tell SLPA exactly where you have installed it.')
            alert.exec_()
            return

        blend = 'rightHand.blend' if dialog.hand == 'R' else 'leftHand.blend'
        blenderFile = os.path.join(os.getcwd(), blend)
        blenderScript = os.path.join(os.getcwd(), 'applyHandCode.py')

        if dialog.id in [0,1]:
            tab = self.configTabs.widget(0)
        else:
            tab = self.configTabs.widget(1)
        if dialog.hand == 'R':
            attr = 'hand1Transcription'
        else:
            attr = 'hand2Transcription'

        code = getattr(tab, attr).blenderCode()

        with open(os.path.join(os.getcwd(), 'handCode.txt'), mode='w', encoding='utf-8') as f:
            f.write(code)

        proc = subprocess.Popen(
            [blenderPath,
             blenderFile,
            '--background',
            "--python", blenderScript,
             ' -- ', os.getcwd(), dialog.hand])
        proc.communicate()

        proc = subprocess.Popen(
            [blenderPlayerPath,
             '-w',
             os.path.join(os.getcwd(), 'testOut3.blend')])
        proc.communicate()
        # self.blenderDialog = BlenderOutputWindow('hand_output.png',self.currentGloss())
        # self.blenderDialog.show()
        # self.blenderDialog.raise_()

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
        self.corpusList = CorpusList(self) #QListWidget(self)
        #self.corpusList.currentItemChanged.connect(self.loadHandShape)
        self.corpusList.itemClicked.connect(self.loadHandShape)
        self.dockLayout.addWidget(self.corpusList)
        self.corpusDock.setWidget(self.dockWrapper)
        self.addDockWidget(Qt.RightDockWidgetArea, self.corpusDock)

    def loadCorpus(self):
        file_path = QFileDialog.getOpenFileName(self,
                'Open Corpus File', os.getcwd(), '*.corpus')
        file_path = file_path[0]
        if not file_path:
            return None
        self.askSaveChanges = False
        self.corpusList.clear()
        self.newGloss()
        self.corpus = load_binary(file_path)
        # self.copyCorpus(file_path)
        # self.checkBackwardsComptibility()
        for sign in self.corpus:
            self.corpusList.addItem(sign.gloss)
        self.corpus.path = file_path
        self.corpusList.sortItems()
        self.corpusList.setCurrentRow(0)
        self.corpusList.itemClicked.emit(self.corpusList.currentItem())
        self.corpusNotes.setText(self.corpus.notes)
        #self.showMaximized()

    @decorators.checkForGloss
    def saveCorpusAs(self, event=None):
        if self.corpus is None:
            self.saveCorpus()
        else:
            savename = QFileDialog.getSaveFileName(self, 'Save Corpus File As', os.getcwd(), '*.corpus')
            path = savename[0]
            if not path:
                return
            if not path.endswith('.corpus'):
                path = path + '.corpus'
            self.corpus.path = path
            self.corpus.name = os.path.split(path)[1].split('.')[0]
            save_binary(self.corpus, path)

    @decorators.checkForGloss
    #@decorators.checkForCorpus
    def saveCorpus(self, event=None, checkForDuplicates=True, isDuplicate = False):
        kwargs = self.generateKwargs()
        if self.corpus is None:
            alert = QMessageBox()
            alert.setWindowTitle('No corpus loaded')
            alert.setText('You must have a corpus loaded before you can save words. What would you like to do?')
            alert.addButton('Create a new corpus', QMessageBox.AcceptRole)
            alert.addButton('Add this word to an existing corpus', QMessageBox.NoRole)

            alert.exec_()
            role = alert.buttonRole(alert.clickedButton())
            if role == QMessageBox.AcceptRole:# create new corpus
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

            elif role == QMessageBox.NoRole: # load existing corpus and add to it
                self.loadCorpus()
                if self.corpus is None:
                    # corpus will be None if the user opened a file dialog, then changed their mind and cancelled
                    return
        # else: #corpus exists
        if not checkForDuplicates:
            isDuplicate = True
            #this tiny if-block is to avoid a "double-checking" problem where a user is prompted twice in a row
            #to save a gloss, under certain circumstances
        elif kwargs['gloss'] in self.corpus.wordlist and self.showDuplicateWarning:
            isDuplicate = True
            alert = QMessageBox()
            alert.setWindowTitle('Duplicate entry')
            alert.setText('A word with the gloss {} already exists in your corpus. '
                            'What do you want to do?'.format(kwargs['gloss']))
            alert.addButton('Overwrite exising word', QMessageBox.AcceptRole)
            alert.addButton('Go back and edit the gloss', QMessageBox.RejectRole)
            alert.exec_()
            role = alert.buttonRole(alert.clickedButton())
            if role == QMessageBox.AcceptRole:#overwrite
                pass
            elif role == QMessageBox.RejectRole:#edit
                return
        self.updateCorpus(kwargs, isDuplicate)
        save_binary(self.corpus, self.corpus.path)
        self.corpus = load_binary(self.corpus.path)
        if self.showSaveAlert:
            QMessageBox.information(self, 'Success', 'Corpus successfully updated!')
        self.askSaveChanges = False
        return True

    def updateCorpus(self, kwargs, isDuplicate=False):
        sign = Sign(kwargs)
        self.corpus.addWord(sign)
        self.corpus.corpusNotes = kwargs['corpusNotes']
        if not isDuplicate:
            self.corpusList.addItem(kwargs['gloss'])
            self.corpusList.sortItems()
            for row in range(self.corpusList.count()):
                if self.corpusList.item(row).text() == kwargs['gloss']:
                    self.corpusList.setCurrentRow(row)
                    break

    def newCorpus(self):
        self.corpus = None
        self.newGloss()
        self.corpusList.clear()
        self.askSaveChanges = False

    def loadHandShape(self, gloss):
        gloss = '' if not gloss else gloss.text()
        sign = self.corpus[gloss]
        self.gloss.setText(sign['gloss'])
        self.signNotes.setText(sign['signNotes'])
        config1 = self.configTabs.widget(0)
        config2 = self.configTabs.widget(1)
        config1.clearAll()
        config2.clearAll()

        for confignum,handnum in itertools.product([1,2], [1,2]):
            name = 'config{}hand{}'.format(confignum, handnum)
            confighand = sign[name]
            configTab = self.configTabs.widget(confignum-1)
            transcription = getattr(configTab, 'hand{}Transcription'.format(handnum))
            for slot in transcription.slots:
                if slot.num == 1:
                    if confighand[0] == '_' or not confighand[0]:
                        slot.setChecked(False)
                    else:
                        slot.setChecked(True)
                else:
                    text = confighand[slot.num - 1]
                    slot.setText('' if text == '_' else text)
                    slot.updateFlags(sign.flags[name][slot.num - 1])

        model = sign.parameters
        self.setupParameterDialog(model)
        self.forearmCheckBox.setChecked(sign['forearmInvolved'])
        self.partialObscurityCheckBox.setChecked(sign['partialObscurity'])
        self.incompleteCodingCheckBox.setChecked(sign['incompleteCoding'])
        self.uncertainCodingCheckBox.setChecked(sign['uncertainCoding'])
        self.askSaveChanges = False

    def generateKwargs(self):
        #This is called whenever the corpus is updated/saved
        kwargs = {'path': None,
                'config1': None, 'config2': None,
                'flags': None, 'parameters': None,
                'corpusNotes': None, 'signNotes': None,
                'forearmInvolved': False, 'partialObscurity': False,
                'uncertainCoding': False, 'incompleteCoding': False}


        config1 = self.configTabs.widget(0)#.findChildren(TranscriptionLayout)
        kwargs['config1'] = [config1.hand1(), config1.hand2()]

        config2 = self.configTabs.widget(1)#.findChildren(TranscriptionLayout)
        kwargs['config2'] = [config2.hand1(), config2.hand2()]

        gloss = self.gloss.glossEdit.text().strip()
        kwargs['gloss'] = gloss

        flags = {'config1hand1': self.configTabs.widget(0).hand1Transcription.flags(),
                 'config1hand2': self.configTabs.widget(0).hand2Transcription.flags(),
                 'config2hand1': self.configTabs.widget(1).hand1Transcription.flags(),
                 'config2hand2': self.configTabs.widget(1).hand2Transcription.flags()}
        kwargs['flags'] = flags
        kwargs['parameters'] = self.parameterDialog.treeWidget.model
        kwargs['corpusNotes'] = self.corpusNotes.getText()
        kwargs['signNotes'] = self.signNotes.getText()
        kwargs['forearmInvolved'] = self.forearmCheckBox.isChecked()
        kwargs['partialObscurity'] = self.partialObscurityCheckBox.isChecked()
        kwargs['incompleteCoding'] = self.incompleteCodingCheckBox.isChecked()
        kwargs['uncertainCoding'] = self.uncertainCodingCheckBox.isChecked()
        return kwargs

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&Menu")
        self.fileMenu.addAction(self.newCorpusAct)
        self.fileMenu.addAction(self.loadCorpusAct)
        self.fileMenu.addAction(self.saveCorpusAct)
        self.fileMenu.addAction(self.saveCorpusAsAct)
        self.fileMenu.addAction(self.newGlossAct)
        self.fileMenu.addAction(self.exportCorpusAct)
        self.fileMenu.addAction(self.quitAct)

        self.constraintsMenu = self.menuBar().addMenu('&Constraints')
        self.constraintsMenu.addAction(self.setConstraintsAct)

        self.settingsMenu = self.menuBar().addMenu('&Options')
        self.settingsMenu.addAction(self.autoSaveAct)
        self.settingsMenu.addAction(self.alertOnCorpusSaveAct)
        self.settingsMenu.addAction(self.keepParametersOnTopAct)
        self.settingsMenu.addAction(self.askAboutDuplicatesAct)

        self.transcriptionMenu = self.menuBar().addMenu('&Transcriptions')
        self.transcriptionMenu.addAction(self.setRestrictionsAct)
        self.transcriptionMenu.addAction(self.changeTranscriptionFlagsAct)
        self.transcriptionMenu.addAction(self.setBlenderPathAct)

        self.notesMenu = self.menuBar().addMenu('&Notes')
        self.notesMenu.addAction(self.addCorpusNotesAct)
        self.notesMenu.addAction(self.addSignNotesAct)

        if not hasattr(sys, 'frozen'):
            self.debugMenu = self.menuBar().addMenu('&Debug')
            self.debugMenu.addAction(self.resetSettingsAct)
            self.debugMenu.addAction(self.forceBackCompatCheckAct)

    def alertOnCorpusSave(self):
        if self.alertOnCorpusSaveAct.isChecked():
            self.showSaveAlert = True
        else:
            self.showSaveAlert = False

    def keepParametersOnTop(self):
        if self.keepParametersOnTopAct.isChecked():
            self.parameterDialog.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.parameterDialog.show()
        else:
            self.parameterDialog.setWindowFlags(self.parameterDialog.windowFlags() ^ Qt.WindowStaysOnTopHint)
            self.parametersDialog.hide()

    def resetSettings(self):
        self.readSettings(reset = True)

    def askAboutDuplicates(self):
        if self.askAboutDuplicatesAct.isChecked():
            self.showDuplicateWarning = True
        else:
            self.showDuplicateWarning = False

    def setAutoSave(self):
        if self.autoSaveAct.isChecked():
            self.autoSave = True
        else:
            self.autoSave = False

    def changeTranscriptionFlags(self):
        config1 = self.configTabs.widget(0)
        config2 = self.configTabs.widget(1)
        flags = [config1.hand1Transcription.flags(), config1.hand2Transcription.flags(),
                 config2.hand1Transcription.flags(), config2.hand2Transcription.flags()]
        dialog = TranscriptionFlagDialog(flags)
        dialog.exec_()
        if dialog.flags is not None:#dialog.flags is None if the user clicked "cancel"
            self.configTabs.widget(0).hand1Transcription.updateFlags(dialog.flags[0])
            self.configTabs.widget(0).hand2Transcription.updateFlags(dialog.flags[1])
            self.configTabs.widget(1).hand1Transcription.updateFlags(dialog.flags[2])
            self.configTabs.widget(1).hand2Transcription.updateFlags(dialog.flags[3])
        #for row in dialog.flags:
            #iterate through the flags and set the appropriate background/border for each transcription slot


    def createActions(self):

        self.setBlenderPathAct = QAction('Set path to Blender...',
                                         self,
                                         statusTip = 'Set path to Blender',
                                         triggered = self.setBlenderPath)

        self.changeTranscriptionFlagsAct = QAction('Set transcription &flags...',
                                                 self,
                                                 statusTip = 'Change multiple flags at once',
                                                 triggered = self.changeTranscriptionFlags)

        self.autoSaveAct = QAction('&Autosave',
                                   self,
                                   statusTip = 'Always save when moving between words in a corpus',
                                   checkable = True,
                                   triggered = self.setAutoSave)

        self.forceBackCompatCheckAct = QAction('Force &backward compatibility check',
                                               self,
                                               statusTip = 'Check compatibility of current corpus',
                                               triggered = self.checkBackwardsComptibility)

        self.askAboutDuplicatesAct = QAction('Warn about duplicate glosses',
                                             self,
                                             statusTip = 'Ask before overwriting duplicate glosses',
                                             checkable = True,
                                             triggered = self.askAboutDuplicates)

        self.resetSettingsAct = QAction('&Reset all settings',
                                        self,
                                        statusTip = 'Reset all options and settings to defaults',
                                        triggered = self.resetSettings)


        self.alertOnCorpusSaveAct = QAction('Show save &alert',
                                            self,
                                            statusTip='Show a pop-up window whenever a corpus entry is saved',
                                            checkable = True,
                                            triggered = self.alertOnCorpusSave)

        self.keepParametersOnTopAct = QAction('Keep parameters window on &top',
                                              self,
                                              statusTip = 'Always keep the parameters window on top of other windows',
                                              checkable = True,
                                              triggered = self.keepParametersOnTop)


        self.newCorpusAct = QAction('&New corpus',
                                    self,
                                    statusTip="Start a new corpus", triggered = self.newCorpus)

        self.loadCorpusAct = QAction( "&Load corpus...",
                self,
                statusTip="Load a corpus",
                triggered=self.loadCorpus)

        self.saveCorpusAct = QAction( "&Save corpus",
                self,
                statusTip="Save current corpus",
                triggered=self.saveCorpus)

        self.saveCorpusAsAct = QAction("Save corpus &as...",
                                       self,
                                       statusTip = "Save current corpus under a new name",
                                       triggered=self.saveCorpusAs)

        self.newGlossAct = QAction('&New gloss',
                self,
                statusTip='Clear current info and make a new gloss',
                triggered=self.newGloss)

        self.quitAct = QAction( "&Quit",
                self,
                statusTip="Quit", triggered=self.closeEvent)

        self.exportCorpusAct = QAction('&Export corpus as csv...',
                                    self,
                                    statusTip='Save corpus as csv for opening as a spreadsheet',
                                    triggered=self.exportCorpus)

        self.setRestrictionsAct = QAction('Allow &unrestricted transcriptions',
                                    self,
                                    statusTip = 'If on, anything can be entered into transcriptions',
                                    triggered = self.setTranscriptionRestrictions,
                                    checkable = True)
        self.setConstraintsAct = QAction('Select anatomical/phonological &constraints...',
                                    self,
                                    statusTip = 'Select (violable) constraints on transcriptions',
                                    triggered = self.setConstraints)
        self.addCorpusNotesAct = QAction('Edit &corpus notes...',
                                         self,
                                         statusTip = 'Open a notepad for information about the corpus',
                                         triggered = self.addCorpusNotes)
        self.addSignNotesAct = QAction('Edit &sign notes...',
                                        self,
                                       statusTip = 'Open a notepad for information about the current sign',
                                       triggered = self.addSignNotes)


    def initCorpusNotes(self):
        self.corpusNotes = NotesDialog()
        if self.corpus is None:
            title = 'Notes for unnamed corpus'
        else:
            title = 'Notes for {} corpus'.format(self.corpus.name)
        self.corpusNotes.setWindowTitle(title)

    def initSignNotes(self):
        self.signNotes = NotesDialog()
        if self.gloss.text():
            self.signNotes.setWindowTitle('Notes for the sign {}'.format(self.gloss.text()))
        else:
            self.signNotes.setWindowTitle('Notes for an unglossed sign')

    def addCorpusNotes(self):
        if self.corpus is None:
            self.corpusNotes.setWindowTitle('Notes for unnamed corpus')
        else:
            self.corpusNotes.setWindowTitle('Notes for {} corpus'.format(self.corpus.name))
        self.corpusNotes.show()
        self.corpusNotes.raise_()
        self.askSaveChanges = True

    def addSignNotes(self):
        if self.gloss.text():
            self.signNotes.setWindowTitle('Notes for the sign {}'.format(self.gloss.text()))
        else:
            self.signNotes.setWindowTitle('Notes for an unglossed sign')
        self.signNotes.show()
        self.signNotes.raise_()
        self.askSaveChanges = True

    def setConstraints(self):
        dialog = ConstraintsDialog(self.constraints)
        constraints = dialog.exec_()
        if constraints:
            for c in MasterConstraintList:
                self.constraints[c[0]] = getattr(dialog, c[0]).isChecked()

    def setTranscriptionRestrictions(self):
        restricted = self.setRestrictionsAct.isChecked()
        self.restrictedTranscriptions = restricted
        self.transcriptionRestrictionsChanged.emit(restricted)

    def exportCorpus(self):

        dialog = ExportCorpusDialog()
        results = dialog.exec_()

        if results:
            path = dialog.fileNameEdit.text()
            include_fields = dialog.includeFields.isChecked()
            blank_space = dialog.blankSpaceEdit.text()
            x_in_box = dialog.xinboxEdit.text()
            null = dialog.nullEdit.text()
            if not blank_space:
                blank_space = ''
            kwargs = {'include_fields': include_fields, 'blank_space': blank_space}
            if x_in_box:
                kwargs['x_in_box'] = x_in_box
            if null:
                kwargs['null'] = null
            output = [word.export(**kwargs) for word in self.corpus]
            try:
                with open(path, encoding='utf-8', mode='w') as f:
                    #print(Sign.headers, file=f)
                    f.write(Sign.headers)
                    for word in output:
                        f.write(word)
                        #print(word, file=f)
                if self.showSaveAlert:
                    QMessageBox.information(self, 'Success', 'Corpus successfully exported!')
            except PermissionError:
                filename = os.path.split(path)[-1]
                alert = QMessageBox()
                alert.setWindowTitle('Error encountered')
                alert.setText('The file {} is already open in a program on your computer. Please close the file before '
                              'saving, or else choose a different file name.'.format(filename))
                alert.exec_()

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

    @decorators.checkForUnsavedChanges
    def newGloss(self, clearFlags=True):
        self.gloss.glossEdit.setText('')
        self.configTabs.widget(0).clearAll(clearFlags=clearFlags)
        self.configTabs.widget(1).clearAll(clearFlags=clearFlags)
        self.configTabs.setCurrentIndex(0)

        self.parameterDialog.accept()
        self.setupParameterDialog(ParameterTreeModel(parameters.defaultParameters))
        self.initSignNotes()
        for widget in self.globalOptionsWidgets:
            widget.setChecked(False)
        self.askSaveChanges = False

class ExportCorpusDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Export Corpus')

        layout = QVBoxLayout()

        fileNameLayout = QHBoxLayout()
        self.fileNameEdit = QLineEdit('')
        self.fileNameEdit.setPlaceholderText('')
        selectLocationButton = QPushButton('Select save location...')
        selectLocationButton.clicked.connect(self.getSaveName)
        fileNameLayout.addWidget(selectLocationButton)
        fileNameLayout.addWidget(self.fileNameEdit)
        layout.addLayout(fileNameLayout)

        outputOptionsLayout = QVBoxLayout()
        blankSpaceLabel = QLabel('\n\nWhich character should be used to represent empty transcription slots?\n'
                                 'Mouse over the text box for details.')
        blankSpaceLabel.setWordWrap(True)
        self.blankSpaceEdit = QLineEdit('')
        self.blankSpaceEdit.setMaximumWidth(100)
        self.blankSpaceEdit.setToolTip('If you want empty slots to appear as blank spaces, then type one space.'
                                  '\nIf you do not want empty slots represented at all in the output, type nothing.')

        self.includeFields = QCheckBox('Include fields in transcription?')
        self.includeFields.setToolTip('If checked, transcriptions will be delimited by square brackets '
                                  'and numbers representing fields.\n'
                                  'If not checked, transcriptions will be one long string.')

        altSymbolsLabel = QLabel('Some programs have trouble displaying the "ultracrossed" symbol (x-in-a-box) and the '
                            'empty set symbol. If you would like to use alternatives in the output file, you can '
                            'enter them below.')
        altSymbolsLabel.setWordWrap(True)
        self.xinboxEdit = QLineEdit('')
        self.xinboxEdit.setMaximumWidth(170)
        self.xinboxEdit.setPlaceholderText('Alternative ultracrossed symbol')

        self.nullEdit = QLineEdit('')
        self.nullEdit.setMaximumWidth(170)
        self.nullEdit.setPlaceholderText('Alternative empty set symbol')

        outputOptionsLayout.addWidget(self.includeFields)
        outputOptionsLayout.addWidget(blankSpaceLabel)
        outputOptionsLayout.addWidget(self.blankSpaceEdit)

        outputOptionsLayout.addWidget(altSymbolsLabel)
        outputOptionsLayout.addWidget(self.xinboxEdit)
        outputOptionsLayout.addWidget(self.nullEdit)
        layout.addLayout(outputOptionsLayout)

        buttonLayout = QHBoxLayout()
        self.okButton = QPushButton('OK')
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.reject)
        self.okButton.clicked.connect(self.accept)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def getSaveName(self):
        savename = QFileDialog.getSaveFileName(self, 'Export Corpus as CSV', os.getcwd(), '*.csv')
        path = savename[0]
        if not path:
            return
        if not path.endswith('.csv'):
            path = path + '.csv'
        self.fileNameEdit.setText(path)

    def accept(self):
        if os.path.exists(os.path.split(self.fileNameEdit.text())[0]):
            super().accept()
        else:
            if not self.fileNameEdit.text():
                text = 'Please enter a file name'
            else:
                text = ('The file name you supplied is not valid. Use the "Select save location..." '
                          'button to select a folder on your computer, and then a enter a name for your output file.')
            alert = QMessageBox()
            alert.setWindowTitle('File name error')
            alert.setText(text)
            alert.exec_()

class BlenderPathDialog(QDialog):

    def __init__(self, current_path=None):
        super().__init__()
        self.setWindowTitle('Set path to Blender')
        label = QLabel('Path to Blender executable: ')
        self.pathEdit = QLineEdit()
        if current_path is not None:
            self.pathEdit.setText(os.path.join(current_path, 'blender.exe'))
            self.file_path = current_path
        else:
            self.file_path = None
        explore = QPushButton('Find')
        explore.clicked.connect(self.findPath)
        explanation = QLabel('Blender is 3rd party software that the Sign Language Phonetic Annotator uses to generate '
                             '3D models of hand shapes. You can download Blender for free from '
                             'https://www.blender.org/download/. '
                             '\n\nYou must download and install Blender in order for '
                             'the "Visualize Handshape" button to work. This is completely optional, however, and '
                             'it is not required for the general use of SLPA.\n\n'
                             'If you have already installed Blender, click the "Find" button above to locate it on '
                             'your computer. Look for a file called "blender.exe" (Windows) or "blender.app" (Mac). '
                             'It is typically located in C:\\Program Files\\Blender Foundation\\Blender on Windows, or '
                             'in /Applications/Blender on Mac.')
        explanation.setWordWrap(True)
        font = QFont(FONT_NAME, FONT_SIZE)
        explanation.setFont(font)
        topLayout = QHBoxLayout()
        topLayout.addWidget(label)
        topLayout.addWidget(self.pathEdit)
        topLayout.addWidget(explore)
        midLayout = QHBoxLayout()
        ok = QPushButton('OK')
        cancel = QPushButton('Cancel')
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        midLayout.addWidget(ok)
        midLayout.addWidget(cancel)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(midLayout)
        mainLayout.addWidget(explanation)
        self.setLayout(mainLayout)

    def findPath(self):
        file_path = QFileDialog.getOpenFileName(self,
                                                'Find Blender', os.getcwd(), 'blender.exe')
        file_path = file_path[0]
        if not file_path:
            self.file_path = None
            self.pathEdit.setText('')
        else:
            path = os.path.abspath(file_path)
            self.file_path = path
            self.pathEdit.setText(path)

def clean(item):
    """Clean up the memory by closing and deleting the item if possible."""
    if isinstance(item, list):
        for _ in range(len(item)):
            clean(item.pop())
    elif isinstance(item, dict):
        while item:
            clean(item.popitem())
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
    elif data == 'oneHandMovement':
        return 5
    elif data == 'twoHandMovement':
        return 6
    elif data == 'orientation':
        return 7

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
    if hasattr(sys, 'frozen'):
        dir = os.path.dirname(sys.executable)
        path = os.path.join(dir, 'media', filename)
    else:
        path = os.path.join(os.getcwd(), 'media', filename)
    return path