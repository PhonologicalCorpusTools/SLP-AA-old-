import itertools
import subprocess
import collections
import parameters
import decorators
from getpass import getuser
from datetime import date
from xml.etree import ElementTree as xmlElementTree
from lexicon import *
from binary import *
from gui.transcriptions import *
from gui.constraintwidgets import *
from gui.notes import NotesDialog, CoderDialog
from gui.search import *
from image import *
from gui.functional_load import *
from gui.colour import *
from constants import GLOBAL_OPTIONS
from gui.parameterwidgets import ParameterDialog, ParameterTreeModel
from gui.transcription_search import TranscriptionSearchDialog
from gui.handshape_search import HandshapeSearchDialog
from gui.phonological_search import ExtendedFingerSearchDialog
from gui.results_windows import ResultsWindow
from gui.helperwidgets import PredefinedHandshapeDialog
#from slpa import __version__ as currentSLPAversion
from pprint import pprint

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
        self.setContentsMargins(0, 0, 0, 0)

        # self.forearmButton = QCheckBox('1. Forearm')
        # self.addWidget(self.forearmButton, 0, 1)
        ##do not delete the commented lines above - they may be useful in the future if the
        ##forearm slot returns to the transcription lines, instead of the global options
        self.addLayout(handshapes, 0, 2)
        self.handShapeMatch = QPushButton('Make Hand 2 = Hand 1')
        self.addWidget(self.handShapeMatch, 1, 0)
        self.hand2 = hand2
        self.handShapeMatch.clicked.connect(self.hand2.match)


class GlossLayout(QHBoxLayout):
    def __init__(self, parent=None, comboBoxes=None):
        QHBoxLayout.__init__(self)
        defaultFont = QFont(FONT_NAME, FONT_SIZE)
        self.setContentsMargins(-1, -1, -1, 0)
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
        #originalItem = [i for i in self.selectedItems()][0]
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
                alert.exec_()
                if alert.buttonRole(alert.clickedButton()) == QMessageBox.YesRole:  #continue and save
                    self.parent.saveCorpus(checkForDuplicates=True)
                    selectedItem = [i for i in self.selectedItems()][0]
                    self.itemClicked.emit(selectedItem)

                elif alert.buttonRole(alert.clickedButton()) == QMessageBox.NoRole:  #continue but don't save
                    selectedItem = [i for i in self.selectedItems()][0]
                    self.itemClicked.emit(selectedItem)

                #elif alert.buttonRole(alert.clickedButton()) == QMessageBox.RejectRole: #go back and edit the gloss
                #    self.setCurrentItem(originalItem)
                #    self.itemClicked.emit(originalItem)


class MergeCorpusMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Duplicate entry')
        self.baseText = 'Your current corpus already has a sign called {}.\n\nWhat do you want to do?'
        self.addButton('Keep the current sign', QMessageBox.AcceptRole)
        self.addButton('Overwrite with the new sign', QMessageBox.ResetRole)
        self.alwaysMergeCheckBox = QCheckBox('Do this for all future duplicates')
        self.setCheckBox(self.alwaysMergeCheckBox)


