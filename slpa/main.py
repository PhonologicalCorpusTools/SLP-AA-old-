import traceback
import itertools
import os
import sys
import subprocess
import collections
from enum import Enum
from imports import *
from handshapes import *
from lexicon import *
from binary import *
from transcriptions import *
from constraints import *
from constraintwidgets import *
#from slpa import __version__ as currentSLPAversion

__currentSLPAversion__ = 0.1
FONT_NAME = 'Arial'
FONT_SIZE = 12
DEFAULT_MAJOR_LOCATIONS = ['', 'Head', 'Arm', 'Trunk', 'Non-dominant', 'Neutral']
DEFAULT_MINOR_LOCATIONS = {'':'',
    'Head': ['Cheek', 'Nose', 'Chin', 'Eye', 'Forehead','Head top', 'Mouth', 'Under chin', 'Upper lip'],
    'Arm': ['Elbow (back)', 'Elbow (front)', 'Forearm (back)', 'Forearm (front)','Forearm (ulnar)',
            'Upper arm','Wrist (back)', 'Wrist (front)'],
    'Trunk': ['Clavicle', 'Hips', 'Neck', 'None specified', 'Shoulder','Torso (bottom)', 'Torso (mid)',
            'Torso (top)', 'Waist'],
    'Non-dominant': ['Finger (back)', 'Finger (front)', 'Finger (radial)','Finger (ulnar)', 'Heel',
            'Palm (front)', 'Palm (back)'],
    'Neutral': ['Neutral', 'Upper head height', 'Mid head height', 'Low head height', 'Neck height', 'Shoulder height',
                'Upper torso height', 'Mid torso height', 'Low torso height', 'Waist height']}
DEFAULT_ONE_HAND_MOVEMENTS = ['','Arc', 'Circular','Straight','Back and forth', 'Multiple', 'Hold']
DEFAULT_TWO_HAND_MOVEMENTS = ['', 'N/A', 'Hold', 'Alternating', 'Simaultaneous']
DEFAULT_ORIENTATIONS = ['','Front', 'Back', 'Side', 'Up', 'Down']
DEFAULT_DISLOCATIONS = ['', 'None', 'Right', 'Left']


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

