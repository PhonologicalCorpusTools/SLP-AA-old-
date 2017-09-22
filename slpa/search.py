from imports import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QPushButton, QFont, QListWidget, QComboBox
from transcriptions import TranscriptionConfigTab


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


        layout = QVBoxLayout()

        self.topLayout = QHBoxLayout()
        explanation = QLabel()
        text = ('Enter the transcription you want to match in your corpus.')
        explanation.setText(text)
        explanation.setFont(QFont('Arial', 16))
        self.topLayout.addWidget(explanation)
        layout.addLayout(self.topLayout)

        self.configTabs = QTabWidget()
        self.configTabs.addTab(TranscriptionConfigTab(1), 'Config 1')
        self.configTabs.addTab(TranscriptionConfigTab(2), 'Config 2')
        layout.addWidget(self.configTabs)

        buttonLayout = QVBoxLayout()
        ok = QPushButton('Search')
        ok.clicked.connect(self.search)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def search(self):
        self.transcriptions = self.getTranscriptions()
        super().accept()

    def getTranscriptions(self):
        transcriptions = list()
        transcriptions.append(self.configTabs.widget(0).hand1Transcription)
        transcriptions.append(self.configTabs.widget(0).hand2Transcription)
        transcriptions.append(self.configTabs.widget(1).hand1Transcription)
        transcriptions.append(self.configTabs.widget(1).hand2Transcription)
        return transcriptions

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