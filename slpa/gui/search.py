from imports import (Qt, QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, QFont, QListWidget,
                     QComboBox, QCheckBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QFrame, QButtonGroup,
                     QRadioButton, QLineEdit, QMenu, QAction, QCompleter, QStringListModel)
from gui.transcriptions import TranscriptionConfigTab, TranscriptionInfo
from image import *
from constants import GLOBAL_OPTIONS, FINGER_SYMBOLS, SYMBOL_DESCRIPTIONS

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

    def __init__(self, allowAnyFinger=False):
        super().__init__()
        self.addItem('Thumb')
        self.addItem('Index')
        self.addItem('Middle')
        self.addItem('Ring')
        self.addItem('Pinky')
        if allowAnyFinger:
            self.addItem('Any')

class FlexionComboBox(QComboBox):

    def __init__(self):
        super().__init__()
        for symbol in FINGER_SYMBOLS[:-1]:
            #the final description is ignored on this loop and then added afterwards
            #because for the search function it's better if we re-order the options
            self.addItem(SYMBOL_DESCRIPTIONS[symbol].title())
        self.addItem('Extended (any)')
        self.addItem('Flexed (any)')
        self.addItem('Intermediate (any)')
        self.addItem('Unestimatable')#this was the description ignored earlier
        self.addItem('Blank')
        self.setMaxVisibleItems(len(FINGER_SYMBOLS)+4)

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

    def __init__(self, allowAnyFinger=False):
        super().__init__()
        self.deleteMe = QCheckBox()
        self.quantifiers = QuantifierComboBox()
        self.fingers = FingerComboBox(allowAnyFinger)
        self.flexions = FlexionComboBox()
        self.configs = ConfigComboBox()
        self.hands = HandComboBox()
        self.addWidget(self.deleteMe)
        self.addWidget(QLabel('In '))
        self.addWidget(self.configs)
        self.addWidget(self.hands)
        self.addWidget(self.quantifiers)
        self.addWidget(QLabel(' of the joints on the '))
        self.addWidget(self.fingers)
        self.addWidget(QLabel(' are '))
        self.addWidget(self.flexions)

    def generatePhrase(self):
        phrase = list()
        for n in range(self.count()):
            widget = self.itemAt(n).widget()
            if isinstance(widget, QLabel):
                phrase.append(widget.text().strip())
            elif isinstance(widget, QComboBox):
                phrase.append(widget.currentText())
        return ' '.join(phrase)


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.transcriptions = None
        self.regularExpressions = None

    def showRecentSearches(self):
        dialog = RecentSearchDialog(self.recents)
        dialog.exec_()
        return dialog.result

    def accept(self):
        self.accepted = True
        #the generate*() functions are implemented by TranscriptionSearchDialog and PhraseSearchDialog
        self.generateTranscriptions()
        self.generateRegEx()
        self.generateGlobalOptions()
        super().accept()

    def reject(self):
        self.accepted = False
        super().reject()


class PhraseDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.descriptionLayouts = list()
        self.introduction = QLabel()
        self.introduction.setFont(QFont('Arial', 15))
        #the introduction label is used by subclasses to present different information to the user

        self.transcriptions = list()
        self.regularExpressions = None

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.introduction)

        self.metaLayout = QVBoxLayout()
        self.layout.addLayout(self.metaLayout)

        sepFrame = QFrame()
        sepFrame.setFrameShape(QFrame.HLine)
        sepFrame.setLineWidth(2)
        self.layout.addWidget(sepFrame)

        self.buttonLayout = QVBoxLayout()
        self.topButtonLayout = QHBoxLayout()
        self.addDescription = QPushButton('')
        self.addDescription.clicked.connect(self.addFingerLayout)
        self.topButtonLayout.addWidget(self.addDescription)
        remove = QPushButton('Remove all selected phrases')
        self.topButtonLayout.addWidget(remove)
        remove.clicked.connect(self.removeFingerLayouts)
        self.buttonLayout.addLayout(self.topButtonLayout)

        bottomButtonLayout = QHBoxLayout()
        ok = QPushButton('OK')
        bottomButtonLayout.addWidget(ok)
        ok.clicked.connect(self.accept)
        cancel = QPushButton('Cancel')
        bottomButtonLayout.addWidget(cancel)
        cancel.clicked.connect(self.reject)
        self.buttonLayout.addLayout(bottomButtonLayout)

        self.layout.addLayout(self.buttonLayout)

        self.setLayout(self.layout)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def removeFingerLayouts(self):
        for n in reversed(range(len(self.descriptionLayouts))):
            layout = self.metaLayout.itemAt(n)
            if layout.deleteMe.isChecked():
                layout = self.metaLayout.takeAt(n)
                self.descriptionLayouts.pop(n)
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()

    def addFingerLayout(self, disable_quantifiers=False, allowAnyFinger=False):
        newLayout = FingerSearchLayout(allowAnyFinger)
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
            slots = [4, 5]
        elif finger == 'index':
            slots = [17,18,19]
        elif finger == 'middle':
            slots = [22, 23, 24]
        elif finger == 'ring':
            slots = [27, 28, 29]
        elif finger == 'pinky':
            slots = [32, 33, 34]
        elif finger == 'any':
            slots = [4, 5, 17, 18, 19, 22, 23, 24, 32, 33, 34]
        return slots

    def findTranscriptionSymbol(self, description):
        description = description.lower()
        if description == 'unestimatable':
            symbol = '?'

        elif description == 'blank':
            symbol = ''

        elif 'extended' in description:
            if 'hyper' in description:
                symbol = 'H'
            elif 'fully' in description:
                symbol = 'E'
            elif 'somewhat' in description:
                symbol = 'e'
            else:
                symbol = 'HEe'

        elif 'flexed' in description:
            if 'fully' in description:
                symbol = 'F'
            elif 'somewhat' in description:
                symbol = 'f'
            else:
                symbol = 'Ff'

        elif 'intermediate' in description:
            if 'clearly' in description:
                symbol = 'i'
            else:
                symbol = 'efi'

        return symbol

    def generateTranscriptions(self):
        transcriptions = list()
        for regex in self.regularExpressions:
            t = list()
            for symbol in regex:
                if symbol == '.':
                    t.append('_')
                else:
                    t.append(symbol)
            transcriptions.append(t)
        self.transcriptions = transcriptions

    def generateGlobalOptions(self):
        self.forearm = False
        self.estimated = False
        self.uncertain = False
        self.incomplete = False
        self.reduplicated = False

    def generatePhrases(self):
        self.phrases = [layout.generatePhrase() for layout in self.descriptionLayouts]

    def generateRegEx(self):
        mapping = {'config1hand1': (0, 'hand1Transcription'),
                   'config1hand2': (0, 'hand2Transcription'),
                   'config2hand1': (1, 'hand1Transcription'),
                   'config2hand2': (1, 'hand2Transcription')}

        for layout in self.descriptionLayouts:
            transcriptions = {'config1hand1': [None for n in range(34)],
                              'config1hand2': [None for n in range(34)],
                              'config2hand1': [None for n in range(34)],
                              'config2hand2': [None for n in range(34)]}

            finger = layout.fingers.currentText().lower()
            quantifier = layout.quantifiers.currentText().lower()
            config = layout.configs.currentText().lower().replace(' ', '')
            hand = layout.hands.currentText().lower().replace(' ', '')
            slots = self.findSlotNumbers(layout.fingers.currentText().lower())
            symbol = self.findTranscriptionSymbol(layout.flexions.currentText())

            configs = ['config1', 'config2'] if config == 'bothconfigs' else [config]
            hands = ['hand1', 'hand2'] if hand == 'bothhands' else [hand]

            if quantifier == 'all':
                pass #symbol is normal
            elif quantifier == 'any':
                if finger == 'thumb':
                    symbol = '{}|.(?={})'.format(symbol, symbol)
                    slots = [slots[0], -1*slots[1]]
                elif finger == 'any':
                    pass
                else:
                    symbol = '{}|.(?={})|.(?=.{})'.format(symbol, symbol, symbol)
                    slots = [slots[0], -1*slots[1], -1*slots[2]]
                #this new "symbol" acts as a regex that looks ahead 2 or 3 slots, depending on the selected finger
                #we don't want to put this regex in each of those slots, but rather only in the first one
            elif quantifier == 'none':
                symbol = '[^{}]'.format(symbol)

            for c in configs:
                for h in hands:
                    for slot in slots:
                        if slot < 0:
                            transcriptions[c+h].pop(slot-1*-1)
                        else:
                            transcriptions[c+h][slot-1] = symbol

            for key, value in transcriptions.items():
                regex = ['.' if v is None else v for v in value]
                transcriptions[key] = regex

            self.regularExpressions = [''.join(transcriptions[key]) for key in sorted(list(transcriptions.keys()))]

    def accept(self):
        self.accepted = True
        super().accept()

    def reject(self):
        self.accepted = False
        super().reject()