class FeaturesDialog(QDialog):

    def __init__(self, settings, parent=None):
        super().__init__()
        self.setWindowTitle('Define major feature values')
        self.majorLocations = settings[0]
        self.minorLocations = settings[1]
        oneHandMovements = settings[2]
        twoHandMovements = settings[3]
        orientations = settings[4]
        dislocations = settings[5]

        layout = QVBoxLayout()

        listLayout = QHBoxLayout()

        majorLocationLayout = QVBoxLayout()
        self.majorLocationList = QListWidget()
        for location in sorted(self.majorLocations):
            if not location:
                continue
            self.majorLocationList.addItem(location)
        addMajorLocationButton = QPushButton('Add major location')
        addMajorLocationButton.clicked.connect(self.addMajorLocation)
        removeMajorLocationButton = QPushButton('Remove major location')
        removeMajorLocationButton.clicked.connect(self.removeMajorLocation)
        majorLocationLayout.addWidget(self.majorLocationList)
        majorLocationLayout.addWidget(addMajorLocationButton)
        majorLocationLayout.addWidget(removeMajorLocationButton)

        minorLocationLayout = QVBoxLayout()
        self.minorLocationList = QListWidget()
        major_location = self.majorLocations[0]
        if major_location not in self.minorLocations:
            self.minorLocations[major_location] = ['']
        for location in sorted(self.minorLocations[self.majorLocations[0]]):
            if not location:
                continue
            self.minorLocationList.addItem(location)
        self.minorLocationList.setCurrentRow(0)
        addMinorLocationButton = QPushButton('Add minor location')
        addMinorLocationButton.clicked.connect(self.addMinorLocation)
        removeMinorLocationButton = QPushButton('Remove minor location')
        removeMinorLocationButton.clicked.connect(self.removeMinorLocation)
        minorLocationLayout.addWidget(self.minorLocationList)
        minorLocationLayout.addWidget(addMinorLocationButton)
        minorLocationLayout.addWidget(removeMinorLocationButton)
        self.majorLocationList.currentItemChanged.connect(self.changeMinorList)
        self.majorLocationList.setCurrentItem(self.majorLocationList.item(0))

        oneHandMovementLayout = QVBoxLayout()
        self.oneHandMovementList = QListWidget()
        for oneHandMovement in sorted(oneHandMovements):
            if not oneHandMovement:
                continue
            self.oneHandMovementList.addItem(oneHandMovement)
        self.oneHandMovementList.setCurrentRow(0)
        addOneHandMovementButton = QPushButton('Add one hand movement')
        addOneHandMovementButton.clicked.connect(self.addOneHandMovement)
        removeOneHandMovementButton = QPushButton('Remove one hand movement')
        removeOneHandMovementButton.clicked.connect(self.removeOneHandMovement)
        oneHandMovementLayout.addWidget(self.oneHandMovementList)
        oneHandMovementLayout.addWidget(addOneHandMovementButton)
        oneHandMovementLayout.addWidget(removeOneHandMovementButton)

        twoHandMovementLayout = QVBoxLayout()
        self.twoHandMovementList = QListWidget()
        for twoHandMovement in sorted(twoHandMovements):
            if not twoHandMovement:
                continue
            self.twoHandMovementList.addItem(twoHandMovement)
        self.twoHandMovementList.setCurrentRow(0)
        addTwoHandMovementButton = QPushButton('Add two hand movement')
        addTwoHandMovementButton.clicked.connect(self.addTwoHandMovement)
        removeTwoHandMovementButton = QPushButton('Remove two hand movement')
        removeTwoHandMovementButton.clicked.connect(self.removeTwoHandMovement)
        twoHandMovementLayout.addWidget(self.twoHandMovementList)
        twoHandMovementLayout.addWidget(addTwoHandMovementButton)
        twoHandMovementLayout.addWidget(removeTwoHandMovementButton)


        orientationLayout = QVBoxLayout()
        self.orientationList = QListWidget()
        for orientation in sorted(orientations):
            if not orientation:
                continue
            self.orientationList.addItem(orientation)
        self.orientationList.setCurrentRow(0)
        addOrientationButton = QPushButton('Add orientation')
        addOrientationButton.clicked.connect(self.addOrientation)
        removeOrientationButton = QPushButton('Remove orientation')
        removeOrientationButton.clicked.connect(self.removeOrientation)
        orientationLayout.addWidget(self.orientationList)
        orientationLayout.addWidget(addOrientationButton)
        orientationLayout.addWidget(removeOrientationButton)

        dislocationLayout = QVBoxLayout()
        self.dislocationList = QListWidget()
        for dislocation in sorted(dislocations):
            if not dislocation:
                continue
            self.dislocationList.addItem(dislocation)
        self.dislocationList.setCurrentRow(0)
        addDislocationButton = QPushButton('Add dislocation')
        addDislocationButton.clicked.connect(self.addDislocation)
        removeDislocationButton = QPushButton('Remove dislocation')
        removeDislocationButton.clicked.connect(self.removeDislocation)
        dislocationLayout.addWidget(self.dislocationList)
        dislocationLayout.addWidget(addDislocationButton)
        dislocationLayout.addWidget(removeDislocationButton)

        listLayout.addLayout(majorLocationLayout)
        listLayout.addLayout(minorLocationLayout)
        listLayout.addLayout(oneHandMovementLayout)
        listLayout.addLayout(twoHandMovementLayout)
        listLayout.addLayout(orientationLayout)
        listLayout.addLayout(dislocationLayout)

        layout.addLayout(listLayout)

        buttonLayout = QHBoxLayout()
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)
        restoreDefaultsButtons = QPushButton('Restore defaults')
        restoreDefaultsButtons.clicked.connect(self.restoreDefaultFeatures)
        buttonLayout.addWidget(restoreDefaultsButtons)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        self.cannotRemove = QMessageBox()
        self.cannotRemove.setWindowTitle('Warning')
        self.cannotRemove.setText('This feature cannot be removed.')

        self.removeWarning = QMessageBox()
        self.removeWarning.setWindowTitle('Warning')
        self.removeWarningText = ('This will remove the {} from the list.\n'
                                 'This may cause problems if any signs in your corpus use this feature.\n'
                                 'Are you sure?')
        self.removeWarning.addButton('OK', QMessageBox.AcceptRole)
        self.removeWarning.addButton('Cancel', QMessageBox.RejectRole)

        self.emptyListWarning = QMessageBox()
        self.emptyListWarning.setWindowTitle('Warning')
        self.emptyListWarning.setText(('This feature cannot be deleted. '
                                      'You must have at least one feature in each list.'))

    def restoreDefaultFeatures(self):
        alert = QMessageBox()
        alert.setWindowTitle('Warning')
        alert.setText('This will remove all current features and restore the default values.\n'
                      'Are you sure you want to do this?')
        alert.addButton('OK', QMessageBox.AcceptRole)
        alert.addButton('Cancel', QMessageBox.RejectRole)
        alert.exec_()
        role = alert.buttonRole(alert.clickedButton())
        if role == QMessageBox.RejectRole:
            return

        #the empty string options are not reset here, in order that they not be displayed in the GUI
        #instead, empty string are added in the "if result" clause of MainWindow.defineFeatures()
        self.minorLocations = DEFAULT_MINOR_LOCATIONS
        self.minorLocations.pop('')
        self.minorLocationList.clear()

        self.majorLocations = DEFAULT_MAJOR_LOCATIONS[1:]
        self.majorLocationList.clear()
        for location in sorted(self.majorLocations):
            self.majorLocationList.addItem(location)
        self.majorLocationList.setCurrentRow(0)

        self.oneHandMovements = DEFAULT_ONE_HAND_MOVEMENTS[1:]
        self.oneHandMovementList.clear()
        for movement in sorted(self.oneHandMovements):
            self.oneHandMovementList.addItem(movement)
        self.oneHandMovementList.setCurrentRow(0)

        self.twoHandMovements = DEFAULT_TWO_HAND_MOVEMENTS[1:]
        self.twoHandMovementList.clear()
        for movement in sorted(self.twoHandMovements):
            self.twoHandMovementList.addItem(movement)
        self.twoHandMovementList.setCurrentRow(0)

        self.orientations = DEFAULT_ORIENTATIONS[1:]
        self.orientationList.clear()
        for orientation in sorted(self.orientations):
            self.orientationList.addItem(orientation)
        self.orientationList.setCurrentRow(0)

        self.dislocations = DEFAULT_DISLOCATIONS[1:]
        self.dislocationList.clear()
        for dislocation in sorted(self.dislocations):
            self.dislocationList.addItem(dislocation)
        self.dislocationList.setCurrentRow(0)

    def changeMinorList(self):
        selectedMajorFeature = self.majorLocationList.currentItem()
        if selectedMajorFeature is None:
            return
            #this happens when restoring default values
            #the major list has no items but currentIndexChanged() is still emitted
        name = selectedMajorFeature.text()
        self.minorLocationList.clear()
        try:
            for location in self.minorLocations[name]:
                self.minorLocationList.addItem(location)
            self.minorLocationList.sortItems()
        except KeyError:
            self.minorLocationList.clear()

    def addMajorLocation(self):
        dialog = FeatureEntryDialog()
        result = dialog.exec_()
        if result:
            name = dialog.featureNameEdit.text()
            if name:
                self.majorLocationList.addItem(name)
                self.minorLocations[name] = list()
                self.majorLocationList.setCurrentRow(len(self.majorLocationList)-1)
                self.majorLocationList.sortItems()

    def removeMajorLocation(self):

        listItems = self.majorLocationList.selectedItems()
        feature_name = listItems[0].text()

        if not feature_name:
            self.cannotRemove.exec_()
            return

        if len(self.majorLocationList) == 1:
            self.emptyListWarning.exec_()
            return


        text = 'the major feature \"{}\" and any associated minor features'.format(feature_name)
        self.removeWarning.setText(self.removeWarningText.format(text))
        self.removeWarning.exec_()
        role = self.removeWarning.buttonRole(self.removeWarning.clickedButton())
        if role == QMessageBox.RejectRole:
            return


        for item in listItems:
            self.majorLocationList.takeItem(self.majorLocationList.row(item))
            try:
                del self.minorLocations[item.text()]
            except KeyError:
                pass
        self.majorLocationList.sortItems()
        self.majorLocationList.setCurrentRow(0)

    def addMinorLocation(self):
        dialog = FeatureEntryDialog()
        result = dialog.exec_()
        if result:
            name = dialog.featureNameEdit.text()
            if name:
                self.minorLocationList.addItem(name)
                major = self.majorLocationList.currentItem().text()
                self.minorLocations[major].append(name)
                self.minorLocationList.setCurrentRow(len(self.minorLocationList) - 1)
                self.minorLocationList.sortItems()

    def removeMinorLocation(self):
        if len(self.minorLocationList) == 1:
            self.emptyListWarning.exec_()
            return

        listItems = self.minorLocationList.selectedItems()
        feature_name = listItems[0].text()
        text = 'the minor location \"{}\"'.format(feature_name)
        self.removeWarning.setText(self.removeWarningText.format(text))
        self.removeWarning.exec_()
        role = self.removeWarning.buttonRole(self.removeWarning.clickedButton())
        if role == QMessageBox.RejectRole:
            return


        major = selectedMajorFeature = self.majorLocationList.currentItem().text()
        for item in listItems:
            self.minorLocationList.takeItem(self.minorLocationList.row(item))
            self.minorLocations[major].remove(item.text())
        self.minorLocationList.sortItems()
        self.minorLocationList.setCurrentRow(0)


    def addOneHandMovement(self):
        dialog = FeatureEntryDialog()
        result = dialog.exec_()
        if result:
            name = dialog.featureNameEdit.text()
            if name:
                self.oneHandMovementList.addItem(name)
                self.oneHandMovementList.setCurrentRow(len(self.oneHandMovementList) - 1)
                self.oneHandMovementList.sortItems()

    def addTwoHandMovement(self):
        dialog = FeatureEntryDialog()
        result = dialog.exec_()
        if result:
            name = dialog.featureNameEdit.text()
            if name:
                self.twoHandMovementList.addItem(name)
                self.twoHandMovementList.setCurrentRow(len(self.twoHandMovementList) - 1)
                self.twoHandMovementList.sortItems()

    def removeOneHandMovement(self):
        if len(self.oneHandMovementList) == 1:
            self.emptyListWarning.exec_()
            return

        listItems = self.oneHandMovementList.selectedItems()
        feature_name = listItems[0].text()
        text = 'the one hand movement feature \"{}\"'.format(feature_name)
        self.removeWarning.setText(self.removeWarningText.format(text))
        self.removeWarning.exec_()
        role = self.removeWarning.buttonRole(self.removeWarning.clickedButton())
        if role == QMessageBox.RejectRole:
            return


        for item in listItems:
            self.oneHandMovementList.takeItem(self.oneHandMovementList.row(item))
        self.oneHandMovementList.sortItems()
        self.oneHandMovementList.setCurrentRow(0)

    def removeTwoHandMovement(self):
        if len(self.twoHandMovementList) == 1:
            self.emptyListWarning.exec_()
            return

        listItems = self.twoHandMovementList.selectedItems()
        feature_name = listItems[0].text()
        text = 'the two hand movement feature \"{}\"'.format(feature_name)
        self.removeWarning.setText(self.removeWarningText.format(text))
        self.removeWarning.exec_()
        role = self.removeWarning.buttonRole(self.removeWarning.clickedButton())
        if role == QMessageBox.RejectRole:
            return

        for item in listItems:
            self.twoHandMovementList.takeItem(self.twoHandMovementList.row(item))
        self.twoHandMovementList.sortItems()
        self.twoHandMovementList.setCurrentRow(0)

    def addOrientation(self):
        dialog = FeatureEntryDialog()
        result = dialog.exec_()
        if result:
            name = dialog.featureNameEdit.text()
            if name:
                self.orientationList.addItem(name)
                self.orientationList.setCurrentRow(len(self.orientationList) - 1)
                self.orientationList.sortItems()

    def removeOrientation(self):
        if len(self.orientationList) == 1:
            self.emptyListWarning.exec_()
            return

        listItems = self.orientationList.selectedItems()
        feature_name = listItems[0].text()
        text = 'the orientation feature \"{}\"'.format(feature_name)
        self.removeWarning.setText(self.removeWarningText.format(text))
        self.removeWarning.exec_()
        role = self.removeWarning.buttonRole(self.removeWarning.clickedButton())
        if role == QMessageBox.RejectRole:
            return

        for item in listItems:
            self.orientationList.takeItem(self.orientationList.row(item))
        self.orientationList.sortItems()
        self.orientationList.setCurrentRow(0)

    def addDislocation(self):
        dialog = FeatureEntryDialog()
        result = dialog.exec_()
        if result:
            name = dialog.featureNameEdit.text()
            if name:
                self.dislocationList.addItem(name)
                self.dislocationList.setCurrentRow(len(self.dislocationList) - 1)
                self.dislocationList.sortItems()

    def removeDislocation(self):
        if len(self.dislocationList) == 1:
            self.emptyListWarning.exec_()
            return

        listItems = self.dislocationList.selectedItems()
        feature_name = listItems[0].text()
        text = 'the dislocation feature \"{}\"'.format(feature_name)
        self.removeWarning.setText(self.removeWarningText.format(text))
        self.removeWarning.exec_()
        role = self.removeWarning.buttonRole(self.removeWarning.clickedButton())
        if role == QMessageBox.RejectRole:
            return

        for item in listItems:
            self.dislocationList.takeItem(self.dislocationList.row(item))
        self.dislocationList.sortItems()
        self.dislocationList.setCurrentRow(0)




class FeatureEntryDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Enter new feature name')
        layout = QHBoxLayout()
        self.featureNameEdit = QLineEdit()
        self.okButton = QPushButton('OK')
        self.cancelButton = QPushButton('Cancel')
        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        layout.addWidget(self.featureNameEdit)
        layout.addWidget(self.okButton)
        layout.addWidget(self.cancelButton)
        self.setLayout(layout)


class MajorFeatureLayout(QHBoxLayout):

    def __init__(self, settings):
        super().__init__()

        self.majorLocations = settings[0]
        self.minorLocations = settings[1]
        self.oneHandMovements = settings[2]
        self.twoHandMovements = settings[3]
        self.orientations = settings[4]
        self.dislocations = settings[5]
        self.setContentsMargins(0,0,0,0)
        self.major = QComboBox()
        for location in self.majorLocations:
            self.major.addItem(location)
        self.minor = QComboBox()
        self.oneHandMovement = QComboBox()
        for movement in self.oneHandMovements:
            self.oneHandMovement.addItem(movement)
        self.twoHandMovement = QComboBox()
        for movement in self.twoHandMovements:
            self.twoHandMovement.addItem(movement)

        self.orientation = QComboBox()
        for orientation in self.orientations:
            self.orientation.addItem(orientation)

        self.dislocation = QComboBox()
        for dislocation in self.dislocations:
            self.dislocation.addItem(dislocation)

        self.major.currentIndexChanged.connect(self.changeMinorLocation)
        self.major.setCurrentIndex(0)
        self.changeMinorLocation()

        self.addWidget(QLabel('Major Location'))#, 0, 0)
        self.addWidget(self.major)#, 0, 1)
        self.addWidget(QLabel('Minor Location'))#, 1, 0)
        self.addWidget(self.minor)#, 1, 1)

        self.addWidget(QLabel('One Hand Movement'))#, 0, 2)# 2, 0)
        self.addWidget(self.oneHandMovement)#, 0, 3)#2, 1)
        self.addWidget(QLabel('Two Hand Movement'))#, 1, 2 )#3, 0)
        self.addWidget(self.twoHandMovement)#, 1, 3 )#3, 1)

        self.addWidget(QLabel('Orientation'))#, 0, 4)#4, 0)
        self.addWidget(self.orientation)#, 0, 5)#4, 1)
        self.addWidget(QLabel('Dislocation'))#, 1, 4)#5, 0)
        self.addWidget(self.dislocation)#, 1, 5)#5, 1)

        self.addWidget(QLabel())#, 0, 7) #adds a filler item for spacing
        # self.setColumnStretch(7,1)


    def changeMinorLocation(self):
        majorText = self.major.currentText()
        if not majorText:
            #this is an empty string if the major box has just been cleared because the user
            #updated the FeaturesDialog options
            #this function is incidentally called during this process because the combo boxes are cleared
            return
        self.minor.clear()
        for location in self.minorLocations[majorText]:
            self.minor.addItem(location)

    def reset(self):
        self.major.setCurrentIndex(0)
        self.minor.setCurrentIndex(0)
        self.oneHandMovement.setCurrentIndex(0)
        self.twoHandMovement.setCurrentIndex(0)
        self.orientation.setCurrentIndex(0)
        self.dislocation.setCurrentIndex(0)

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
                getattr(self.hand1Transcription, slot).removeFlag()
                getattr(self.hand2Transcription, slot).removeFlag()

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
        if event.button() == Qt.LeftButton:
            if self.parent.askSaveChanges:
            # if self.askSaveChanges:
                alert = QMessageBox()
                alert.setWindowTitle('Warning')
                alert.setText('Save changes to current entry?')
                alert.addButton('Continue and save', QMessageBox.YesRole)
                alert.addButton('Continue but don\'t save', QMessageBox.NoRole)
                alert.addButton('Go back', QMessageBox.RejectRole)
                result = alert.exec_()
                if alert.buttonRole(alert.clickedButton()) == QMessageBox.YesRole:
                    self.parent.saveCorpus()
                    self.parent.askSaveChanges = False
                elif alert.buttonRole(alert.clickedButton()) == QMessageBox.RejectRole:
                    # self.parent().askSaveChanges = False
                    # index = self.indexFromItem(previous_gloss)
                    # self.corpusList.setCurrentIndex(index)
                    return
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    transcriptionRestrictionsChanged = Signal(bool)

    def __init__(self,app):
        app.messageFromOtherInstance.connect(self.handleMessage)
        super(MainWindow, self).__init__()
        self.setWindowTitle('SLP-Annotator')
        self.setWindowIcon(QIcon(getMediaFilePath('slpa_icon.png')))

        self.createActions()
        self.createMenus()

        # self.restrictedTranscriptions = True
        self.askSaveChanges = False
        self.constraints = dict()
        self.clipboard = list()
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

        # Add major features (location, movement, orientation, dislocation)
        self.featuresLayout = MajorFeatureLayout([self.majorLocations, self.minorLocations,
                                                  self.oneHandMovements, self.twoHandMovements,
                                                  self.orientations, self.dislocations])
        self.featuresLayout.major.currentTextChanged.connect(self.userMadeChanges)
        self.featuresLayout.minor.currentTextChanged.connect(self.userMadeChanges)
        self.featuresLayout.oneHandMovement.currentTextChanged.connect(self.userMadeChanges)
        self.featuresLayout.orientation.currentTextChanged.connect(self.userMadeChanges)
        layout.addLayout(self.featuresLayout)

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

        self.makeCorpusDock()

        self.showMaximized()
        #self.setFixedSize(self.size())
        self.defineTabOrder()

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
        dialog = TranscriptionCopyDialog(transcriptions)
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
        self.setTabOrder(self.configTabs.widget(1).hand2Transcription[-1],
                         self.featuresLayout.major)
        self.setTabOrder(self.featuresLayout.major, self.featuresLayout.minor)
        self.setTabOrder(self.featuresLayout.minor, self.featuresLayout.oneHandMovement)
        self.setTabOrder(self.featuresLayout.oneHandMovement, self.featuresLayout.orientation)

    def writeSettings(self):
        self.settings = QSettings('UBC Phonology Tools', application='SLP-Annotator')
        self.settings.beginGroup('constraints')
        for c in MasterConstraintList:
            name = c[0]
            self.settings.setValue(name, self.constraints[name])
        self.settings.endGroup()

        self.settings.beginGroup('transcriptions')
        self.settings.setValue('restrictedTranscriptions', self.setRestrictionsAct.isChecked())
        self.settings.endGroup()

        self.settings.beginGroup('features')
        self.settings.setValue('majorLocations', self.majorLocations)
        self.settings.setValue('minorLocations', self.minorLocations)
        self.settings.setValue('oneHandMovements', self.oneHandMovements)
        self.settings.setValue('twoHandMovements', self.twoHandMovements)
        self.settings.setValue('orientations', self.orientations)
        self.settings.setValue('dislocations', self.dislocations)
        self.settings.endGroup()

    def readSettings(self):
        self.settings = QSettings('UBC Phonology Tools', application='SLP-Annotator')
        self.settings.beginGroup('constraints')
        for c in MasterConstraintList:
            name = c[0]
            self.constraints[name] = self.settings.value(name, type=bool)
        self.settings.endGroup()

        self.settings.beginGroup('transcriptions')
        self.restrictedTranscriptions = self.settings.value('restrictedTranscriptions', type=bool)
        self.setRestrictionsAct.setChecked(self.restrictedTranscriptions)
        self.transcriptionRestrictionsChanged.emit(self.restrictedTranscriptions)
        self.settings.endGroup()

        self.settings.value

        self.settings.beginGroup('features')
        self.majorLocations = self.settings.value('majorLocations', defaultValue=DEFAULT_MAJOR_LOCATIONS)
        self.minorLocations = self.settings.value('minorLocations', defaultValue=DEFAULT_MINOR_LOCATIONS)
        self.oneHandMovements = self.settings.value('oneHandMovements', defaultValue=DEFAULT_ONE_HAND_MOVEMENTS)
        self.twoHandMovements = self.settings.value('twoHandMovements',defaultValue=DEFAULT_TWO_HAND_MOVEMENTS)
        self.orientations = self.settings.value('orientations', defaultValue=DEFAULT_ORIENTATIONS)
        self.dislocations = self.settings.value('dislocations', defaultValue=DEFAULT_DISLOCATIONS)
        self.settings.endGroup()

    def closeEvent(self, e):
        if self.askSaveChanges:
            alert = QMessageBox()
            alert.setWindowTitle('Warning')
            alert.setText('You have unsaved changes that will be lost if you quit.\n What would you like to do?')
            alert.addButton('Save and quit', QMessageBox.AcceptRole)
            alert.addButton('Quit without saving' , QMessageBox.RejectRole)
            alert.addButton('Go back', QMessageBox.NoRole)
            alert.exec_()
            role = alert.buttonRole(alert.clickedButton())
            if role == QMessageBox.AcceptRole:
                result = self.saveCorpus()
                if result is None:
                    return
            elif role == QMessageBox.RejectRole:
                pass
            elif role == QMessageBox.NoRole:
                return
        self.writeSettings()
        try:
            os.remove(os.path.join(os.getcwd(),'handCode.txt'))
        except FileNotFoundError:
            pass
        #super().closeEvent(QCloseEvent())
        self.close()

    def checkBackwardsComptibility(self):
        word = self.corpus.randomWord()
        for attribute in Sign.sign_attributes:
            if not hasattr(word, attribute):
                break
        else:
            return

        for word in self.corpus:
            for attribute, default_value in Sign.sign_attributes.items():
                if not hasattr(word, attribute):
                    setattr(word, attribute, default_value)

            if hasattr(word, 'movement'):
                setattr(word, 'oneHandMovement', word.movement)
                del word.movement

        save_binary(self.corpus, self.corpus.path)
        self.corpus = load_binary(self.corpus.path)


    def checkTranscription(self):
        dialog = ConstraintCheckMessageBox(self.constraints, self.configTabs, self.featuresLayout)
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
        blenderPath = r'C:\Program Files\Blender Foundation\Blender\blender.exe'
        if not os.path.exists(blenderPath):
            blenderPath = r'C:\Program Files (x86)\Blender Foundation\Blender\blender.exe'
        if not os.path.exists(blenderPath):
            blenderPath = '~/Applications/blender.app'
        blenderFile = os.path.join(os.getcwd(), 'handForPCT.blend')
        blenderScript = os.path.join(os.getcwd(), 'position_hand.py')

        code = self.configTabs.widget(0).hand1Transcription.blenderCode()

        # if os.path.exists(os.path.join(os.getcwd(), 'handCode.txt')):
        #     #check if the existing code matches the current transcription
        #     #if so, just load the most recent image, don't render a second time
        #     with open(os.path.join(os.getcwd(), 'handCode.txt'), encoding='utf-8') as file:
        #         old_code = file.read()
        #         old_code = old_code.strip()
        #         print(code)
        #         print(old_code)
        #     if old_code == code:
        #         self.blenderDialog = BlenderOutputWindow('hand_output.png')
        #         self.blenderDialog.show()
        #         self.blenderDialog.raise_()
        #         return

        with open(os.path.join(os.getcwd(), 'handCode.txt'), mode='w', encoding='utf-8') as f:
            f.write(code)

        proc = subprocess.Popen(
            [blenderPath,
              blenderFile,
             '--background',
              "--python", blenderScript])
        proc.communicate()
        self.blenderDialog = BlenderOutputWindow('hand_output.png', self.gloss.glossEdit.text())
        self.blenderDialog.show()
        self.blenderDialog.raise_()

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
        self.corpusList.currentItemChanged.connect(self.loadHandShape)
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
        self.checkBackwardsComptibility()
        for sign in self.corpus:
            self.corpusList.addItem(sign.gloss)
        self.corpusList.sortItems()

        #self.showMaximized()

    def saveCorpus(self, event=None, checkForEmptyGloss=True):
        isDuplicate = False
        if not self.gloss.glossEdit.text() and checkForEmptyGloss:
            alert = QMessageBox()
            alert.setWindowTitle('Missing gloss')
            alert.setText('Please enter a gloss before saving')
            alert.exec_()
            return

        kwargs = self.generateKwargs()
        if self.corpus is None:
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

            elif role == 0: #load existing corpus and add to it
                self.loadCorpus()
                if self.corpus is None:
                    # corpus will be None if the user opened a file dialog, then changed their mind and cancelled
                    return

        else: #corpus exists
            kwargs['path'] = self.corpus.path
            kwargs['file_mode'] = 'a'
            if kwargs['gloss'] in self.corpus.wordlist:
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
        QMessageBox.information(self, 'Success', 'Corpus successfully updated!')
        return True

    def updateCorpus(self, kwargs, isDuplicate=False):
        sign = Sign(kwargs)
        self.corpus.addWord(sign)
        if not isDuplicate:
            self.corpusList.addItem(kwargs['gloss'])
            self.corpusList.sortItems()

            for row in range(self.corpusList.count()):
                if self.corpusList.item(row).text() == kwargs['gloss']:
                    self.corpusList.setCurrentRow(row)
                    break
        save_binary(self.corpus, kwargs['path'])
        self.askSaveChanges = False

    def newCorpus(self):
        self.corpus = None
        self.newGloss()
        self.corpusList.clear()
        self.askSaveChanges = False

    def loadHandShape(self, gloss, previous_gloss=None):
        gloss = '' if not gloss else gloss.text()
        # gloss = gloss.text()
        sign = self.corpus[gloss]
        self.gloss.glossEdit.setText(sign['gloss'])
        config1 = self.configTabs.widget(0)
        config2 = self.configTabs.widget(1)
        config1.clearAll()
        config2.clearAll()

        handconfig = 'config1hand1'
        config1hand1 = sign[handconfig]
        for slot in config1.hand1Transcription.slots:
            if slot.num == 1:
                if config1hand1[0] == '_' or not config1hand1[0]:
                    slot.setChecked(False)
                else:
                    slot.setChecked(True)
            else:
                text = config1hand1[slot.num-1]
                slot.setText('' if text == '_' else text)
                if sign['flags'][handconfig][slot.num-1]:
                    slot.addFlag()
                else:
                    slot.removeFlag()

        handconfig = 'config1hand2'
        config1hand2 = sign[handconfig]
        for slot in config1.hand2Transcription.slots:
            if slot.num == 1:
                if config1hand2[0] == '_' or not config1hand2[0]:
                    slot.setChecked(False)
                else:
                    slot.setChecked(True)
            else:
                text = config1hand2[slot.num-1]
                slot.setText('' if text == '_' else text)
                if sign['flags'][handconfig][slot.num-1]:
                    slot.addFlag()
                else:
                    slot.removeFlag()


        handconfig = 'config2hand1'
        config2hand1 = sign[handconfig]
        for slot in config2.hand1Transcription.slots:
            if slot.num == 1:
                if config2hand1[0] == '_' or not config2hand1[0]:
                    slot.setChecked(False)
                else:
                    slot.setChecked(True)
            else:
                text = config2hand1[slot.num-1]
                slot.setText('' if text == '_' else text)
                if sign['flags'][handconfig][slot.num-1]:
                    slot.addFlag()
                else:
                    slot.removeFlag()

        handconfig = 'config2hand2'
        config2hand2 = sign[handconfig]
        for slot in config2.hand2Transcription.slots:
            if slot.num == 1:
                if config2hand2[0] == '_' or not config2hand2[0]:
                    slot.setChecked(False)
                else:
                    slot.setChecked(True)
            else:
                text = config2hand2[slot.num-1]
                slot.setText('' if text == '_' else text)
                if sign['flags'][handconfig][slot.num-1]:
                    slot.addFlag()
                else:
                    slot.removeFlag()

        for name in ['major', 'minor', 'oneHandMovement', 'twoHandMovement', 'orientation', 'dislocation']:
            widget = getattr(self.featuresLayout, name)
            index = widget.findText(sign[name])
            if index == -1:
                index = 0
            widget.setCurrentIndex(index)
        self.askSaveChanges = False

    def generateKwargs(self):
        #This is called whenever the corpus is updated/saved
        kwargs = {'path': None, 'file_mode': None,
                'config1': None, 'config2': None,
                'major': None, 'minor': None,
                'oneHandMovement': None, 'twoHandMovement': None,
                'orientation': None, 'dislocation': None,
                'flags': None}
        config1 = self.configTabs.widget(0)#.findChildren(TranscriptionLayout)
        kwargs['config1'] = [config1.hand1(), config1.hand2()]

        config2 = self.configTabs.widget(1)#.findChildren(TranscriptionLayout)
        kwargs['config2'] = [config2.hand1(), config2.hand2()]

        gloss = self.gloss.glossEdit.text().strip()
        kwargs['gloss'] = gloss

        major = self.featuresLayout.major.currentText()
        kwargs['major'] = 'None' if not major else major

        minor = self.featuresLayout.minor.currentText()
        kwargs['minor'] = 'None' if not minor else minor

        oneHandMovement = self.featuresLayout.oneHandMovement.currentText()
        kwargs['oneHandMovement'] = 'None' if not oneHandMovement else oneHandMovement

        twoHandMovement = self.featuresLayout.twoHandMovement.currentText()
        kwargs['twoHandMovement'] = 'None' if not twoHandMovement else twoHandMovement

        orientation = self.featuresLayout.orientation.currentText()
        kwargs['orientation'] = 'None' if not orientation else orientation

        dislocation = self.featuresLayout.dislocation.currentText()
        kwargs['dislocation'] = 'None' if not dislocation else dislocation

        flags = {'config1hand1': self.configTabs.widget(0).hand1Transcription.flagList,
                 'config1hand2': self.configTabs.widget(0).hand2Transcription.flagList,
                 'config2hand1': self.configTabs.widget(1).hand1Transcription.flagList,
                 'config2hand2': self.configTabs.widget(1).hand2Transcription.flagList}
        kwargs['flags'] = flags
        return kwargs

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&Menu")
        self.fileMenu.addAction(self.newCorpusAct)
        self.fileMenu.addAction(self.loadCorpusAct)
        self.fileMenu.addAction(self.saveCorpusAct)
        self.fileMenu.addAction(self.newGlossAct)
        self.fileMenu.addAction(self.exportCorpusAct)
        self.fileMenu.addAction(self.quitAct)
        self.settingsMenu = self.menuBar().addMenu('&Settings')
        self.settingsMenu.addAction(self.setRestrictionsAct)
        self.settingsMenu.addAction(self.setConstraintsAct)
        self.featuresMenu = self.menuBar().addMenu('&Features')
        self.featuresMenu.addAction(self.defineFeaturesAct)

    def createActions(self):

        self.newCorpusAct = QAction('&New corpus',
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
                statusTip="Quit", triggered=self.closeEvent)

        self.exportCorpusAct = QAction('&Export corpus as csv',
                                    self,
                                    statusTip='Save corpus as csv for opening as a spreadsheet',
                                    triggered=self.exportCorpus)

        self.setRestrictionsAct = QAction('Allow &unrestricted transcriptions',
                                    self,
                                    statusTip = 'If on, anything can be entered into transcriptions',
                                    triggered = self.setTranscriptionRestrictions,
                                    checkable = True)
        self.setConstraintsAct = QAction('Select anatomical/phonological constraints',
                                    self,
                                    statusTip = 'Select constraints on transcriptions',
                                    triggered = self.setConstraints)
        self.defineFeaturesAct = QAction('View/edit major feature values...',
                                        self,
                                        statusTip = 'View/edit major feature values',
                                        triggered = self.defineFeatures)

    def defineFeatures(self):
        currentMajor = self.featuresLayout.major.currentText()
        currentMinor = self.featuresLayout.minor.currentText()
        currentOneHandMovement = self.featuresLayout.oneHandMovement.currentText()
        currentTwoHandMovement = self.featuresLayout.twoHandMovement.currentText()
        currentOrientation = self.featuresLayout.orientation.currentText()
        currentDislocation = self.featuresLayout.dislocation.currentText()

        dialog = FeaturesDialog([self.majorLocations, self.minorLocations,
                                 self.oneHandMovements, self.twoHandMovements,
                                 self.orientations, self.dislocations])
        results = dialog.exec_()
        if results:

            self.featuresLayout.minor.clear()
            self.minorLocations = dialog.minorLocations

            #Empty strings are added here to allow the user to have no feature selected (as opposed to, say, no movement
            #which is different). These empty strings are used in the "define features" dialog.
            self.featuresLayout.major.clear()
            self.majorLocations = list()
            self.majorLocations.append('')
            self.featuresLayout.major.addItem('')
            for index in range(dialog.majorLocationList.count()):
                item = dialog.majorLocationList.item(index)
                self.majorLocations.append(item.text())
                self.featuresLayout.major.addItem(item.text())

            if currentMajor in self.majorLocations:
                self.featuresLayout.major.setCurrentText(currentMajor)
                self.featuresLayout.minor.setCurrentText(currentMinor)
            else:
                self.featuresLayout.major.setCurrentIndex(0)
                self.featuresLayout.minor.setCurrentIndex(0)

            self.featuresLayout.oneHandMovement.clear()
            self.oneHandMovements = list()
            self.oneHandMovements.append('')
            self.featuresLayout.oneHandMovement.addItem('')
            for index in range(dialog.oneHandMovementList.count()):
                item = dialog.oneHandMovementList.item(index)
                self.oneHandMovements.append(item.text())
                self.featuresLayout.oneHandMovement.addItem(item.text())
            if currentOneHandMovement in self.oneHandMovements:
                self.featuresLayout.oneHandMovement.setCurrentText(currentOneHandMovement)
            else:
                self.featuresLayout.oneHandMovement.setCurrentIndex(0)

            self.featuresLayout.twoHandMovement.clear()
            self.twoHandMovements = list()
            self.twoHandMovements.append('')
            self.featuresLayout.twoHandMovement.addItem('')
            for index in range(dialog.twoHandMovementList.count()):
                item = dialog.twoHandMovementList.item(index)
                self.twoHandMovements.append(item.text())
                self.featuresLayout.twoHandMovement.addItem(item.text())
            if currentTwoHandMovement in self.twoHandMovements:
                self.featuresLayout.twoHandMovement.setCurrentText(currentTwoHandMovement)
            else:
                self.featuresLayout.twoHandMovement.setCurrentIndex(0)

            self.featuresLayout.orientation.clear()
            self.orientations = list()
            self.orientations.append('')
            self.featuresLayout.orientation.addItem('')
            for index in range(dialog.orientationList.count()):
                item = dialog.orientationList.item(index)
                self.orientations.append(item.text())
                self.featuresLayout.orientation.addItem(item.text())
            if currentOrientation in self.orientations:
                self.featuresLayout.orientation.setCurrentText(currentOrientation)
            else:
                self.featuresLayout.orientation.setCurrentIndex(0)

            self.featuresLayout.dislocation.clear()
            self.dislocations = list()
            self.dislocations.append('')
            self.featuresLayout.dislocation.addItem('')
            for index in range(dialog.dislocationList.count()):
                item = dialog.dislocationList.item(index)
                self.dislocations.append(item.text())
                self.featuresLayout.dislocation.addItem(item.text())
            if currentDislocation in self.dislocations:
                self.featuresLayout.dislocation.setCurrentText(currentDislocation)
            else:
                self.featuresLayout.dislocation.setCurrentIndex(0)

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
                    print(Sign.headers, file=f)
                    for word in output:
                        print(word, file=f)
                QMessageBox.information(self, 'Success', 'Corpus successfully exported!')
            except PermissionError:
                filename = os.path.split(path)[-1]
                alert = QMessageBox()
                alert.setWindowTitle('Error encountered')
                alert.setText('The file {} is already open in a program on your computer. Please close the file before '
                              'saving, or choose a different file name.'.format(filename))
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

    def newGloss(self, clearFlags=False):
        if self.askSaveChanges:
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
        self.configTabs.widget(0).clearAll(clearFlags=clearFlags)
        self.configTabs.widget(1).clearAll(clearFlags=clearFlags)

        self.featuresLayout.reset()
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
    # if hasattr(sys, 'frozen'):
    #     dir = os.path.dirname(sys.executable)
    #     # dir = os.path.dirname(sys.argv[0])
    #     path = os.path.join(dir, 'media', filename)
    # else:
    #     path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', filename)
    path = os.path.join(os.getcwd(), 'media', filename)
    return path