class MainWindow(QMainWindow):
    transcriptionRestrictionsChanged = Signal(bool)
    forearmChecked = Signal(bool)

    def __init__(self, app=None):
        if app is not None:
            app.messageFromOtherInstance.connect(self.handleMessage)
        super(MainWindow, self).__init__()
        self.setWindowTitle('SLP-Annotator')
        self.setWindowIcon(QIcon(getMediaFilePath('slpa_icon.png')))
        self.setContentsMargins(0, 0, 0, 0)

        self.coder = getuser()
        self.today = date.today()

        #Set "global" variables
        self.askSaveChanges = False
        self.constraints = dict()
        self.clipboard = list()
        self.createActions()
        self.createMenus()
        self.readSettings()
        if not self.recentPhraseSearches:
            self.recentPhraseSearches = list()
        if not self.recentTranscriptionSearches:
            self.recentTranscriptionSearches = list()
        self.recentPhraseSearches = collections.deque(self.recentPhraseSearches, maxlen=self.recentSearchMax)
        self.recentTranscriptionSearches = collections.deque(self.recentTranscriptionSearches, maxlen=self.recentSearchMax)
        #these variables are reinitialized because we don't know the maxlen value until after the readSettings() call

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
        #self.copyButton = QPushButton('Copy')
        #self.pasteButton = QPushButton('Paste')
        #self.copyButton.clicked.connect(self.copyTranscription)
        #self.pasteButton.clicked.connect(self.pasteTranscription)
        #topLayout.addWidget(self.copyButton)
        #topLayout.addWidget(self.pasteButton)

        # Predefined handshapes
        self.predefineButton = QPushButton('Predefined handshapes')
        self.predefineButton.clicked.connect(self.predefinedTranscription)
        topLayout.addWidget(self.predefineButton)

        # Add parameters button
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
        self.configTabs.addTab(TranscriptionConfigTab(1), 'Config 1')
        self.configTabs.addTab(TranscriptionConfigTab(2), 'Config 2')
        self.configTabs.widget(0).updateSignal.connect(self.updateLastUpdated)
        self.configTabs.widget(1).updateSignal.connect(self.updateLastUpdated)
        layout.addWidget(self.configTabs)

        #Add "global" handshape options (as checkboxes)
        self.globalOptionsLayout = QHBoxLayout()
        self.setupGlobalOptions()
        layout.addLayout(self.globalOptionsLayout)

        #Make hand image and accompanying info
        self.infoPanel = QHBoxLayout()
        self.handImage = HandShapeImage(getMediaFilePath('hand.JPG'))
        self.infoPanel.addWidget(self.handImage)
        self.transcriptionInfo = TranscriptionInfo(coder=self.coder, lastUpdated=self.today)
        self.transcriptionInfo.signNoteEdited.connect(self.changeSaveFlag)
        self.transcriptionInfo.coderUpdated.connect(self.changeSaveFlag)
        self.transcriptionInfo.dateUpdated.connect(self.changeSaveFlag)

        self.infoPanel.addLayout(self.transcriptionInfo)
        layout.addLayout(self.infoPanel)

        #Connect transcription signals to various main window slots
        for k in [0, 1]:
            self.configTabs.widget(k).hand1Transcription.slots[0].stateChanged.connect(self.userMadeChanges)
            self.forearmChecked.connect(self.configTabs.widget(k).hand1Transcription.slot1.setChecked)

            for slot in self.configTabs.widget(k).hand1Transcription.slots[1:]:
                slot.slotSelectionChanged.connect(self.handImage.useNormalImage)
                slot.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)
                slot.slotSelectionChanged.connect(self.transcriptionInfo.transcriptionSlotChanged)
                slot.textChanged.connect(self.userMadeChanges)
                slot.slotFlagged.connect(self.userMadeChanges)
                self.transcriptionRestrictionsChanged.connect(slot.changeValidatorState)

            self.configTabs.widget(k).hand2Transcription.slots[0].stateChanged.connect(self.userMadeChanges)
            self.forearmChecked.connect(self.configTabs.widget(k).hand2Transcription.slot1.setChecked)
            for slot in self.configTabs.widget(k).hand2Transcription.slots[1:]:
                slot.slotSelectionChanged.connect(self.handImage.useReverseImage)
                slot.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)
                slot.slotSelectionChanged.connect(self.transcriptionInfo.transcriptionSlotChanged)
                slot.textChanged.connect(self.userMadeChanges)
                slot.slotFlagged.connect(self.userMadeChanges)
                self.transcriptionRestrictionsChanged.connect(slot.changeValidatorState)

        self.transcriptionRestrictionsChanged.emit(self.restrictedTranscriptions)

        self.globalLayout.addLayout(layout)

        self.wrapper.setLayout(self.globalLayout)
        self.setCentralWidget(self.wrapper)

        self.parameterDialog = None
        self.setupParameterDialog(ParameterTreeModel(parameters.defaultParameters))
        self.initCorpusNotes()
        #self.initSignNotes()
        self.makeCorpusDock()

        self.showMaximized()
        #self.defineTabOrder()

    def updateLastUpdated(self, value):
        if value:
            self.transcriptionInfo.lastUpdated = self.today

    def changeSaveFlag(self, edited):
        if edited:
            self.askSaveChanges = True

    def resizeEvent(self, e):
        self.showMaximized()

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
            return

        alert = QMessageBox()
        alert.setWindowTitle('Warning')
        alert.setText('Are you sure you want to delete this entry from your corpus? This action cannot be undone.')
        alert.addButton('Yes, delete it', QMessageBox.YesRole)
        alert.addButton('No, go back', QMessageBox.NoRole)
        alert.exec_()
        if alert.buttonRole(alert.clickedButton()) == QMessageBox.NoRole:
            return
        else:
            del self.corpus.wordlist[gloss]
            for n in range(self.corpusList.count()):
                item = self.corpusList.item(n)
                if item.text() == gloss:
                    goodbye = self.corpusList.takeItem(n)
                    del goodbye
                    break
            save_binary(self.corpus, self.corpus.path)
            self.newGloss()

    def setupGlobalOptions(self):
        self.globalOptionsWidgets = list()
        globalOptionsLabel = QLabel('Global handshape options:')
        globalOptionsLabel.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(globalOptionsLabel)
        for option in GLOBAL_OPTIONS:
            widget = GlobalOptionCheckBox(option.title(), self.userMadeChanges)
            option += 'CheckBox'
            setattr(self, option, widget)
            widget = getattr(self, option)
            self.globalOptionsLayout.addWidget(widget)
            self.globalOptionsWidgets.append(widget)


    def checkForearm(self):
        self.forearmChecked.emit(self.forearmCheckBox.isChecked())

    def setupParameterDialog(self, model):
        currentGloss = self.currentGloss()
        # if self.corpus is not None and currentGloss:
        #     model = self.corpus[currentGloss].parameters
        # else:
        #     model = ParameterTreeModel(parameters.defaultParameters)

        if self.parameterDialog is None:
            self.parameterDialog = ParameterDialog(model)
            #self.parameterDialog.reset()
        else:
            self.parameterDialog.close()
            self.parameterDialog.deleteLater()
            self.parameterDialog = ParameterDialog(model, checkStrategy='load')

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
        transcriptions = self.getTranscriptions()
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
            include_flags = dialog.includeFlags.isChecked()
            if dialog.transcriptionID == 0:
                self.configTabs.widget(0).hand1Transcription.updateFromCopy(self.clipboard,include_flags=include_flags)
            elif dialog.transcriptionID == 1:
                self.configTabs.widget(0).hand2Transcription.updateFromCopy(self.clipboard,include_flags=include_flags)
            if dialog.transcriptionID == 2:
                self.configTabs.widget(1).hand1Transcription.updateFromCopy(self.clipboard,include_flags=include_flags)
            if dialog.transcriptionID == 3:
                self.configTabs.widget(1).hand2Transcription.updateFromCopy(self.clipboard,include_flags=include_flags)

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
        for k in range(1, 35):
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

        self.settings.beginGroup('recentSearches')
        if not self.recentTranscriptionSearches:
            self.recentTranscriptionSearches = list()
        if not self.recentPhraseSearches:
            self.recentPhraseSearches = list()
        self.settings.setValue('recentTranscriptionSearches', list(self.recentTranscriptionSearches))
        self.settings.setValue('recentPhraseSearches', list(self.recentPhraseSearches))
        self.settings.setValue('recentSearchMax', self.recentSearchMax)
        self.settings.setValue('transcriptionSearchBlankOption', self.transcriptionSearchBlankOption)
        self.settings.setValue('transcriptionSearchWildcard', self.transcriptionSearchWildcard)
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

        self.settings.beginGroup('recentSearches')
        self.recentTranscriptionSearches = self.settings.value('recentTranscriptionSearches')
                                                               #defaultValue=list(), type=list)
        self.recentPhraseSearches = self.settings.value('recentPhraseSearches')
                                                        #defaultValue=list(), type=list)
        self.recentSearchMax = self.settings.value('recentSearchMax',
                                                   defaultValue=10, type=int)
        self.transcriptionSearchBlankOption = self.settings.value('transcriptionSearchBlankOption')
        self.transcriptionSearchWildcard = self.settings.value('transcriptionSearchWildcard')
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

    def checkForFlags(self):
        for word in self.corpus:
            newflags = {k:list() for k in word.flags.keys()}
            for key,value in word.flags.items():
                newflags[key] = [Flag(v, False) for v in value]
                #SET TO UNCERTAIN
            word.flags = newflags

    def checkBackwardsComptibility(self, forceUpdate=False):

        for attribute, default_value in sorted(Corpus.corpus_attributes.items()):
            if not hasattr(self.corpus, attribute):
                setattr(self.corpus, attribute, Corpus.copyValue(Corpus, default_value))

        word = self.corpus.randomWord()

        oldParameterTreeMethods = dir(word.parameters)
        currentParameterTreeMethods = dir(ParameterTreeModel)
        for method in currentParameterTreeMethods:
            if not method in oldParameterTreeMethods:
                updateParameters = True
                break
        else:
            updateParameters = False


        for attribute, default_value in Sign.sign_attributes.items():
            if not hasattr(word, attribute):
                updateSigns = True
                break
        else:
            updateSigns = False

        if forceUpdate:
            updateSigns = True
            updateParameters = True

        if not updateSigns and not updateParameters:
            return

        for word in self.corpus:
            if updateSigns:
                for attribute, default_value in sorted(Sign.sign_attributes.items()):
                    if not hasattr(word, attribute):
                        setattr(word, attribute, Sign.copyValue(Sign, default_value))
                    if attribute == 'estimated' and hasattr(word, 'partialObscurity'):
                        word.estimated = word.partialObscurity
                        del word.partialObscurity
                    elif attribute == 'forearm' and hasattr(word, 'forearmInvolved'):
                        word.forearm = word.forearmInvolved
                        del word.forearmInvolved
                    elif attribute == 'uncertain' and hasattr(word, 'uncertainCoding'):
                        word.uncertain = word.uncertainCoding
                        del word.uncertainCoding
                    elif attribute == 'incomplete' and hasattr(word, 'incompleteCoding'):
                        word.incomplete = word.incompleteCoding
                        del word.incompleteCoding
                    elif attribute == 'oneHandMovement' and hasattr(word, 'movement'):
                        word.oneHandMovement = word.movement
                        del word.movement
            if updateParameters:
                try:
                    params = word.parameters.parameterList
                    newTree = ParameterTreeModel(params)
                except AttributeError:#occurs with older copora where ParameterNode and anytree.Nodes are intermixed
                    newTree = ParameterTreeModel(parameters.defaultParameters)
                word.parameters = newTree

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
        transcriptions = self.getTranscriptions()
        dialog = TranscriptionSelectDialog(transcriptions, mode='blender')
        dialog.exec_()
        if not dialog.selectedTranscription:
            return

        nonstandard = list()
        for slot in dialog.selectedTranscription:
            symbol = slot.getText(empty_text='_')
            if symbol not in STANDARD_SYMBOLS:
                nonstandard.append(symbol)

        if nonstandard:
            nonstandard = '   '.join(nonstandard)
            alert = QMessageBox()
            alert.setWindowTitle('Nonstandard symbols')
            alert.setText('The transcription you selected contains the following non-standard symbols:\n\n{}\n\n'
                          'Unfortunately, SLPAnnotator cannot interpret these symbols, and therefore cannot create a '
                          '3D image of this handshape. Sorry about that!\n\n'
                          'The accepted "standard" symbols are those found in transcription dropdown boxes and next to '
                          'the image of the hand. '.format(nonstandard))

            alert.exec_()
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
            elif os.path.exists('/Applications/Blender'):
                blenderPath = '/Applications/Blender/blender.app/Contents/MacOS/blender'
                blenderPlayerPath = '/Applications/Blender/blenderplayer.app/Contents/MacOS/blenderplayer'
                foundPath = True
            elif os.path.exists(os.path.expanduser('/Applications/Blender')):
                blenderPath = os.path.expanduser('/Applications/Blender/blender.app/Conents/MacOS/blender')
                blenderPlayerPath = os.path.expanduser('/Applications/Blender/blenderplayer.app/Contents/MacOS/blenderplayer')
                foundPath = True

        if not foundPath:
            alert = QMessageBox()
            alert.setWindowTitle('Error')
            alert.setText('Unfortunately, SLPAnnotator could not detect an installation of Blender on your computer. Blender '
                          'is 3rd party software that SLPAnnotator uses to generate 3D models of hand shapes. You can '
                          'download Blender for free at www.blender.org/download \n'
                          'If you already have Blender installed, go to the Transcriptions menu, and click on '
                          '"Set path to Blender" to tell SLPAnnotator exactly where you have installed it.')
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

        colourDialog = ColourPickerDialog()
        colourDialog.exec_()
        handColour = colourDialog.selectedColor()

        colorCodeR = str(float(handColour.red()/255))
        colorCodeG = str(float(handColour.green()/255))
        colorCodeB = str(float(handColour.blue()/255))
        proc = subprocess.Popen(
            [blenderPath,
             blenderFile,
            '--background',
            '--python', blenderScript,
             os.getcwd(), dialog.hand, colorCodeR, colorCodeG, colorCodeB])
        proc.communicate()

        proc = subprocess.Popen(
            [blenderPlayerPath,
             '-w',
             os.path.join(os.getcwd(), 'handImage.blend')])
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
        self.corpusList = CorpusList(self)  #QListWidget(self)
        #self.corpusList.currentItemChanged.connect(self.loadHandShape)
        self.corpusList.itemClicked.connect(self.loadHandShape)
        self.dockLayout.addWidget(self.corpusList)
        self.corpusDock.setWidget(self.dockWrapper)
        self.addDockWidget(Qt.RightDockWidgetArea, self.corpusDock)

    def loadCorpus(self, showFileDialog = True):
        file_path = QFileDialog.getOpenFileName(self, 'Open Corpus File', os.getcwd(), '*.corpus')
        file_path = file_path[0]
        if not file_path:
            return None
        self.corpus = load_binary(file_path)
        self.corpus.path = file_path
        #self.checkBackwardsComptibility()
        self.setupNewCorpus()

    def setupNewCorpus(self):
        self.askSaveChanges = False
        self.corpusList.clear()
        self.newGloss()
        self.corpusDock.setWindowTitle(self.corpus.name)

        for sign in self.corpus:
            self.corpusList.addItem(sign.gloss)

        self.corpusList.sortItems()
        self.corpusList.setCurrentRow(0)
        self.corpusList.itemClicked.emit(self.corpusList.currentItem())
        self.corpusNotes.setText(self.corpus.notes)

        self.transcriptionInfo.signNoteText.setText(self.currentHandShape().notes)

        #self.signNotes.setText(self.currentHandShape().notes)
        #save_binary(self.corpus, self.corpus.path)
        self.showMaximized()

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
            self.corpus = load_binary(path)

    @decorators.checkForGloss
    #@decorators.checkForCorpus
    def saveCorpus(self, checkForDuplicates=True, isDuplicate = False):
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

            elif role == QMessageBox.NoRole:  # load existing corpus and add to it
                self.loadCorpus()
                if self.corpus is None:
                    # corpus will be None if the user opened a file dialog, then changed their mind and cancelled
                    return
        # else: #corpus exists
        if not checkForDuplicates:
            isDuplicate = False

        #this tiny if-block is to avoid a "double-checking" problem where a user is prompted twice in a row
        #to save a gloss, under certain circumstances
        elif kwargs['gloss'] in self.corpus.wordlist and self.showDuplicateWarning:
            isDuplicate = True
            alert = QMessageBox()
            alert.setWindowTitle('Duplicate entry')
            alert.setText('A word with the gloss {} already exists in your corpus. '
                          'What do you want to do?'.format(kwargs['gloss']))
            alert.addButton('Overwrite existing word', QMessageBox.AcceptRole)
            alert.addButton('Go back and edit the gloss', QMessageBox.RejectRole)
            alert.exec_()
            role = alert.buttonRole(alert.clickedButton())
            if role == QMessageBox.AcceptRole:  # overwrite
                pass
            elif role == QMessageBox.RejectRole:  # edit
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
        try:
            gloss = gloss.text()
        except AttributeError:
            if not gloss:
                gloss = ''  # else it's just a string
        sign = self.corpus[gloss]
        self.gloss.setText(sign['gloss'])
        self.transcriptionInfo.signNoteText.setText(sign['signNotes'])

        if not hasattr(sign, '_coder') or not hasattr(sign, '_lastUpdated'):
            setattr(sign, '_coder', self.coder)
            setattr(sign, '_lastUpdated', self.today)

        self.transcriptionInfo.coderLineEdit.setText(sign['_coder'])
        self.transcriptionInfo.lastUpdatedLineEdit.setText(str(sign['_lastUpdated']))

        #self.signNotes.setText(sign['signNotes'])
        config1 = self.configTabs.widget(0)
        config2 = self.configTabs.widget(1)
        config1.clearAll()
        config2.clearAll()

        for confignum, handnum in itertools.product([1, 2], [1, 2]):
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

        model = ParameterTreeModel(sign.parameters)
        self.setupParameterDialog(model)
        for option in GLOBAL_OPTIONS:
            name = option+'CheckBox'
            widget = getattr(self, name)
            widget.setChecked(sign[option])
        self.askSaveChanges = False
        self.showMaximized()

    def generateKwargs(self):
        #This is called whenever the corpus is updated/saved
        kwargs = {'path': None,
                  'config1': None, 'config2': None,
                  'flags': None, 'parameters': None,
                  'corpusNotes': None, 'signNotes': None,
                  '_coder': None, '_lastUpdated': None,
                  'forearm': False, 'estimated': False,
                  'uncertain': False, 'incomplete': False, 'reduplicated': False}

        config1 = self.configTabs.widget(0)
        kwargs['config1'] = [config1.hand1(), config1.hand2()]

        config2 = self.configTabs.widget(1)
        kwargs['config2'] = [config2.hand1(), config2.hand2()]

        gloss = self.gloss.glossEdit.text().strip()
        kwargs['gloss'] = gloss

        flags = {'config1hand1': self.configTabs.widget(0).hand1Transcription.flags(),
                 'config1hand2': self.configTabs.widget(0).hand2Transcription.flags(),
                 'config2hand1': self.configTabs.widget(1).hand1Transcription.flags(),
                 'config2hand2': self.configTabs.widget(1).hand2Transcription.flags()}
        kwargs['flags'] = flags
        kwargs['parameters'] = self.parameterDialog.saveParameters()
        kwargs['corpusNotes'] = self.corpusNotes.getText()
        kwargs['signNotes'] = self.transcriptionInfo.signNoteText.text()
        #kwargs['signNotes'] = self.signNotes.getText()
        if not kwargs['signNotes']:
            kwargs['signNotes'] == 'None'
        kwargs['_coder'] = self.transcriptionInfo.coder
        kwargs['_lastUpdated'] = self.transcriptionInfo.lastUpdated
        for option in GLOBAL_OPTIONS:
            kwargs[option] = getattr(self, option+'CheckBox').isChecked()
        return kwargs

    def overwriteAllGlosses(self):
        #this is a debugging function and should not normally be called
        for word in self.corpus:
            self.loadHandShape(word.gloss)
            self.saveCorpus()

    def funcLoad(self):
        if not self.corpus:
            return 
        dialog = FunctionalLoadDialog(self.corpus)
        dialog.exec_()
        resultsTable = FunctionalLoadResultsTable(dialog.results)
        resultsTable.exec_()

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(self.newCorpusAct)
        self.fileMenu.addAction(self.loadCorpusAct)
        self.fileMenu.addAction(self.mergeCorpusAct)
        self.fileMenu.addAction(self.saveCorpusAct)
        self.fileMenu.addAction(self.saveCorpusAsAct)
        self.fileMenu.addAction(self.newGlossAct)
        self.fileMenu.addAction(self.exportCorpusAct)
        self.fileMenu.addAction(self.importCorpusAct)
        self.fileMenu.addAction(self.quitAct)
        self.fileMenu.addAction(self.switchAct)

        self.editMenu = self.menuBar().addMenu('\u200C&Edit')
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)
        self.editMenu.addAction(self.autofillAct)
        #self.editMenu.addAction(self.predefineAct)

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
        self.notesMenu.addAction(self.editCoderAct)
        #self.notesMenu.addAction(self.addSignNotesAct)

        #self.searchMenu = self.menuBar().addMenu('&Search')
        #self.searchMenu.addAction(self.transcriptionSearchAct)
        #self.searchMenu.addAction(self.phraseSearchAct)
        #self.searchMenu.addAction(self.glossSearchAct)
        #self.searchMenu.addAction(self.funcloadAct)

        if not hasattr(sys, 'frozen'):
            self.debugMenu = self.menuBar().addMenu('&Debug')
            self.debugMenu.addAction(self.resetSettingsAct)
            self.debugMenu.addAction(self.forceCompatibilityUpdateAct)
            self.debugMenu.addAction(self.printCorpusObjectAct)
            self.debugMenu.addAction(self.overwriteAllGlossesAct)

    def printCorpusObject(self):
        if self.corpus is None:
            print('No corpus loaded')
        else:
            print('CORPUS ATTRIBUTES')
            for key, value in sorted(self.corpus.__dict__.items()):
                print(key, type(value), value)
            print('\nWORD ATTRIBUTES')
            #word = self.corpus.randomWord()
            word = self.corpus[self.currentGloss()]
            for key, value in sorted(word.__dict__.items()):
                print(key, type(value), value)

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
            self.parameterDialog.hide()

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

    def getTranscriptions(self):
        transcriptions = list()
        transcriptions.append(self.configTabs.widget(0).hand1Transcription)
        transcriptions.append(self.configTabs.widget(0).hand2Transcription)
        transcriptions.append(self.configTabs.widget(1).hand1Transcription)
        transcriptions.append(self.configTabs.widget(1).hand2Transcription)
        return transcriptions

    def searchCorpus(self, searchType = 'transcriptions'):
        if not self.corpus:
            alert = QMessageBox()
            alert.setWindowTitle('No corpus')
            alert.setText('You have not yet loaded a corpus, so no search can be performed.')
            alert.exec_()
            return

        if searchType == 'transcriptions':
            dialog = TranscriptionSearchDialog(self.corpus, self.recentTranscriptionSearches,
                                               self.transcriptionSearchBlankOption, self.transcriptionSearchWildcard)
        elif searchType == 'phrases':
            dialog = PhraseSearchDialog(self.corpus, self.recentPhraseSearches)

        elif searchType == 'gloss':
            dialog = GlossSearchDialog(self.corpus)

        dialog.exec_()
        if not dialog.accepted:
            return


        if searchType == 'transcriptions':
            matches = self.corpus.regExSearch(dialog.regularExpressions)
            search = RecentSearch(dialog.transcriptions, dialog.regularExpressions, matches)
            self.recentTranscriptionSearches.appendleft(search)
            self.transcriptionSearchBlankOption = dialog.blankValue
            self.transcriptionSearchWildcard = dialog.wildcard
        elif searchType == 'phrases':
            matches = self.corpus.regExSearch(dialog.regularExpressions)
            search = RecentSearch(dialog.phrases, dialog.regularExpressions, matches)
            self.recentPhraseSearches.appendleft(search)
        elif searchType == 'gloss':
            if dialog.searchWord in self.corpus: #this is a case-insensitive search
                self.loadHandShape(dialog.searchWord)
                return
            else:
                matches = False

        if matches:
            remove = list()
            attrs = GLOBAL_OPTIONS
            for i,match in enumerate(matches):
                if any(getattr(dialog, attr)!= getattr(match, attr)for attr in attrs):
                    remove.append(i)
            matches = [matches[i] for i in range(len(matches)) if not i in remove]


            resultsDialog = SearchResultsDialog(matches)
            resultsDialog.exec_()
            if resultsDialog.result:
                self.loadHandShape(resultsDialog.result)
        else:
            alert = QMessageBox()
            alert.setWindowTitle('Search results')
            alert.setText('No matches were found in your corpus.')
            alert.exec_()

    def autoFillTranscription(self):
        dialog = AutoFillDialog()
        dialog.exec_()
        if not dialog.accepted:
            return

        currentTranscriptions = self.getTranscriptions()
        if any(not t.isEmpty() for t in currentTranscriptions):
            alert = QMessageBox()
            alert.setWindowTitle('Warning')
            alert.setText('This autofill operation may overwrite a portion of your existing transcription.')
            alert.setInformativeText('Do you want to continue?')
            alert.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
            choice = alert.exec_()
            if choice == QMessageBox.Cancel:
                return

        mapping = {'config1hand1': (0, 'hand1Transcription'),
                   'config1hand2': (0, 'hand2Transcription'),
                   'config2hand1': (1, 'hand1Transcription'),
                   'config2hand2': (1, 'hand2Transcription')}
        for confighand in mapping:
            widgetnum, attribute_name = mapping[confighand]
            if any(x is not None for x in dialog.transcriptions[confighand]):
                current = currentTranscriptions[0]
                for slot, symbol in enumerate(dialog.transcriptions[confighand]):
                    if symbol is not None:
                        getattr(self.configTabs.widget(widgetnum), attribute_name)[slot].setText(symbol)

    def PredefinedHandshapeDialogClosed(self, event):
        item1 = self.configTabs.widget(0).hand1Transcription.lineLayout.takeAt(0)
        w1 = item1.widget()
        w1.deleteLater()

        item2 = self.configTabs.widget(0).hand2Transcription.lineLayout.takeAt(0)
        w2 = item2.widget()
        w2.deleteLater()

        item3 = self.configTabs.widget(1).hand1Transcription.lineLayout.takeAt(0)
        w3 = item3.widget()
        w3.deleteLater()

        item4 = self.configTabs.widget(1).hand2Transcription.lineLayout.takeAt(0)
        w4 = item4.widget()
        w4.deleteLater()

        self.selected.deleteLater()

    def predefinedTranscription(self):
        handshapeDialog = PredefinedHandshapeDialog(parent=self)
        handshapeDialog.closeSignal.connect(self.PredefinedHandshapeDialogClosed)
        handshapeDialog.show()

        # Push button at the beginning for predefined handshapes
        self.selected = QButtonGroup()
        self.config1hand1selection = QRadioButton()
        self.config1hand1selection.setToolTip('Select for predefined handshapes')
        self.config1hand1selection.setChecked(True)
        self.config1hand2selection = QRadioButton()
        self.config1hand2selection.setToolTip('Select for predefined handshapes')
        self.config2hand1selection = QRadioButton()
        self.config2hand1selection.setToolTip('Select for predefined handshapes')
        self.config2hand2selection = QRadioButton()
        self.config2hand2selection.setToolTip('Select for predefined handshapes')
        self.selected.addButton(self.config1hand1selection)
        self.selected.addButton(self.config1hand2selection)
        self.selected.addButton(self.config2hand1selection)
        self.selected.addButton(self.config2hand2selection)
        self.selected.setId(self.config1hand1selection, 1)
        self.selected.setId(self.config1hand2selection, 2)
        self.selected.setId(self.config2hand1selection, 3)
        self.selected.setId(self.config2hand2selection, 4)

        self.configTabs.widget(0).hand1Transcription.lineLayout.insertWidget(0, self.config1hand1selection)
        self.configTabs.widget(0).hand2Transcription.lineLayout.insertWidget(0, self.config1hand2selection)
        self.configTabs.widget(1).hand1Transcription.lineLayout.insertWidget(0, self.config2hand1selection)
        self.configTabs.widget(1).hand2Transcription.lineLayout.insertWidget(0, self.config2hand2selection)

    def mergeCorpus(self):
        if self.corpus is None:
            alert = QMessageBox()
            alert.setWindowTitle('No corpus loaded')
            alert.setText('You must have a corpus already loaded in order to merge.')
            alert.exec_()
            return

        dialog = MergeCorpusDialog()
        dialog.exec_()

        if dialog.filename:
            corpus2 = load_binary(dialog.filename)
            for sign in corpus2:
                if sign.gloss in self.corpus:
                    alert = MergeCorpusMessageBox()
                    alert.setText(alert.baseText.format(sign.gloss))
                    alert.exec_()
                else:
                    self.corpus.addWord(sign)
            save_binary(self.corpus, self.corpus.path)
            currentGloss = self.currentGloss()
            self.setupNewCorpus()

            for n in range(self.corpusList.count()):
                item = self.corpusList.item(n)
                if item.text() == currentGloss:
                    self.corpusList.setCurrentRow(n)
                    break
            else:
                self.corpusList.setCurrentRow(0)

    def createActions(self):

        self.mergeCorpusAct = QAction('&Merge corpus...',
                                self,
                                triggered = self.mergeCorpus)

        #self.funcloadAct = QAction('Calculate functional load...',
        #                           self,
        #                           triggered = self.funcLoad)

        self.copyAct = QAction('&Copy a transcription...',
                              self,
                              triggered = self.copyTranscription)

        self.pasteAct = QAction('&Paste a transcription...',
                                self,
                                triggered = self.pasteTranscription)

        self.autofillAct = QAction('&Autofill transcription slots...',
                               self,
                               triggered = self.autoFillTranscription)

        #self.predefineAct = QAction('&Open predefined handshapes...',
        #                            self,
        #                            triggered=self.predefineTranscription)

        #self.glossSearchAct = QAction('Search by &gloss...',
        #                              self,
        #                              triggered = lambda x: self.searchCorpus(searchType = 'gloss'))

        #self.transcriptionSearchAct = QAction('Search by &transcription...',
        #                                      self,
        #                                      triggered = lambda x: self.searchCorpus(searchType = 'transcriptions'))

        #self.phraseSearchAct = QAction('Search by descriptive &phrase...',
        #                               self,
        #                               triggered = lambda x: self.searchCorpus(searchType = 'phrases'))

        self.overwriteAllGlossesAct = QAction('Resave all glosses in new style',
                                              self,
                                              triggered = self.overwriteAllGlosses)

        self.printCorpusObjectAct = QAction('Print corpus.__dict__',
                                         self,
                                         triggered = self.printCorpusObject)

        self.importCorpusAct = QAction('&Import corpus from csv...',
                                       self,
                                       statusTip = 'Import from csv file',
                                       triggered = self.importCorpus)

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

        self.forceCompatibilityUpdateAct = QAction('Force compatibility update',
                                               self,
                                               triggered = self.forceComptibilityUpdate)

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

        self.saveCorpusAct = QAction( "&Save current word",
                self,
                statusTip="Save current word and update corpus",
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
                                         statusTip='Open a notepad for information about the corpus',
                                         triggered=self.addCorpusNotes)
        self.editCoderAct = QAction('Edit coder...',
                                    self,
                                    statusTip='Edit the name for the default coder',
                                    triggered=self.editCoder)
        #self.addSignNotesAct = QAction('Edit &sign notes...',
        #                               self,
        #                               statusTip='Open a notepad for information about the current sign',
        #                               triggered=self.addSignNotes)

        self.switchAct = QAction('Switch to analyzer mode',
                                 self,
                                 statusTip='Switch to analyzer mode',
                                 triggered=self.switchMode)

    def editCoder(self):
        coder = CoderDialog(self.coder, parent=self)
        success = coder.exec_()
        if success:
            self.coder = coder.coderName

    def switchMode(self):
        if self.corpus is None:
            reply = QMessageBox.critical(self, 'Missing corpus',
                                         'There is no corpus loaded. Please load a corpus before switching'
                                         'to the analyzer mode.')
            return

        self.writeSettings()
        self.close()
        self.analyzer = AnalyzerMainWindow(self.corpus)
        self.analyzer.show()

    def forceComptibilityUpdate(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open Corpus File', os.getcwd(), '*.corpus')
        file_path = file_path[0]
        if not file_path:
            return
        self.corpus = load_binary(file_path)
        self.corpus.path = file_path
        self.checkBackwardsComptibility(forceUpdate=True)
        save_binary(self.corpus, self.corpus.path)
        alert = QMessageBox()
        alert.setText('Corpus updated!')
        alert.exec_()


    def initCorpusNotes(self):
        self.corpusNotes = NotesDialog()
        if self.corpus is None:
            title = 'Notes for unnamed corpus'
        else:
            title = 'Notes for {} corpus'.format(self.corpus.name)
        self.corpusNotes.setWindowTitle(title)

    #def initSignNotes(self):
    #    self.signNotes = NotesDialog()
    #    if self.gloss.text():
    #        self.signNotes.setWindowTitle('Notes for the sign {}'.format(self.gloss.text()))
    #    else:
    #        self.signNotes.setWindowTitle('Notes for an unglossed sign')

    def addCorpusNotes(self):
        if self.corpus is None:
            self.corpusNotes.setWindowTitle('Notes for unnamed corpus')
        else:
            self.corpusNotes.setWindowTitle('Notes for {} corpus'.format(self.corpus.name))
        self.corpusNotes.show()
        self.corpusNotes.raise_()
        self.askSaveChanges = True

    #def addSignNotes(self):
    #    if self.gloss.text():
    #        self.signNotes.setWindowTitle('Notes for the sign {}'.format(self.gloss.text()))
    #    else:
    #        self.signNotes.setWindowTitle('Notes for an unglossed sign')
    #    self.signNotes.show()
    #    self.signNotes.raise_()
    #    self.askSaveChanges = True

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

        if not self.corpus:
            alert = QMessageBox()
            alert.setWindowTitle('No corpus')
            alert.setText('You must save the current word to a corpus before you can export it.')
            alert.exec_()
            return

        dialog = ExportCorpusDialog()
        results = dialog.exec_()

        if results:
            path = dialog.fileNameEdit.text()
            include_fields = dialog.includeFields.isChecked()
            blank_space = dialog.blankSpaceText
            x_in_box = dialog.xinboxEdit.text()
            null = dialog.nullEdit.text()
            if not blank_space:
                blank_space = ''
            kwargs = {'include_fields': include_fields,
                      'blank_space': blank_space,
                      'parameter_format': dialog.parameterFormat}
            if x_in_box:
                kwargs['x_in_box'] = x_in_box
            if null:
                kwargs['null'] = null
            #output = [word.export(**kwargs) for word in self.corpus]
            try:
                with open(path, encoding='utf-8', mode='w') as f:
                    print(Sign.headers, file=f)
                    for sign in self.corpus:
                        kwargs['sign'] = sign
                        output = self.getSignDataForExport(**kwargs)
                        print(output, file=f)
                if self.showSaveAlert:
                    QMessageBox.information(self, 'Success', 'Corpus successfully exported!')
            except PermissionError:
                filename = os.path.split(path)[-1]
                alert = QMessageBox()
                alert.setWindowTitle('Error encountered')
                alert.setText('The file {} is already open in a program on your computer. Please close the file before '
                              'saving, or else choose a different file name.'.format(filename))
                alert.exec_()

    @classmethod
    def getSignDataForExport(self, sign=None, include_fields=False, blank_space='_',
                             x_in_box=X_IN_BOX, null=NULL, parameter_format='xml'):
        def add_fields(transcription):
            transcription = '[{}]1[{}]2[{}]3[{}]4[{}]5[{}]6[{}]7'.format(transcription[0],
                                                                         ''.join(transcription[1:5]),
                                                                         ''.join(transcription[5:15]),
                                                                         ''.join(transcription[15:19]),
                                                                         ''.join(transcription[19:24]),
                                                                         ''.join(transcription[24:29]),
                                                                         ''.join(transcription[29:34]))
            return transcription

        output = list()
        output.append(sign.gloss)
        for config_num in [1, 2]:
            for hand_num in [1, 2]:
                hand = getattr(sign, 'config{}hand{}'.format(config_num, hand_num))
                if hand[0] == '_' or not hand[0]:
                    hand[0] = blank_space
                else:
                    hand[0] = 'V'
                transcription = [x if x else blank_space for x in hand]
                transcription[7] = null
                if transcription[19] == X_IN_BOX:
                    transcription[19] = x_in_box
                if transcription[24] == X_IN_BOX:
                    transcription[24] = x_in_box
                if transcription[29] == X_IN_BOX:
                    transcription[29] = x_in_box
                if include_fields:
                    transcription = add_fields(transcription)
                output.append(''.join(transcription))

        for config_num in [1, 2]:
            for hand_num in [1, 2]:
                slot_list = getattr(sign, 'config{}hand{}'.format(config_num, hand_num))
                for slot_num in range(34):
                    symbol = slot_list[slot_num]
                    if symbol == X_IN_BOX:
                        symbol = x_in_box
                    if symbol == NULL:
                        symbol = null
                    output.append(symbol)

                uncertain, estimates = list(), list()
                key_name = 'config{}hand{}'.format(config_num, hand_num)
                for i, flag in enumerate(sign.flags[key_name]):
                    if flag.isUncertain:
                        uncertain.append(str(i + 1))
                    if flag.isEstimate:
                        estimates.append(str(i + 1))
                uncertain = 'None' if not uncertain else '-'.join(uncertain)
                estimates = 'None' if not estimates else '-'.join(estimates)
                output.append(uncertain)
                output.append(estimates)
        for option in GLOBAL_OPTIONS:
            output.append('True' if getattr(sign, option) else 'False')
        notes = ''.join([n.replace('\n', '  ').replace('\t', '    ') for n in sign.notes])
        output.append(notes)
        if parameter_format == 'xml':
            outputParameters = parameters.exportXML(sign.parameters)
        elif parameter_format == 'txt':
            outputParameters = parameters.exportTree(sign.parameters)
        elif parameter_format == 'none':
            outputParameters = ' '
        output.append(outputParameters)
        output = '\t'.join(output)

        return output

    def importCorpus(self):
        if self.corpus is not None:
            alert = QMessageBox()
            alert.setWindowTitle('Warning')
            alert.setText(('You currently have an open corpus, and you will lose any unsaved changes. '
                            'What would you like to do?'))
            alert.addButton('Return to corpus', QMessageBox.NoRole)
            alert.addButton('Continue', QMessageBox.YesRole)
            alert.exec_()
            if alert.buttonRole(alert.clickedButton()) == QMessageBox.NoRole:
                return
        filepath = QFileDialog.getOpenFileName(self, 'Import Corpus from CSV', os.getcwd(), '*.csv')
        filepath = filepath[0]
        if not filepath:
            return
        filepath, filename = os.path.split(filepath)
        filename = filename.split('.')[0]

        corpora = [f for f in os.listdir(filepath) if f.endswith('.corpus')]
        for c in corpora:
            if c.split('.')[0] == filename:
                showAlert = True
                break
        else:
            showAlert = False

        if showAlert:
            alert = QMessageBox()
            alert.setWindowTitle('Warning')
            alert.setText('The current folder already contains a corpus called \"{}\". To avoid overwriting this file, '
                          'your imported corpus will be called \"{}-import\". You can rename your corpus in '
                          'SLPAnnotator by selecting File > Save as...\n\n'
                          'What do you want to do?'.format(filename, filename))

            alert.addButton('Import CSV file', QMessageBox.AcceptRole)
            alert.addButton('Cancel', QMessageBox.RejectRole)
            alert.exec_()
            if alert.buttonRole(alert.clickedButton()) == QMessageBox.RejectRole:
                return

        if showAlert:
            corpus = Corpus({'name':filename+'-import', 'path': os.path.join(filepath, filename+'-1.corpus')})
        else:
            corpus = Corpus({'name': filename, 'path':os.path.join(filepath, filename+'.corpus')})

        with open(os.path.join(filepath, filename+'.csv'), mode='r', encoding='utf-8') as f:
            headers = f.readline().strip()
            headers = headers.split('\t')
            #print('headers', headers)
            start = f.tell()
            #print('start', start)
            firstline = f.readline()
            #print('firstline', firstline)
            params = firstline.split('\t')[-1].strip()
            verfied, useDefaultParameters = self.verifyParametersForImport(params)
            if not verfied:
                return
            f.seek(start)

            for line in f:
                line = line.strip()
                line = line.split('\t')
                data = {h:l for (h,l) in zip(headers, line)}
                kwargs = dict()
                flags = dict()
                transcriptions = [ [[None for n in range(34)], [None for n in range(34)]],
                                   [[None for n in range(34)], [None for n in range(34)]] ]
                for config in [1, 2]:
                    for hand in [1, 2]:
                        for n in range(1,35):
                            name = 'config{}hand{}slot{}'.format(config, hand, n)
                            transcriptions[config-1][hand-1][n-1] = data[name]

                        uncertain = data['config{}hand{}uncertain'.format(config, hand)]
                        if uncertain == 'None':
                            uncertain = list()
                        else:
                            uncertain = [int(n) for n in uncertain.split('-')]

                        estimated = data['config{}hand{}estimated'.format(config, hand)]
                        if estimated == 'None':
                            estimated = list()
                        else:
                            estimated = [int(n) for n in estimated.split('-')]

                        confighand = 'config{}hand{}'.format(config, hand)
                        flags[confighand] = [Flag(True if n in uncertain else False, True if n in estimated else False)
                                             for n in range(34)]
                kwargs['config1'] = transcriptions[0]
                kwargs['config2'] = transcriptions[1]
                kwargs['flags'] = flags
                kwargs['gloss'] = data['gloss']
                for option in GLOBAL_OPTIONS:  #GLOBAL_OPTIONS = ['forearm', 'estimated', 'uncertain', 'incomplete']
                    kwargs[option] = True if data[option] == 'True' else False
                if useDefaultParameters:
                    model = ParameterTreeModel(parameters.defaultParameters)
                else:
                    model = ParameterTreeModel(data['parameters'], fromXML=True)
                kwargs['parameters'] = model.params
                kwargs['signNotes'] = '' if data['notes'] == 'None' else data['notes']
                sign = Sign(kwargs)
                corpus.addWord(sign)
        self.corpus = corpus
        self.setupNewCorpus()

    def verifyParametersForImport(self, parameters):
        message = None
        useDefaults = False
        if not parameters:
            message = ('Your corpus was exported without any parameter information.', '')
        else:
            try:
                xmlElementTree.fromstring(parameters)
            except xmlElementTree.ParseError:
                message = ('Your corpus was exported in a format that cannot be re-imported.',
                           'You will lose any existing parameter information.')

        if message is not None:
            alert = QMessageBox()
            alert.setWindowTitle('Loading from csv')
            alert.setText(('There is a problem loading the parameters from your corpus.\n'
                           '{}\n'
                           'If you continue, SLPA will load your corpus with default parameters. {}\n'
                           'What would you like to do?').format(message[0], message[1]))
            load = QPushButton('Load with defaults')
            cancel = QPushButton('Cancel')
            alert.addButton(load, QMessageBox.AcceptRole)
            alert.addButton(cancel, QMessageBox.RejectRole)
            alert.exec_()
            if alert.buttonRole(alert.clickedButton()) == QMessageBox.RejectRole:
                return False, False
            else:
                useDefaults = True

        return True, useDefaults

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
        self.transcriptionRestrictionsChanged.emit(self.restrictedTranscriptions)

        self.parameterDialog.accept()
        self.setupParameterDialog(ParameterTreeModel(parameters.defaultParameters))
        self.transcriptionInfo.clearSignNoteText()
        self.transcriptionInfo.changeCoderName(self.coder)
        #self.initSignNotes()
        for widget in self.globalOptionsWidgets:
            widget.setChecked(False)
        self.askSaveChanges = False
        self.showMaximized()


class GlobalOptionCheckBox(QCheckBox):

    def __init__(self, text, slot):
        super().__init__()
        self.setText(text)
        self.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.clicked.connect(slot)


class MergeCorpusDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Merge corpus')
        layout = QVBoxLayout()

        explanation = QLabel('Select a corpus file to merge into the corpus that you currently have open.\n')
        layout.addWidget(explanation)

        findLayout = QHBoxLayout()
        findButton = QPushButton('Select corpus file...')
        findButton.clicked.connect(self.getFileName)
        self.fileNameEdit = QLineEdit()
        findLayout.addWidget(findButton)
        findLayout.addWidget(self.fileNameEdit)
        layout.addLayout(findLayout)

        buttonLayout = QHBoxLayout()
        ok = QPushButton('OK')
        ok.clicked.connect(self.accept)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def getFileName(self):
        filename = QFileDialog.getOpenFileName(self, 'Merge Corpus Files', os.getcwd(), '*.corpus')
        path = filename[0]
        if not path:
            return
        if not path.endswith('.corpus'):
            path = path + '.corpus'
        self.fileNameEdit.setText(path)

    def accept(self):
        self.filename = self.fileNameEdit.text()
        if not self.filename:
            alert = QMessageBox()
            alert.setWindowTitle('Error')
            alert.setText('You must select a valid corpus file')
            alert.exec_()
            return
        super().accept()

    def reject(self):
        self.filename = None
        super().reject()

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

        blankSpaceLayout = QVBoxLayout()
        blankSpaceLabel = QLabel('How should empty transcription slots be represented in your output?')
        # blankSpaceLabel.setWordWrap(True)
        blankSpaceLayout.addWidget(blankSpaceLabel)

        blankRadioButtonLayout = QHBoxLayout()
        noBlanksOption = QRadioButton('Do not show empty slots in the output')
        blankRadioButtonLayout.addWidget(noBlanksOption)
        blankSpaceOption = QRadioButton('Print a blank space')
        blankRadioButtonLayout.addWidget(blankSpaceOption)
        otherBlankOption = QRadioButton('Print this character: ')
        blankRadioButtonLayout.addWidget(otherBlankOption)
        otherBlankOption.setChecked(True)
        self.blankOptionEdit = QLineEdit()
        self.blankOptionEdit.setMaxLength(1)
        self.blankOptionEdit.setMaximumWidth(30)
        self.blankOptionEdit.setText('_')
        blankRadioButtonLayout.addWidget(self.blankOptionEdit)
        self.blankOptionButtons = QButtonGroup()
        self.blankOptionButtons.addButton(noBlanksOption)
        self.blankOptionButtons.addButton(blankSpaceOption)
        self.blankOptionButtons.addButton(otherBlankOption)
        self.blankOptionButtons.setId(noBlanksOption, 0)
        self.blankOptionButtons.setId(blankSpaceOption, 1)
        self.blankOptionButtons.setId(otherBlankOption, 2)
        otherBlankOption.setChecked(True)
        blankSpaceLayout.addLayout(blankRadioButtonLayout)

        self.includeFields = QCheckBox('Include fields in transcription?')
        self.includeFields.setToolTip('If checked, transcriptions will be delimited by square brackets '
                                  'and numbers representing fields.\n'
                                  'If not checked, transcriptions will be one long string.')

        parametersLayout = QVBoxLayout()
        exportParamsLabel = QLabel('What format should be used for parameters?')
        parametersLayout.addWidget(exportParamsLabel)
        parameterOptionsLayout = QHBoxLayout()
        self.parameterOptions = QButtonGroup()
        plainTextOption = QRadioButton('plain text')
        xmlOption = QRadioButton('xml')
        noParametersOption = QRadioButton('don\'t export parameters')
        parameterOptionsLayout.addWidget(plainTextOption)
        parameterOptionsLayout.addWidget(xmlOption)
        parameterOptionsLayout.addWidget(noParametersOption)
        parameterOptionsLayout.insertSpacing(-1, 100)
        parametersLayout.addLayout(parameterOptionsLayout)
        self.parameterOptions.addButton(plainTextOption)
        self.parameterOptions.addButton(xmlOption)
        self.parameterOptions.addButton(noParametersOption)
        self.parameterOptions.setId(plainTextOption, 0)
        self.parameterOptions.setId(xmlOption, 1)
        self.parameterOptions.setId(noParametersOption, 2)
        xmlOption.setChecked(True)

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
        outputOptionsLayout.addLayout(blankSpaceLayout)
        outputOptionsLayout.addLayout(parametersLayout)
        outputOptionsLayout.addWidget(altSymbolsLabel)
        outputOptionsLayout.addWidget(self.xinboxEdit)
        outputOptionsLayout.addWidget(self.nullEdit)

        noteLabel = QLabel('NOTE: If you are exporting a corpus that you want to re-import into SLP-Annotator, you '
                           'must use the default options (no fields, underscore for blanks, xml parameters, no '
                           'alternative symbols).')
        noteLabel.setWordWrap(True)
        outputOptionsLayout.addWidget(noteLabel)

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
        selectedButton = self.blankOptionButtons.checkedButton()
        id = self.blankOptionButtons.id(selectedButton)
        if id == 0:
            self.blankSpaceText = ''
        elif id == 1:
            self.blankSpaceText = ' '
        elif id == 2:
            if not self.blankOptionEdit.text():
                alert = QMessageBox()
                alert.setWindowTitle('Missing information')
                alert.setText('You selected to replace empty transcription slots with a symbol of your choosing, but no'
                              ' symbol was typed into the text box. Please enter a symbol, or choose a different'
                              ' option.')
                alert.exec_()
                return
            else:
                self.blankSpaceText = self.blankOptionEdit.text()

        selectedButton = self.parameterOptions.checkedButton()
        id = self.parameterOptions.id(selectedButton)
        if id == 0:
            self.parameterFormat = 'txt'
        elif id == 1:
            self.parameterFormat = 'xml'
        else:
            self.parameterFormat = 'none'

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

#TODO: add settings arguments
class AnalyzerMainWindow(QMainWindow):
    def __init__(self, corpus):
        super().__init__()

        self.corpus = corpus
        self.setWindowTitle('SLP-Analyzer')

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QVBoxLayout()
        centralWidget.setLayout(mainLayout)

        wordFrame = QGroupBox(self.corpus.name)
        wordLayout = QVBoxLayout()
        wordFrame.setLayout(wordLayout)
        # mainLayout.addWidget(wordFrame)

        #searchField = QLineEdit()
        #searchField.setPlaceholderText('Search...')
        #wordLayout.addWidget(searchField, alignment=Qt.AlignRight)

        wordList = WordListView()
        wordList.itemClicked.connect(self.loadData)
        wordLayout.addWidget(wordList)
        # wordList.setWindowTitle('Word')

        #model = QStandardItemModel()

        rightFrame = QFrame()
        rightLayout = QVBoxLayout()
        rightFrame.setLayout(rightLayout)
        # mainLayout.addWidget(rightFrame)

        globalFrame = QGroupBox('Global options')
        #globalFrame.setEnabled(False)
        globalLayout = QHBoxLayout()
        globalFrame.setLayout(globalLayout)
        rightLayout.addWidget(globalFrame)
        self.forearmButton = QCheckBox('Forearm')
        self.forearmButton.setEnabled(False)
        globalLayout.addWidget(self.forearmButton)
        self.estimatedButton = QCheckBox('Estimated')
        self.estimatedButton.setEnabled(False)
        globalLayout.addWidget(self.estimatedButton)
        self.uncertainButton = QCheckBox('Uncertain')
        self.uncertainButton.setEnabled(False)
        globalLayout.addWidget(self.uncertainButton)
        self.incompleteButton = QCheckBox('Incomplete')
        self.incompleteButton.setEnabled(False)
        globalLayout.addWidget(self.incompleteButton)

        config1Frame = QGroupBox('Config 1')
        config1Layout = QVBoxLayout()
        config1Frame.setLayout(config1Layout)
        rightLayout.addWidget(config1Frame)

        self.config1 = TranscriptionConfigTab(1, view_only=True)
        config1Layout.addWidget(self.config1)

        config2Frame = QGroupBox('Config 2')
        config2Layout = QVBoxLayout()
        config2Frame.setLayout(config2Layout)
        rightLayout.addWidget(config2Frame)

        self.config2 = TranscriptionConfigTab(2, view_only=True)
        config2Layout.addWidget(self.config2)

        parameterFrame = QGroupBox('Parameter')
        paramLayout = QHBoxLayout()
        parameterFrame.setLayout(paramLayout)
        rightLayout.addWidget(parameterFrame)

        qualityFrame = QGroupBox('Quality')
        paramLayout.addWidget(qualityFrame)
        majorMovementFrame = QGroupBox('Major movement')
        paramLayout.addWidget(majorMovementFrame)
        localMovementFrame = QGroupBox('Local movement')
        paramLayout.addWidget(localMovementFrame)
        majorLocationFrame = QGroupBox('Major location')
        paramLayout.addWidget(majorLocationFrame)
        reduplicationFrame = QGroupBox('Reduplication')
        paramLayout.addWidget(reduplicationFrame)

        splitter = QSplitter()
        splitter.addWidget(wordFrame)
        splitter.addWidget(rightFrame)
        mainLayout.addWidget(splitter)

        for word in self.corpus:
            wordList.addItem(word.gloss)

        wordList.sortItems()
        wordList.setCurrentRow(0)
        wordList.itemClicked.emit(wordList.currentItem())
        # create an item with a caption
        # item = QStandardItem(word.gloss)

        # add a checkbox to it
        # item.setCheckable(True)

        # Add the item to the model
        # model.appendRow(item)
        # =====

        # Apply the model to the list view
        # wordList.setModel(model)

        self.createActions()
        self.createMenu()

    def createMenu(self):
        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(self.loadCorporaAction)
        self.fileMenu.addAction(self.switchAct)

        self.searchMenu = self.menuBar().addMenu('&Search')
        self.searchMenu.addAction(self.searchByTranscriptionAct)
        self.searchMenu.addAction(self.searchByExtendedFingersAct)
        self.searchMenu.addAction(self.searchByHandshapesAct)

    def createActions(self):
        self.loadCorporaAction = QAction('&Load corpora...', self, statusTip='Load a corpus',
                                                   triggered=self.loadCorpora)
        self.switchAct = QAction('Switch to annotator mode',
                                 self,
                                 statusTip='Switch to annotator mode',
                                 triggered=self.switchMode)

        self.searchByTranscriptionAct = QAction('Search by transcription...', self,
                                                triggered=self.searchByTranscription)
        self.searchByExtendedFingersAct = QAction('Search by extended fingers...', self,
                                                  triggered=self.searchByExtendedFingers)
        self.searchByHandshapesAct = QAction('Search by handshapes...', self,
                                             triggered=self.searchByHandshapes)

    def searchByHandshapes(self):
        searchDialog = HandshapeSearchDialog(self.corpus, self, None, None)
        success = searchDialog.exec_()
        if success:
            self.HSResultWindow = ResultsWindow('Handshape Search Results',
                                                searchDialog,
                                                self)
            self.HSResultWindow.show()

    def searchByTranscription(self):
        searchDialog = TranscriptionSearchDialog(self.corpus, self, None, None)
        success = searchDialog.exec_()
        if success:
            self.TSResultWindow = ResultsWindow('Transcription Search Results',
                                                searchDialog,
                                                self)
            self.TSResultWindow.show()

    def searchByExtendedFingers(self):
        searchDialog = ExtendedFingerSearchDialog(self.corpus, self, None, None)
        success = searchDialog.exec_()
        if success:
            self.EFResultWindow = ResultsWindow('Extended Finger Search Results',
                                                searchDialog,
                                                self)
            self.EFResultWindow.show()

    def switchMode(self):
        #pass
        self.close()
        self.annotator = MainWindow()
        self.annotator.corpus = self.corpus
        self.annotator.setupNewCorpus()
        self.annotator.show()

    def loadCorpora(self):
        file_path = QFileDialog.getOpenFileName(self,
                                                'Open Corpus File', os.getcwd(), '*.corpus')

    def loadData(self, item):
        gloss = item.text()
        sign = self.corpus[gloss]

        self.config1.clearAll()
        self.config2.clearAll()

        for confignum, handnum in itertools.product([1, 2], [1, 2]):
            name = 'config{}hand{}'.format(confignum, handnum)
            confighand = sign[name]

            if confignum == 1:
                configTab = self.config1
            else:
                configTab = self.config2

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

        for option in GLOBAL_OPTIONS:
            name = option + 'Button'
            button = getattr(self, name)
            button.setChecked(sign[option])

        #TODO: Set parameters


class WordListView(QListWidget):

    def __init__(self):
        super().__init__()


    def mousePressEvent(self, event):
        #originalItem =  [i for i in self.selectedItems()][0]
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            selectedItem = [i for i in self.selectedItems()][0]
            self.itemClicked.emit(selectedItem)

