from imports import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QButtonGroup,
                     QRadioButton, QApplication, QGridLayout, QTabWidget, QWidget,
                     QSizePolicy, Qt, Slot, QLineEdit)
from gui.transcriptions import TranscriptionConfigTab
from constants import GLOBAL_OPTIONS
import sys
from gui.function_windows import FunctionDialog, FunctionWorker
import regex as re
from itertools import combinations
from pprint import pprint
from analysis.phonological_search import extended_finger_search

class EFWorker(FunctionWorker):
    def run(self):
        corpus = self.kwargs.pop('corpus')
        c1h1 = self.kwargs.pop('c1h1')
        c1h2 = self.kwargs.pop('c1h2')
        c2h1 = self.kwargs.pop('c2h1')
        c2h2 = self.kwargs.pop('c2h2')
        logic = self.kwargs.pop('logic')
        sign_type = self.kwargs.pop('signType')

        results = extended_finger_search(corpus, c1h1, c1h2, c2h1, c2h2, logic, sign_type)
        #pprint(self.results)
        self.dataReady.emit(results)


class PhonologicalSearchDialog(QDialog):

    def __init__(self, parent, corpus):
        super().__init__()

        self.parent = parent
        self.corpus = corpus

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        handShapeLayout = QVBoxLayout()
        mainLayout.addLayout(handShapeLayout)

        globalFrame = QGroupBox('Global options')
        globalLayout = QHBoxLayout()
        globalFrame.setLayout(globalLayout)
        handShapeLayout.addWidget(globalFrame)

        forearmButton = QCheckBox('Forearm')
        globalLayout.addWidget(forearmButton)
        estimatedButton = QCheckBox('Estimated')
        globalLayout.addWidget(estimatedButton)
        uncertainButton = QCheckBox('Uncertain')
        globalLayout.addWidget(uncertainButton)
        incompleteButton = QCheckBox('Incomplete')
        globalLayout.addWidget(incompleteButton)

        config1Frame = QGroupBox('Config 1')
        config1Layout = QVBoxLayout()
        config1Frame.setLayout(config1Layout)
        handShapeLayout.addWidget(config1Frame)

        config1 = TranscriptionConfigTab(1)
        config1Layout.addWidget(config1)

        config2Frame = QGroupBox('Config 2')
        config2Layout = QVBoxLayout()
        config2Frame.setLayout(config2Layout)
        handShapeLayout.addWidget(config2Frame)

        config2 = TranscriptionConfigTab(2)
        config2Layout.addWidget(config2)

        searchOptionLayout= QHBoxLayout()

        extendedFingerSearch = ExtendedFingerPanel()
        searchOptionLayout.addWidget(extendedFingerSearch)


        mainLayout.addLayout(searchOptionLayout)

        buttonLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)
        okButton = QPushButton('Search')
        recentButton = QPushButton('Show recent searches...')
        cancelButton = QPushButton('Cancel')
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(recentButton)
        buttonLayout.addWidget(cancelButton)