class PhraseSearchDialog(PhraseDialog, SearchDialog):

    def __init__(self, corpus, recents):
        PhraseDialog.__init__(self)
        self.corpus = corpus
        self.recents = recents
        self.regularExpressions = None
        self.transcriptions = list()
        self.setWindowTitle('Seach by descriptive phrase')
        self.addDescription.setText('Add search description')
        self.introduction.setText('Find a handshape with the following properties...')
        self.addFingerLayout()
        self.regularExpressions = list()
        showRecents = QPushButton('Show recent searches...')
        showRecents.clicked.connect(self.recentSearches)
        self.topButtonLayout.addWidget(showRecents)

    def recentSearches(self):
        result = self.showRecentSearches()
        if result is not None:
            results = result.recentData.segmentedTranscription

            #iterate through the results and get the relevant parts of each phrase
            #each result is a list of strings that, e.g.:
            #['in','config','1','hand','2','all','of','the','joints','on','the','index','finger','are','flexed']
            for i, result in enumerate(results):
                config = ' '.join([result[1], result[2]])
                hand = ' '.join([result[3], result[4]])
                quantifier = result[5]
                finger = result[11]
                flexion = result[13]
                #this try/except is to check for cases where there are more phrases in the result than there are
                #currently displayed on screen. in such a case we need to add a new layout.
                try:
                    layout = self.descriptionLayouts[i]
                except IndexError:
                    layout = FingerSearchLayout()
                    self.descriptionLayouts.append(layout)
                    self.metaLayout.addLayout(layout)


                index = layout.configs.findText(config)
                layout.configs.setCurrentIndex(index)

                index = layout.hands.findText(hand)
                layout.hands.setCurrentIndex(index)

                index = layout.quantifiers.findText(quantifier)
                layout.quantifiers.setCurrentIndex(index)

                index = layout.fingers.findText(finger)
                layout.fingers.setCurrentIndex(index)

                index = layout.flexions.findText(flexion)
                layout.flexions.setCurrentIndex(index)

                # if the recent search had fewer results than the current display, we need to delete any extra layouts
            if len(results) < len(self.descriptionLayouts):
                self.descriptionLayouts = self.descriptionLayouts[:len(results)]
                for n in range(self.metaLayout.count()):
                    layout = self.metaLayout.itemAt(n)
                    if n + 1 <= len(results):
                        layout.deleteMe.setChecked(False)
                    else:
                        layout.deleteMe.setChecked(True)
                self.removeFingerLayouts()

    def accept(self):
        self.generateRegEx()
        self.generatePhrases()
        super().accept()

