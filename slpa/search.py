from imports import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QPushButton, QFont, QListWidget, QComboBox, Qt,
                     QCheckBox)
from transcriptions import TranscriptionConfigTab, TranscriptionInfo
from image import *

FONT_NAME = 'Arial'
FONT_SIZE = 12

class ConfigComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.addItem('Config 1')
        self.addItem('Config 2')
        self.addItem('Either config')
        self.addItem('Both configs')

class HandComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.addItem('Hand 1')
        self.addItem('Hand 2')
        self.addItem('Either hand')
        self.addItem('Both hands')

class FingerComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.addItem('Thumb')
        self.addItem('Index')
        self.addItem('Middle')
        self.addItem('Ring')
        self.addItem('Pinky')

class FlexionComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.addItem('Hyperextended')
        self.addItem('Extended')
        self.addItem('Intermediate')
        self.addItem('Flexed')
        self.addItem('Obscured')
        self.addItem('Blank')

class QuantifierComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.addItem('All')
        self.addItem('Any')
        self.addItem('None')

class JointComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.addItem('Proximal')
        self.addItem('Medial')
        self.addItem('Distal')

class JointSearchLayout(QHBoxLayout):

    def __init__(self):
        super().__init__()
        self.quantifiers = QuantifierComboBox()
        self.joints = JointComboBox()
        self.flexions = FlexionComboBox()
        self.fingers = FingerComboBox()
        self.configs = ConfigComboBox()
        self.hands = HandComboBox()
        self.addWidget(QLabel('For '))
        self.addWidget(self.configs)
        self.addWidget(self.hands)
        self.addWidget(self.quantifiers)
        self.addWidget(QLabel(' of the '))
        self.addWidget(self.joints)
        self.addWidget(QLabel(' on the '))
        self.addWidget(self.fingers)
        self.addWidget(QLabel(' are '))
        self.addWidget(self.flexions)

class FingerSearchLayout(QHBoxLayout):

    def __init__(self):
        super().__init__()
        self.quantifiers = QuantifierComboBox()
        self.fingers = FingerComboBox()
        self.flexions = FlexionComboBox()
        self.configs = ConfigComboBox()
        self.hands = HandComboBox()
        self.addWidget(QLabel('In '))
        self.addWidget(self.configs)
        self.addWidget(self.hands)
        self.addWidget(self.quantifiers)
        self.addWidget(QLabel(' of the joints on the '))
        self.addWidget(self.fingers)
        self.addWidget(QLabel(' are '))
        self.addWidget(self.flexions)

class PhraseDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.descriptionLayouts = list()
        self.introduction = QLabel()
        self.introduction.setFont(QFont('Arial', 15))
        #this label is used by subclasses to present different information to the user

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.introduction)

        self.metaLayout = QVBoxLayout()
        self.layout.addLayout(self.metaLayout)

        buttonLayout = QHBoxLayout()
        self.addDescription = QPushButton('')
        self.addDescription.clicked.connect(self.addFingerLayout)
        buttonLayout.addWidget(self.addDescription)
        ok = QPushButton('OK')
        buttonLayout.addWidget(ok)
        ok.clicked.connect(self.accept)
        cancel = QPushButton('Cancel')
        buttonLayout.addWidget(cancel)
        cancel.clicked.connect(self.reject)
        self.layout.addLayout(buttonLayout)

        self.setLayout(self.layout)

    def addFingerLayout(self, disable_quantifiers=False):
        newLayout = FingerSearchLayout()
        if disable_quantifiers:
            newLayout.quantifiers.removeItem(2)
            newLayout.quantifiers.removeItem(1)
            newLayout.configs.removeItem(2)
            newLayout.hands.removeItem(2)
        self.descriptionLayouts.append(newLayout)
        self.metaLayout.addLayout(newLayout)

    def addJointLayout(self):
        newLayout = JointSearchLayout()
        self.descriptionLayouts.append(newLayout)
        self.metaLayout.addLayout(newLayout)

    def findSlotNumbers(self, finger):
        if finger == 'thumb':
            slots = (4, 5)
        elif finger == 'index':
            slots = (17,18,19)
        elif finger == 'middle':
            slots = (22, 23, 24)
        elif finger == 'ring':
            slots = (27, 28, 29)
        elif finger == 'pinky':
            slots = (32, 33, 34)
        return slots

    def findTranscriptionSymbol(self, description):
        if description == 'Obscured':
            symbol = '?'
        elif description == 'Blank':
            symbol = ''
        else:
            symbol = description[0]
            if symbol == 'I': #intermediate has to be lowercase, but the other flexion values do not
                symbol = 'i'

        return symbol

    def generateTranscriptions(self):
        pass #overloaded function, see subclasses

    def accept(self):
        self.transcriptions = self.generateTranscriptions()
        super().accept()

    def reject(self):
        self.transcriptions = None
        super().reject()

class PhraseSearchDialog(PhraseDialog):

    def __init__(self, corpus):
        super().__init__()
        self.corpus = corpus
        self.setWindowTitle('Seach by descriptive phrase')
        self.addDescription.setText('Add search description')
        self.introduction.setText('Find a handshape with the following properties...')
        self.addFingerLayout()

    def generateTranscription(self):
        pass