class BasicSearchTab(QWidget):

    def __init__(self):
        super().__init__()

        self.handPanel = LogicRadioButtonGroup('horizontal',
                                               'c1h1',
                                               title='Configuration/Hand',
                                               c1h1='Config1Hand1',
                                               c1h2='Config1Hand2',
                                               c2h1='Config2Hand1',
                                               c2h2='Config2Hand2', )

        self.includeIbutton = QCheckBox('Treat "i" as extended')
        self.includeIbutton.setChecked(False)

        self.fingerConfigPanel = ExtendedFingerPanel()
        self.fingerNumberPanel = NumExtendedFingerPanel()

        self.relationlogicPanel = LogicRadioButtonGroup('vertical',
                                                        'a',
                                                        title='Relation between finger configuration and '
                                                              'number of extended fingers',
                                                        a='Apply both',
                                                        o='Apply either',
                                                        fg='Apply only the finger configuration',
                                                        nf='Apply only the number of extended fingers')

        self.signTypePanel = LogicRadioButtonGroup('vertical',
                                                   'e',
                                                   title='Sign type',
                                                   sg='Only one-hand signs',
                                                   db='Only two-hand signs',
                                                   e='Either')

        self.modePanel = LogicRadioButtonGroup('vertical',
                                               'p',
                                               title='Search mode',
                                               p='Positive',
                                               n='Negative')
        self.notePanel = QLineEdit()
        self.notePanel.setPlaceholderText('Enter notes here...')

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.handPanel, 0, 0, 1, 2)
        mainLayout.addWidget(self.includeIbutton, 0, 2, 1, 1)
        mainLayout.addWidget(self.fingerConfigPanel, 1, 0, 1, 3)
        mainLayout.addWidget(self.fingerNumberPanel, 2, 0, 1, 3)
        mainLayout.addWidget(self.relationlogicPanel, 3, 0, 1, 1)
        mainLayout.addWidget(self.signTypePanel, 3, 1, 1, 1)
        mainLayout.addWidget(self.modePanel, 3, 2, 1, 1)
        mainLayout.addWidget(self.notePanel, 4, 0, 1, 3)

    def value(self):
        handconfig = self.handPanel.value()
        fingerConfigRegExps = self.fingerConfigPanel.generateRegExp(self.includeIbutton.isChecked())
        fingerNumberRegExps = self.fingerNumberPanel.generateRegExp(self.includeIbutton.isChecked())
        reltionLogic = self.relationlogicPanel.value()
        searchMode = self.modePanel.value()

        handconfigvalue = {
            'fingerConfigRegExps': fingerConfigRegExps,
            'fingerNumberRegExps': fingerNumberRegExps,
            'relationLogic': reltionLogic,
            'searchMode': searchMode
        }

        neutralhandRegExp = re.compile('(?P<thumb>_....)..\u2205/......' \
                            '(?P<index>1...)' \
                            '(?P<middle>.2...)' \
                            '(?P<ring>.3...)' \
                            '(?P<pinky>.4...)')
        neutralhandRegExps = set()
        neutralhandRegExps.add(neutralhandRegExp)
        neutralvalue = {
            'fingerConfigRegExps': neutralhandRegExps,
            'fingerNumberRegExps': neutralhandRegExps,
            'relationLogic': 'Apply both',
            'searchMode': 'Positive'
        }

        if handconfig == 'Configuration 1 Hand 1':
            c1h1 = handconfigvalue
            c1h2 = neutralvalue
            c2h1 = neutralvalue
            c2h2 = neutralvalue
        elif handconfig == 'Configuration 1 Hand 2':
            c1h1 = neutralvalue
            c1h2 = handconfigvalue
            c2h1 = neutralvalue
            c2h2 = neutralvalue
        elif handconfig == 'Configuration 2 Hand 1':
            c1h1 = neutralvalue
            c1h2 = neutralvalue
            c2h1 = handconfigvalue
            c2h2 = neutralvalue
        else:
            c1h1 = neutralvalue
            c1h2 = neutralvalue
            c2h1 = neutralvalue
            c2h2 = handconfigvalue

        return {
            'c1h1': c1h1,
            'c1h2': c1h2,
            'c2h1': c2h1,
            'c2h2': c2h2,
            'logic': 'All four hand/configuration specifications',
            'signType': self.signTypePanel.value(),
            'note': self.notePanel.text()
        }