class AutoFillDialog(PhraseDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Autofill')
        self.addDescription.setText('Add autofill operation')
        self.introduction.setText('Fill in the current transcription so that...')
        self.addFingerLayout()

    def accept(self):
        self.generateTranscriptions()
        super().accept()

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
        self.transcriptions = transcriptions

class TranscriptionsSearchOptionsDialog(QDialog):

    def __init__(self, blankOptionSelection = None, wildcard = None):
        super().__init__()

        self.blankOptionSelection = blankOptionSelection
        self.wildcard = wildcard

        self.setWindowTitle('Search Options')
        layout = QVBoxLayout()

        blankOptionsLabel = QLabel('How should blank spaces be interpreted in your search?')
        layout.addWidget(blankOptionsLabel)

        blankOptionsLayout = QVBoxLayout()
        self.blankOptionsGroup = QButtonGroup()

        asBlankOption = QRadioButton('Interpret as literal blanks, and only match blank slots')
        blankOptionsLayout.addWidget(asBlankOption)
        self.blankOptionsGroup.addButton(asBlankOption)
        self.blankOptionsGroup.setId(asBlankOption, 0)
        if self.blankOptionSelection == 'literal':
            asBlankOption.setChecked(True)

        asWildcardOption = QRadioButton('Interpret as wildcards, and match anything')
        blankOptionsLayout.addWidget(asWildcardOption)
        self.blankOptionsGroup.addButton(asWildcardOption)
        self.blankOptionsGroup.setId(asWildcardOption, 1)
        if self.blankOptionSelection == 'wildcard' or self.blankOptionSelection is None:
            asWildcardOption.setChecked(True)

        miniLayout = QHBoxLayout()
        asBlankWithWildcard = QRadioButton('Interpret as literal blanks, and use this character for wildcards: ')
        self.wildcardLineEdit = QLineEdit()
        self.wildcardLineEdit.setMaxLength(1)
        self.wildcardLineEdit.setMaximumWidth(30)
        self.blankOptionsGroup.addButton(asBlankWithWildcard)
        self.blankOptionsGroup.setId(asBlankWithWildcard, 2)
        if self.blankOptionSelection == 'both':
            asBlankWithWildcard.setChecked(True)
            self.wildcardLineEdit.setText(self.wildcard)
        miniLayout.addWidget(asBlankWithWildcard)
        miniLayout.addWidget(self.wildcardLineEdit)
        blankOptionsLayout.addLayout(miniLayout)

        layout.addLayout(blankOptionsLayout)

        buttonLayout = QHBoxLayout()
        ok = QPushButton('OK')
        ok.clicked.connect(self.accept)
        buttonLayout.addWidget(ok)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def accept(self):
        selectedButton = self.blankOptionsGroup.checkedButton()
        id_ = self.blankOptionsGroup.id(selectedButton)
        if id_ == 0:
            self.blankOptionSelection = 'literal'
            self.wildcard = None
        elif id_ == 1:
            self.blankOptionSelection = 'wildcard'
            self.wildcard = '_'
        elif id_ == 2:
            self.blankOptionSelection = 'both'
            self.wildcard = self.wildcardLineEdit.text()
        super().accept()

class GlossSearchDialog(QDialog):

    def __init__(self, corpus):
        super().__init__()
        self.setWindowTitle('Search by gloss')

        layout = QVBoxLayout()

        searchLayout = QHBoxLayout()

        searchLabel = QLabel('Enter gloss to search for: ')
        searchLayout.addWidget(searchLabel)

        self.searchEdit = QLineEdit()
        completer = QCompleter()
        model = QStringListModel()
        model.setStringList([word.gloss for word in corpus])
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchEdit.setCompleter(completer)
        searchLayout.addWidget(self.searchEdit)

        buttonLayout = QHBoxLayout()
        ok = QPushButton('OK')
        ok.clicked.connect(self.accept)
        buttonLayout.addWidget(ok)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(cancel)

        layout.addLayout(searchLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def reject(self):
        self.accepted = False
        super().reject()

    def accept(self):
        self.accepted = True
        self.searchWord = self.searchEdit.text()
        super().accept()


class TranscriptionSearchDialog(SearchDialog):

    def __init__(self, corpus, recents, blankValue, wildcard):
        super().__init__()

        print('recents', recents)
        print('blankValue', blankValue)
        print('wildcard', wildcard)

        self.corpus = corpus
        self.recents = recents
        self.blankValue = blankValue
        self.wildcard = wildcard
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
        self.handImage = HandShapeImage(getMediaFilePath('hand.JPG'))
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
                slot.changeValidatorState(True)

            for slot in self.configTabs.widget(k).hand2Transcription.slots[1:]:
                slot.slotSelectionChanged.connect(self.handImage.useReverseImage)
                slot.slotSelectionChanged.connect(self.handImage.transcriptionSlotChanged)
                slot.slotSelectionChanged.connect(self.transcriptionInfo.transcriptionSlotChanged)
                slot.changeValidatorState(True)

        buttonLayout = QHBoxLayout()
        blankOptionsButton = QPushButton('Search options...')
        blankOptionsButton.clicked.connect(self.showSearchOptions)
        buttonLayout.addWidget(blankOptionsButton)
        showRecents = QPushButton('Show recent searches...')
        showRecents.clicked.connect(self.recentSearches)
        ok = QPushButton('Search')
        ok.clicked.connect(self.accept)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(showRecents)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        self.showMaximized()

    def showSearchOptions(self):
        dialog = TranscriptionsSearchOptionsDialog(self.blankValue, self.wildcard)
        if dialog.exec_():
            self.blankValue = dialog.blankOptionSelection
            self.wildcard = dialog.wildcard

    def recentSearches(self):
        result = self.showRecentSearches()
        if result is not None:
            results = result.recentData.segmentedTranscription
            results = [[results[0], results[1]], [results[2], results[3]]]
            for config in [0,1]:
                for hand in [0,1]:
                    widget = getattr(self.configTabs.widget(config), 'hand{}Transcription'.format(hand+1))
                    for n,symbol in enumerate(results[config][hand]):
                        slot = getattr(widget, 'slot{}'.format(n+1))
                        slot.setText(symbol)

    def setupGlobalOptions(self):
        self.globalOptionsWidgets = list()
        globalOptionsLabel = QLabel('Global handshape options:')
        globalOptionsLabel.setFont(QFont(FONT_NAME, FONT_SIZE))
        self.globalOptionsLayout.addWidget(globalOptionsLabel)
        for option in GLOBAL_OPTIONS:
            widget = QCheckBox(option.title())
            option += 'CheckBox'
            setattr(self, option, widget)
            widget = getattr(self, option)
            self.globalOptionsLayout.addWidget(widget)
            self.globalOptionsWidgets.append(widget)

    def generateRegEx(self):
        expressions = list()

        for transcription in self.transcriptions:
            regex = list()
            for slot in transcription.slots:
                symbol = slot.text()
                if not symbol or symbol == ' ':
                    if self.blankValue == 'literal' or self.blankValue == 'both':
                        symbol = '_'
                    elif self.blankValue == 'wildcard':
                        symbol = '.'
                if symbol == self.wildcard:
                    symbol = '.'
                if symbol in ['?', '*', '$', '^', '+']:
                    symbol = '\\'+symbol

                regex.append(symbol)
            regex = ''.join(regex)
            expressions.append(regex)
        self.regularExpressions = expressions


    def generateTranscriptions(self):
        self.transcriptions = list()
        self.transcriptions.append(self.configTabs.widget(0).hand1Transcription)
        self.transcriptions.append(self.configTabs.widget(0).hand2Transcription)
        self.transcriptions.append(self.configTabs.widget(1).hand1Transcription)
        self.transcriptions.append(self.configTabs.widget(1).hand2Transcription)

    def generateGlobalOptions(self):
        for option in GLOBAL_OPTIONS:
            setattr(self, option, getattr(self, option+'CheckBox').isChecked())
        # self.forearm = self.forearmCheckBox.isChecked()
        # self.estimated = self.estimatedCheckBox.isChecked()
        # self.uncertain = self.uncertainCheckBox.isChecked()
        # self.incomplete = self.incompleteCheckBox.isChecked()
        # self.reduplicated = self.reduplicatedCheckBox.isChecked()

class RecentSearch:

    def __init__(self, transcriptions, regex, results):
        try:
            #assume that this is a list of Transcription objects
            top = ','.join([t.str_with_underscores() for t in transcriptions[0:2]])
            bottom = ','.join([t.str_with_underscores() for t in transcriptions[2:-1]])
            self.segmentedTranscription = [[slot.getText(empty_text='') for slot in transcription] for transcription in
                                           transcriptions]
            self.transcriptions = '\n'.join([top, bottom])
        except AttributeError:
            #if that fails, then it might be a descriptive phrase
            if transcriptions[0].startswith('In Config'):
                self.segmentedTranscription = [transcription.split(' ') for transcription in transcriptions]
                self.transcriptions = '\n'.join(transcriptions)
            #and if that's not the case, then it must be a list of transcriptions as strings
            else:
                top = ','.join([''.join(t) for t in transcriptions[0:2]])
                bottom = ','.join([''.join(t) for t in transcriptions[2:-1]])
                self.segmentedTranscription = [[slot for slot in transcription] for transcription in transcriptions]
                self.transcriptions = '\n'.join([top, bottom])

        self.regularExpression = regex
        self.results = ', '.join([r.gloss for r in results])

    def __str__(self):
        return self.transcriptions

class RecentSearchItem(QTableWidgetItem):

    def __init__(self, recentData, textType, menuText):
        super().__init__()
        self.recentData = recentData
        self.setText(getattr(self.recentData, textType))
        #self.makeMenu(menuText)

    def makeMenu(self, text):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.popMenu = QMenu(self)
        if 'Add' in text:
            function = self.addToFavourites
        elif 'Remove' in text:
            function = self.removeFromFavourites
        action = QAction(text, self, triggered = function)
        self.popMenu.addAction(action)

    def showContextMenu(self, point):
        self.popMenu.exec_(self.mapToGlobal(point))

    def addToFavourites(self):
        pass

    def removeFromFavourites(self):
        pass

class RecentSearchTable(QTableWidget):

    def __init__(self, searches, menuText):
        super().__init__()
        self.menuText = menuText
        self.setupTable(searches)

    def setupTable(self, searches):
        self.setColumnCount(2)
        self.setRowCount(len(searches))
        self.setHorizontalHeaderLabels(['Search', 'Results'])
        for row, recent in enumerate(searches):
            self.setItem(row, 0, RecentSearchItem(recent, 'transcriptions', self.menuText))
            self.setItem(row, 1, RecentSearchItem(recent, 'results', self.menuText))

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.resizeColumnToContents(0)

class RecentSearchDialog(QDialog):

    def __init__(self, recents, favourites = None):
        if favourites is None:
            favourites = list()
        super().__init__()
        self.setWindowTitle('Recent Searches')
        self.result = None
        layout = QVBoxLayout()

        tableLayout = QHBoxLayout()

        self.recentTable = RecentSearchTable(recents, 'Add to favourites')
        tableLayout.addWidget(self.recentTable)

        self.favouriteTable = RecentSearchTable(favourites, 'Remove from favourites')
        tableLayout.addWidget(self.favouriteTable)

        buttonLayout = QHBoxLayout()
        ok = QPushButton('Use selected search')
        ok.clicked.connect(self.accept)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)

        layout.addLayout(tableLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        self.resize(self.recentTable.width()*1.5, self.height())

    def addToFavourites(self):
        pass

    def removeFromFavourites(self):
        pass

    def setupTable(self, table, searches):
        table.setColumnCount(2)
        table.setRowCount(len(searches))
        table.setHorizontalHeaderLabels(['Search', 'Results'])
        for row, recent in enumerate(searches):
            table.setItem(row, 0, RecentSearchItem(recent, 'transcriptions'))
            table.setItem(row, 1, RecentSearchItem(recent, 'results'))

        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.resizeColumnToContents(0)

    def makeMenu(self, table, text, function):
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(self.showContextMenu)
        table.popMenu = QMenu(self)
        action = QAction(text, self, triggered = function)
        table.popMenu.addAction(action)

    def showContextMenu(self, table, point):
        table.popMenu.exec_(self.mapToGlobal(point))

    def accept(self):
        row = self.recentTable.currentRow()
        self.result = self.recentTable.item(row, 0)
        super().accept()

    def reject(self):
        self.result = None
        super().reject()


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