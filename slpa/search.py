from imports import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget, QPushButton, QFont, QListWidget, QComboBox
from transcriptions import TranscriptionConfigTab


class ConfigComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.addItem('Config 1')
        self.addItem('Config 2')
        self.addItem('Any config')

class HandComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        self.addItem('Hand 1')
        self.addItem('Hand 2')
        self.addItem('Any hand')

class FingerComboBox(QComboBox):

    def __init__(self):
        super().__init__()
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
        self.addWidget(QLabel('For '))
        self.addWidget(self.configs)
        self.addWidget(self.hands)
        self.addWidget(self.quantifiers)
        self.addWidget(QLabel(' of the joints on the '))
        self.addWidget(self.fingers)
        self.addWidget(QLabel(' finger are '))
        self.addWidget(self.flexions)


class NaturalLanguageSearchDialog(QDialog):

    def __init__(self, corpus):
        super().__init__()
        self.corpus = corpus
        self.setWindowTitle('Search')
        self.searchLayouts = list()

        self.layout = QVBoxLayout()

        buttonLayout = QHBoxLayout()
        addFingerDescription = QPushButton('Add search description')
        addFingerDescription.clicked.connect(self.addFingerLayout)
        buttonLayout.addWidget(addFingerDescription)
        # addJointDescription = QPushButton('Add search description (joint-based)')
        # addJointDescription.clicked.connect(self.addJointLayout)
        # buttonLayout.addWidget(addJointDescription)
        ok = QPushButton('OK')
        buttonLayout.addWidget(ok)
        ok.clicked.connect(self.accept)
        cancel = QPushButton('Cancel')
        buttonLayout.addWidget(cancel)
        cancel.clicked.connect(self.reject)
        self.layout.addLayout(buttonLayout)

        self.setLayout(self.layout)

    def addFingerLayout(self):
        newLayout = FingerSearchLayout()
        self.searchLayouts.append(newLayout)
        self.layout.addLayout(newLayout)

    def addJointLayout(self):
        newLayout = JointSearchLayout()
        self.searchLayouts.append(newLayout)
        self.layout.addLayout(newLayout)

    def accept(self):
        self.transcriptions = None
        super().accept()

    def reject(self):
        self.transcriptions = None
        super().reject()


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