class AdvancedSearchTab(QWidget):
    def __init__(self):
        super().__init__()

        style = 'QTabWidget::pane { /* The tab widget frame */' \
                'border: 5px solid #9B9B9B;' \
                'top: -0.75em;}'

        self.c1h1Tab = AdvancedFingerTab()
        self.c1h2Tab = AdvancedFingerTab()
        self.c2h1Tab = AdvancedFingerTab()
        self.c2h2Tab = AdvancedFingerTab()

        handTab = QTabWidget()
        handTab.setStyleSheet(style)
        handTab.addTab(self.c1h1Tab, 'Config1Hand1')
        handTab.addTab(self.c1h2Tab, 'Config1Hand2')
        handTab.addTab(self.c2h1Tab, 'Config2Hand1')
        handTab.addTab(self.c2h2Tab, 'Config2Hand2')

        self.logicPanel = LogicRadioButtonGroup('horizontal', 'all', 'Signs should contain',
                                                all='All four hand/configuration specifications',
                                                any='Any of the four hand/configuration specifications')

        self.signTypePanel = LogicRadioButtonGroup('horizontal',
                                                   'e',
                                                   title='Sign type',
                                                   sg='Only one-hand signs',
                                                   db='Only two-hand signs',
                                                   e='Either')
        self.notePanel = QLineEdit()
        self.notePanel.setPlaceholderText('Enter notes here...')

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(handTab)
        mainLayout.addWidget(self.logicPanel)
        mainLayout.addWidget(self.signTypePanel)
        mainLayout.addWidget(self.notePanel)

    def value(self):
        return {
            'c1h1': self.c1h1Tab.value(),
            'c1h2': self.c1h2Tab.value(),
            'c2h1': self.c2h1Tab.value(),
            'c2h2': self.c2h2Tab.value(),
            'logic': self.logicPanel.value(),
            'signType': self.signTypePanel.value(),
            'note': self.notePanel.text()
        }


class AdvancedFingerTab(QWidget):
    def __init__(self):
        super().__init__()

        self.fingerConfigPanel = ExtendedFingerPanel()
        self.fingerNumberPanel = NumExtendedFingerPanel()
        self.relationlogicPanel = LogicRadioButtonGroup('vertical',
                                                        'a',
                                                        title='Relation between finger configuration and '
                                                              'number of extended fingers',
                                                        a='Apply both',
                                                        o='Apply either',
                                                        fg='Apply only the finger configuration',
                                                        nf='Apply only the number of extended fingers')
        self.modePanel = LogicRadioButtonGroup('vertical',
                                               'p',
                                               title='Search mode',
                                               p='Positive',
                                               n='Negative')

        self.includeIbutton = QCheckBox('Treat "i" as extended')
        self.includeIbutton.setChecked(False)

        self.default = QPushButton('Return to default')
        self.default.clicked.connect(self.setToDefault)

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.fingerConfigPanel, 0, 0, 1, 3)
        mainLayout.addWidget(self.fingerNumberPanel, 1, 0, 1, 3)
        mainLayout.addWidget(self.relationlogicPanel, 2, 0, 2, 1)
        mainLayout.addWidget(self.modePanel, 2, 1, 2, 1)
        mainLayout.addWidget(self.includeIbutton, 2, 2, 1, 1)
        mainLayout.addWidget(self.default, 3, 2, 1, 1)

    def setToDefault(self):
        self.fingerConfigPanel.setToDefault()
        self.fingerNumberPanel.setToDefault()
        self.relationlogicPanel.setToDefault('Apply both')
        self.modePanel.setToDefault('Positive')
        self.includeIbutton.setChecked(False)

    def value(self):
        return {
            'fingerConfigRegExps': self.fingerConfigPanel.generateRegExp(self.includeIbutton.isChecked()),
            'fingerNumberRegExps': self.fingerNumberPanel.generateRegExp(self.includeIbutton.isChecked()),
            'relationLogic': self.relationlogicPanel.value(),
            'searchMode': self.modePanel.value()
        }