class AutoFillDialog(PhraseDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Autofill')
        self.addDescription.setText('Add autofill operation')
        self.introduction.setText('Fill in the current transcription so that...')
        self.addFingerLayout()

    def addFingerLayout(self):
        super().addFingerLayout(disable_quantifiers=True)

    def generateTranscriptions(self):

        transcriptions = {'config1hand1': [None for n in range(34)],
                          'config1hand2': [None for n in range(34)],
                          'config2hand1': [None for n in range(34)],
                          'config2hand2': [None for n in range(34)]}

        for layout in self.descriptionLayouts:
            quantifier = layout.quantifiers.currentText().lower()
            config = layout.configs.currentText().lower().replace(' ', '')
            hand = layout.hands.currentText().lower().replace(' ', '')
            slots = self.findSlotNumbers(layout.fingers.currentText().lower())
            symbol = self.findTranscriptionSymbol(layout.flexions.currentText())

            configs = ['config1', 'config2'] if config == 'bothconfigs' else [config]
            hands = ['hand1', 'hand2'] if hand == 'bothhands' else [hand]

            for c in configs:
                for h in hands:
                    for slot in slots:
                        transcriptions[c+h][slot-1] = symbol

        return transcriptions


class TranscriptionSearchDialog(QDialog):

    def __init__(self, corpus):
        super().__init__()

        self.corpus = corpus
        self.transcriptions = None
        self.setWindowTitle('Search')
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        layout = QVBoxLayout()

        #Set up up top layout
        self.topLayout = QHBoxLayout()
        explanation = QLabel()
        text = ('Enter the transcription you want to match in your corpus.')
        explanation.setText(text)
        explanation.setFont(QFont('Arial', 16))
        self.topLayout.addWidget(explanation)
        layout.addLayout(self.topLayout)

        #Set up config tabs
        self.configTabs = QTabWidget()
        self.configTabs.addTab(TranscriptionConfigTab(1), 'Config 1')
        self.configTabs.addTab(TranscriptionConfigTab(2), 'Config 2')
        layout.addWidget(self.configTabs)

        # Add "global" handshape options (as checkboxes)
        self.globalOptionsLayout = QHBoxLayout()
        self.setupGlobalOptions()
        layout.addLayout(self.globalOptionsLayout)

        #Add hand image
        self.infoPanel = QHBoxLayout()
        self.handImage = HandShapeImage(getMediaFilePath('hand.png'))
        self.infoPanel.addWidget(self.handImage)
        self.transcriptionInfo = TranscriptionInfo()
        self.infoPanel.addLayout(self.transcriptionInfo)
        layout.addLayout(self.infoPanel)

        #Connects some slots and signals
        for k in [0,1]:
            for slot in self.configTabs.widget(k).hand1Transcription.slots[1:]:
                slot.slotSelectionChanged.connect(self.handImage.useNormalImage)
                slot.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)
                slot.slotSelectionChanged.connect(self.transcriptionInfo.transcriptionSlotChanged)

            for slot in self.configTabs.widget(k).hand2Transcription.slots[1:]:
                slot.slotSelectionChanged.connect(self.handImage.useReverseImage)
                slot.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)
                slot.slotSelectionChanged.connect(self.transcriptionInfo.transcriptionSlotChanged)

        buttonLayout = QVBoxLayout()
        ok = QPushButton('Search')
        ok.clicked.connect(self.search)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.showMaximized()

    def setupGlobalOptions(self):
        globalOptionsLabel = QLabel('Global handshape options:')
        globalOptionsLabel.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(globalOptionsLabel)
        self.forearmCheckBox = QCheckBox('Forearm is involved (slot 1/field 1)')
        self.forearmCheckBox.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(self.forearmCheckBox)
        self.partialObscurityCheckBox = QCheckBox('This sign is partially obscured')
        self.partialObscurityCheckBox.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(self.partialObscurityCheckBox)
        self.uncertainCodingCheckBox = QCheckBox('The coding for this sign is uncertain')
        self.uncertainCodingCheckBox.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(self.uncertainCodingCheckBox)
        self.incompleteCodingCheckBox = QCheckBox('The coding for this sign is incomplete')
        self.incompleteCodingCheckBox.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(self.incompleteCodingCheckBox)
        self.globalOptionsWidgets = [self.forearmCheckBox,
                                     self.partialObscurityCheckBox,
                                     self.uncertainCodingCheckBox,
                                     self.incompleteCodingCheckBox]

    def generateRegEx(self):
        expressions = list()

        for transcription in self.transcriptions:
            regex = list()
            for slot in transcription.slots:
                symbol = slot.text()
                if not symbol or symbol == ' ':
                    symbol = '.'
                regex.append(symbol)
            regex = ''.join(regex)
            expressions.append(regex)
        self.regularExpressions = expressions


    def search(self):
        self.getTranscriptions()
        self.generateRegEx()
        super().accept()

    def getTranscriptions(self):
        self.transcriptions = list()
        self.transcriptions.append(self.configTabs.widget(0).hand1Transcription)
        self.transcriptions.append(self.configTabs.widget(0).hand2Transcription)
        self.transcriptions.append(self.configTabs.widget(1).hand1Transcription)
        self.transcriptions.append(self.configTabs.widget(1).hand2Transcription)
        self.forearmInvolved = self.forearmCheckBox.isChecked()
        self.partialObscurity = self.partialObscurityCheckBox.isChecked()
        self.uncertainCoding = self.uncertainCodingCheckBox.isChecked()
        self.incompleteCoding = self.incompleteCodingCheckBox.isChecked()

class SearchResultsDialog(QDialog):

    def __init__(self, results):
        super().__init__()
        self.setWindowTitle('Search Results')
        layout = QVBoxLayout()
        self.result = None

        resultsLayout = QHBoxLayout()

        self.resultsList = QListWidget()
        for r in results:
            self.resultsList.addItem(r.gloss)

        resultsLayout.addWidget(self.resultsList)
        layout.addLayout(resultsLayout)

        buttonLayout = QHBoxLayout()
        okButton = QPushButton('Go to this entry')
        cancelButton = QPushButton('Cancel')
        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def accept(self):
        item = self.resultsList.currentItem()
        self.result = item
        super().accept()

    def reject(self):
        self.result = None
        super().reject()