class ExtendedFingerSearchDialog(FunctionDialog):
    header = ['Corpus', 'Sign', 'Token frequency', 'Note']
    about = 'Extended finger search'
    name = 'extended finger search'

    def __init__(self, corpus, parent, settings, recent):
        super().__init__(parent, settings, EFWorker())

        self.corpus = corpus
        self.recent = recent

        mainLayout = QGridLayout()

        self.basicTab = BasicSearchTab()
        self.advancedTab = AdvancedSearchTab()

        self.searchTab = QTabWidget()
        self.searchTab.addTab(self.basicTab, 'Basic search')
        self.searchTab.addTab(self.advancedTab, 'Advanced search')

        mainLayout.addWidget(self.searchTab, 0, 0)

        #####This part should be removed later#####
        #self.testButton = QPushButton('test')
        #mainLayout.addWidget(self.testButton, 1, 0)
        #self.testButton.clicked.connect(self.test)
        #####This part should be removed later#####

        self.layout().insertLayout(0, mainLayout)

    #def test(self):
    #    res = self.generateKwargs()
    #    ret = extended_finger_search(self.corpus, res['c1h1'], res['c1h2'], res['c2h1'], res['c2h2'], res['logic'])
    #    pprint(ret)

    def generateKwargs(self):
        kwargs = dict()

        tab = self.searchTab.currentIndex()  # 0 = basic and 1 = advanced
        if tab == 0:  # basic
            value = self.basicTab.value()
        else:
            value = self.advancedTab.value()

        kwargs['corpus'] = self.corpus
        kwargs['c1h1'] = value['c1h1']
        kwargs['c1h2'] = value['c1h2']
        kwargs['c2h1'] = value['c2h1']
        kwargs['c2h2'] = value['c2h2']
        kwargs['logic'] = value['logic']
        kwargs['signType'] = value['signType']
        self.note = value['note']
        return kwargs

    @Slot(object)
    def setResults(self, results):
        #TODO: need to modify token frequency when implemented (right not there is not frquency info)
        #TODO: double check thread method to properly place accept()
        self.results = list()
        for sign in results:
            self.results.append({'Corpus': self.corpus.name,
                                 'Sign': sign.gloss,
                                 'Token frequency': 1,
                                 'Note': self.note})
        self.accept()


class NumExtendedFingerPanel(QGroupBox):
    fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
    fingerConfigDict_with_i = {
        'thumb': {'Extended': r'(?P<thumb>.(?P<thumb_opposition>[LU]).(?<thumb_mcp>[HEei]).).+.\u2205/.+.....',
                  'Not extended': r'(?P<thumb>.(?P<thumb_opposition_1>[^LU]).(?<thumb_mcp_1>[HEei]).|_(?P<thumb_opposition_2>[LU]).(?<thumb_mcp_2>[^HEei]).|_(?P<thumb_opposition_3>[^LU]).(?<thumb_mcp_3>[^HEei]).).+.\u2205/.+.....',
                  'Either': r'(?P<thumb>.(?P<thumb_opposition>.).(?<thumb_mcp>.).).+.\u2205/.+.....'},
        'index': {'Extended': r'(?P<index>1(?P<index_mcp>[HEei])..)',
                  'Not extended': r'(?P<index>1(?P<index_mcp>[^HEei])..)',
                  'Either': r'(?P<index>1(?P<index_mcp>.)..)'},
        'middle': {'Extended': r'(?P<middle>.+2(?P<middle_mcp>[HEei])..)',
                   'Not extended': r'(?P<middle>.+2(?P<middle_mcp>[^HEei])..)',
                   'Either': r'(?P<middle>.+2(?P<middle_mcp>.)..)'},
        'ring': {'Extended': r'(?P<ring>.+3(?P<ring_mcp>[HEei])..)',
                 'Not extended': r'(?P<ring>.+3(?P<ring_mcp>[^HEei])..)',
                 'Either': r'(?P<ring>.+3(?P<ring_mcp>.)..)'},
        'pinky': {'Extended': r'(?P<pinky>.+4(?P<pinky_mcp>[HEei])..)',
                  'Not extended': r'(?P<pinky>.+4(?P<pinky_mcp>[^HEei])..)',
                  'Either': r'(?P<pinky>.+4(?P<pinky_mcp>.)..)'}
    }

    fingerConfigDict_without_i = {
        'thumb': {'Extended': r'(?P<thumb>.(?P<thumb_opposition>[LU]).(?<thumb_mcp>[HEe]).).+.\u2205/.+.....',
                  'Not extended': r'(?P<thumb>.(?P<thumb_opposition_1>[^LU]).(?<thumb_mcp_1>[HEe]).|_(?P<thumb_opposition_2>[LU]).(?<thumb_mcp_2>[^HEe]).|_(?P<thumb_opposition_3>[^LU]).(?<thumb_mcp_3>[^HEe]).).+.\u2205/.+.....',
                  'Either': r'(?P<thumb>.(?P<thumb_opposition>.).(?<thumb_mcp>.).).+.\u2205/.+.....'},
        'index': {'Extended': r'(?P<index>1(?P<index_mcp>[HEe])..)',
                  'Not extended': r'(?P<index>1(?P<index_mcp>[^HEe])..)',
                  'Either': r'(?P<index>1(?P<index_mcp>.)..)'},
        'middle': {'Extended': r'(?P<middle>.+2(?P<middle_mcp>[HEe])..)',
                   'Not extended': r'(?P<middle>.+2(?P<middle_mcp>[^HEe])..)',
                   'Either': r'(?P<middle>.+2(?P<middle_mcp>.)..)'},
        'ring': {'Extended': r'(?P<ring>.+3(?P<ring_mcp>[HEe])..)',
                 'Not extended': r'(?P<ring>.+3(?P<ring_mcp>[^HEe])..)',
                 'Either': r'(?P<ring>.+3(?P<ring_mcp>.)..)'},
        'pinky': {'Extended': r'(?P<pinky>.+4(?P<pinky_mcp>[HEe])..)',
                  'Not extended': r'(?P<pinky>.+4(?P<pinky_mcp>[^HEe])..)',
                  'Either': r'(?P<pinky>.+4(?P<pinky_mcp>.)..)'}
    }

    def __init__(self):
        super().__init__('Number of extended fingers')

        groupLayout = QVBoxLayout()
        self.setLayout(groupLayout)

        logicComment = QLabel('Returned signs will contain ANY of the specificed numbers:')
        groupLayout.addWidget(logicComment)

        buttonLayout = QHBoxLayout()
        groupLayout.addLayout(buttonLayout)

        self.zero = QCheckBox('0')
        self.one = QCheckBox('1')
        self.two = QCheckBox('2')
        self.three = QCheckBox('3')
        self.four = QCheckBox('4')
        self.five = QCheckBox('5')
        self.zero.setChecked(True)
        self.one.setChecked(True)
        self.two.setChecked(True)
        self.three.setChecked(True)
        self.four.setChecked(True)
        self.five.setChecked(True)

        buttonLayout.addWidget(self.zero)
        buttonLayout.addWidget(self.one)
        buttonLayout.addWidget(self.two)
        buttonLayout.addWidget(self.three)
        buttonLayout.addWidget(self.four)
        buttonLayout.addWidget(self.five)

    def setToDefault(self):
        self.zero.setChecked(True)
        self.one.setChecked(True)
        self.two.setChecked(True)
        self.three.setChecked(True)
        self.four.setChecked(True)
        self.five.setChecked(True)

    def generateRegExp(self, includeI):
        def generate_subset(s, n):
            """
            Helper function for calculating "from s take n"
            """
            return list(combinations(s, n))

        regExps = set()
        # First, find the numbers that are checked
        numFingers = self.value()

        for num in numFingers:
            # Second, find the fingers that corresponding to a num
            combs = generate_subset(self.fingers, num)
            for comb in combs:
                fingers_reg = r''
                for finger in self.fingers:
                    if includeI:
                        if finger in comb:
                            reg = self.fingerConfigDict_with_i[finger]['Extended']
                            fingers_reg += reg
                        else:
                            reg = self.fingerConfigDict_with_i[finger]['Not extended']
                            fingers_reg += reg
                    else:
                        if finger in comb:
                            reg = self.fingerConfigDict_without_i[finger]['Extended']
                            fingers_reg += reg
                        else:
                            reg = self.fingerConfigDict_without_i[finger]['Not extended']
                            fingers_reg += reg
                regExps.add(fingers_reg)

        return regExps

    def value(self):
        checkedNum = list()
        for button in [self.zero, self.one, self.two, self.three, self.four, self.five]:
            if button.isChecked():
                checkedNum.append(int(button.text()))
        return checkedNum


class ExtendedFingerPanel(QGroupBox):

    def __init__(self):
        super().__init__('Finger configuration')
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        fingerExtensionSpecificationLayout = QHBoxLayout()
        mainLayout.addLayout(fingerExtensionSpecificationLayout)

        self.optionsForT = FingerOptionGroup('Thumb')
        self.optionsForI = FingerOptionGroup('Index')
        self.optionsForM = FingerOptionGroup('Middle')
        self.optionsForR = FingerOptionGroup('Ring')
        self.optionsForP = FingerOptionGroup('Pinky')
        fingerExtensionSpecificationLayout.addWidget(self.optionsForT)
        fingerExtensionSpecificationLayout.addWidget(self.optionsForI)
        fingerExtensionSpecificationLayout.addWidget(self.optionsForM)
        fingerExtensionSpecificationLayout.addWidget(self.optionsForR)
        fingerExtensionSpecificationLayout.addWidget(self.optionsForP)

        self.logicGroup = LogicRadioButtonGroup('horizontal', 'a',
                                                title='Sign should contain:',
                                                a='All of the extensions',
                                                o='Any of the extensions')
        mainLayout.addWidget(self.logicGroup)

    def setToDefault(self):
        self.optionsForT.setToDefault()
        self.optionsForI.setToDefault()
        self.optionsForM.setToDefault()
        self.optionsForR.setToDefault()
        self.optionsForP.setToDefault()
        self.logicGroup.setToDefault('All of the extensions')

    def generateRegExp(self, includeI):
        """
        :return: A set of regular expressions that represent the finger configuration
        """
        def generate_subset(s, n):
            """
            Helper function for calculating "from s take n"
            """
            return list(combinations(s, n))

        fingerConfigLogic = self.logicGroup.value()
        regExps = set()

        if fingerConfigLogic == 'All of the extensions':
            # This is the easy case: just concatenate the regular expression for each finger
            regExp = re.compile(
                self.optionsForT.generateRegExp(includeI) +
                self.optionsForI.generateRegExp(includeI) +
                self.optionsForM.generateRegExp(includeI) +
                self.optionsForR.generateRegExp(includeI) +
                self.optionsForP.generateRegExp(includeI))
            regExps.add(regExp)

        else:  # 'Any of the extendions'
            # First, find the fingers that are chosen to be extended
            extendedFingers = list()
            for finger in [self.optionsForT, self.optionsForI, self.optionsForM, self.optionsForR, self.optionsForP]:
                chosen = finger.value()
                if chosen == 'Extended':
                    extendedFingers.append(finger.title().lower())

            # Second, find all the possible combinations of extended fingers

            for n in range(1, len(extendedFingers)+1):  # n = 1, 2, ... up to 5
                combs = generate_subset(extendedFingers, n)
                for comb in combs:  # comb is a list of extended fingers, e.g., ['thumb', 'ring']
                    # go through each finger to see if it's in comb
                    fingers_reg = r''
                    for option in [self.optionsForT, self.optionsForI, self.optionsForM, self.optionsForR, self.optionsForP]:
                        finger = option.title().lower()
                        # if so, we need to get the 'Extended' regular expression
                        if finger in comb:
                            reg = option.getExtendedRegExp(includeI)
                            fingers_reg += reg
                        elif finger in extendedFingers:  # the finger not in comb but still specified as extended
                            reg = option.getNotExtendedRegExp(includeI)
                            fingers_reg += reg
                        else:  # else just get its original specification
                            reg = option.generateRegExp(includeI)
                            fingers_reg += reg
                    regExps.add(fingers_reg)
        return regExps

    def value(self):
        valueDict = dict()
        valueDict['thumb'] = self.optionsForT.value()
        valueDict['index'] = self.optionsForI.value()
        valueDict['middle'] = self.optionsForM.value()
        valueDict['ring'] = self.optionsForR.value()
        valueDict['pinky'] = self.optionsForP.value()
        valueDict['logic'] = self.logicGroup.value()

        return valueDict


class LogicRadioButtonGroup(QGroupBox):
    def __init__(self, direction, default, title='', **kwarg):
        super().__init__(title)

        if direction == 'vertical':
            buttonLayout = QVBoxLayout()
        else:  # direction == 'horizontal'
            buttonLayout = QHBoxLayout()

        self.buttonGroup = QButtonGroup()
        self.setLayout(buttonLayout)

        for short_name, text in kwarg.items():
            button = QRadioButton(text)
            if short_name == default:
                button.setChecked(True)
            self.buttonGroup.addButton(button)
            buttonLayout.addWidget(button)

    def setToDefault(self, default_option):
        for option in self.buttonGroup.buttons():
            if option.text() == default_option:
                option.setChecked(True)
            else:
                option.setChecked(False)

    def value(self):
        checked = self.buttonGroup.checkedButton()
        return checked.text()


class FingerOptionGroup(QGroupBox):
    fingerOptionDict_with_i = {
        'thumb': {'Extended': r'(?P<thumb>.(?P<thumb_opposition>[LU]).(?<thumb_mcp>[HEei]).).+.\u2205/.+.....',
                  'Not extended': r'(?P<thumb>.(?P<thumb_opposition_1>[^LU]).(?<thumb_mcp_1>[HEei]).|_(?P<thumb_opposition_2>[LU]).(?<thumb_mcp_2>[^HEei]).|_(?P<thumb_opposition_3>[^LU]).(?<thumb_mcp_3>[^HEei]).).+.\u2205/.+.....',
                  'Either': r'(?P<thumb>.(?P<thumb_opposition>.).(?<thumb_mcp>.).).+.\u2205/.+.....'},
        'index': {'Extended': r'(?P<index>1(?P<index_mcp>[HEei])..)',
                  'Not extended': r'(?P<index>1(?P<index_mcp>[^HEei])..)',
                  'Either': r'(?P<index>1(?P<index_mcp>.)..)'},
        'middle': {'Extended': r'(?P<middle>.+2(?P<middle_mcp>[HEei])..)',
                   'Not extended': r'(?P<middle>.+2(?P<middle_mcp>[^HEei])..)',
                   'Either': r'(?P<middle>.+2(?P<middle_mcp>.)..)'},
        'ring': {'Extended': r'(?P<ring>.+3(?P<ring_mcp>[HEei])..)',
                 'Not extended': r'(?P<ring>.+3(?P<ring_mcp>[^HEei])..)',
                 'Either': r'(?P<ring>.+3(?P<ring_mcp>.)..)'},
        'pinky': {'Extended': r'(?P<pinky>.+4(?P<pinky_mcp>[HEei])..)',
                  'Not extended': r'(?P<pinky>.+4(?P<pinky_mcp>[^HEei])..)',
                  'Either': r'(?P<pinky>.+4(?P<pinky_mcp>.)..)'}
    }

    fingerOptionDict_without_i = {
        'thumb': {'Extended': r'(?P<thumb>.(?P<thumb_opposition>[LU]).(?<thumb_mcp>[HEe]).).+.\u2205/.+.....',
                  'Not extended': r'(?P<thumb>.(?P<thumb_opposition_1>[^LU]).(?<thumb_mcp_1>[HEe]).|_(?P<thumb_opposition_2>[LU]).(?<thumb_mcp_2>[^HEe]).|_(?P<thumb_opposition_3>[^LU]).(?<thumb_mcp_3>[^HEe]).).+.\u2205/.+.....',
                  'Either': r'(?P<thumb>.(?P<thumb_opposition>.).(?<thumb_mcp>.).).+.\u2205/.+.....'},
        'index': {'Extended': r'(?P<index>1(?P<index_mcp>[HEe])..)',
                  'Not extended': r'(?P<index>1(?P<index_mcp>[^HEe])..)',
                  'Either': r'(?P<index>1(?P<index_mcp>.)..)'},
        'middle': {'Extended': r'(?P<middle>.+2(?P<middle_mcp>[HEe])..)',
                   'Not extended': r'(?P<middle>.+2(?P<middle_mcp>[^HEe])..)',
                   'Either': r'(?P<middle>.+2(?P<middle_mcp>.)..)'},
        'ring': {'Extended': r'(?P<ring>.+3(?P<ring_mcp>[HEe])..)',
                 'Not extended': r'(?P<ring>.+3(?P<ring_mcp>[^HEe])..)',
                 'Either': r'(?P<ring>.+3(?P<ring_mcp>.)..)'},
        'pinky': {'Extended': r'(?P<pinky>.+4(?P<pinky_mcp>[HEe])..)',
                  'Not extended': r'(?P<pinky>.+4(?P<pinky_mcp>[^HEe])..)',
                  'Either': r'(?P<pinky>.+4(?P<pinky_mcp>.)..)'}
    }

    def __init__(self, groupName):
        super().__init__(groupName)

        self.buttonGroup = QButtonGroup()
        self.extended = QRadioButton('Extended')
        self.notExtended = QRadioButton('Not extended')
        self.either = QRadioButton('Either')
        self.either.setChecked(True)

        self.buttonGroup.addButton(self.extended)
        self.buttonGroup.addButton(self.notExtended)
        self.buttonGroup.addButton(self.either)

        buttonLayout = QVBoxLayout()
        self.setLayout(buttonLayout)
        buttonLayout.addWidget(self.extended)
        buttonLayout.addWidget(self.notExtended)
        buttonLayout.addWidget(self.either)

    def setToDefault(self):
        self.extended.setChecked(False)
        self.notExtended.setChecked(False)
        self.either.setChecked(True)

    def getExtendedRegExp(self, includeI):
        finger = self.title().lower()
        if includeI:
            regExp = self.fingerOptionDict_with_i[finger]['Extended']
        else:
            regExp = self.fingerOptionDict_without_i[finger]['Extended']
        return regExp

    def getEitherRegExp(self, includeI):
        finger = self.title().lower()
        if includeI:
            regExp = self.fingerOptionDict_with_i[finger]['Either']
        else:
            regExp = self.fingerOptionDict_without_i[finger]['Either']
        return regExp

    def getNotExtendedRegExp(self, includeI):
        finger = self.title().lower()
        if includeI:
            regExp = self.fingerOptionDict_with_i[finger]['Not extended']
        else:
            regExp = self.fingerOptionDict_without_i[finger]['Not extended']
        return regExp

    def generateRegExp(self, includeI):
        finger = self.title()
        chosen = self.buttonGroup.checkedButton().text()

        if includeI:
            if finger == 'Thumb':
                regExp = self.fingerOptionDict_with_i['thumb'][chosen]
            elif finger == 'Index':
                regExp = self.fingerOptionDict_with_i['index'][chosen]
            elif finger == 'Middle':
                regExp = self.fingerOptionDict_with_i['middle'][chosen]
            elif finger == 'Ring':
                regExp = self.fingerOptionDict_with_i['ring'][chosen]
            else:
                regExp = self.fingerOptionDict_with_i['pinky'][chosen]
        else:
            if finger == 'Thumb':
                regExp = self.fingerOptionDict_without_i['thumb'][chosen]
            elif finger == 'Index':
                regExp = self.fingerOptionDict_without_i['index'][chosen]
            elif finger == 'Middle':
                regExp = self.fingerOptionDict_without_i['middle'][chosen]
            elif finger == 'Ring':
                regExp = self.fingerOptionDict_without_i['ring'][chosen]
            else:
                regExp = self.fingerOptionDict_without_i['pinky'][chosen]

        return regExp

    def value(self):
        checked = self.buttonGroup.checkedButton()
        return checked.text()





#app = QApplication(sys.argv)
#main = ExtendedFingerSearchDialog(None, None, None, None)
#main.show()
#sys.exit(app.exec_())


