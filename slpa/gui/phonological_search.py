from imports import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QButtonGroup,
                     QRadioButton, QApplication, QGridLayout, QTabWidget, QWidget,
                     QSizePolicy, Qt)
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
        pass


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
        self.handPanel = LogicRadioButtonGroup('vertical',
                                               'h1c1',
                                               title='Hand/Configuration',
                                               h1c1='Hand 1 Configuration 1',
                                               h1c2='Hand 1 Configuration 2',
                                               h2c1='Hand 2 Configuration 1',
                                               h2c2='Hand 2 Configuration 2',)
        self.modePanel = LogicRadioButtonGroup('vertical',
                                               'p',
                                               title='Search mode',
                                               p='Positive',
                                               n='Negative')

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.fingerConfigPanel, 0, 0, 1, 3)
        mainLayout.addWidget(self.fingerNumberPanel, 1, 0, 1, 3)
        mainLayout.addWidget(self.relationlogicPanel, 2, 0, 1, 1)
        mainLayout.addWidget(self.handPanel, 2, 1, 1, 1)
        mainLayout.addWidget(self.modePanel, 2, 2, 1, 1)

    def value(self):
        handconfig = self.handPanel.value()
        fingerConfigRegExps = self.fingerConfigPanel.generateRegExp()
        fingerNumberRegExps = self.fingerNumberPanel.generateRegExp()
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

        if handconfig == 'Hand 1 Configuration 1':
            h1c1 = handconfigvalue
            h1c2 = neutralvalue
            h2c1 = neutralvalue
            h2c2 = neutralvalue
        elif handconfig == 'Hand 1 Configuration 2':
            h1c1 = neutralvalue
            h1c2 = handconfigvalue
            h2c1 = neutralvalue
            h2c2 = neutralvalue
        elif handconfig == 'Hand 2 Configuration 1':
            h1c1 = neutralvalue
            h1c2 = neutralvalue
            h2c1 = handconfigvalue
            h2c2 = neutralvalue
        else:
            h1c1 = neutralvalue
            h1c2 = neutralvalue
            h2c1 = neutralvalue
            h2c2 = handconfigvalue

        return {
            'h1c1': h1c1,
            'h1c2': h1c2,
            'h2c1': h2c1,
            'h2c2': h2c2,
            'logic': 'All four hand/configuration specifications'
        }


class AdvancedSearchTab(QWidget):
    def __init__(self):
        super().__init__()

        style = 'QTabWidget::pane { /* The tab widget frame */' \
                'border: 5px solid #9B9B9B;' \
                'top: -0.75em;}'

        self.h1c1Tab = AdvancedFingerTab()
        self.h1c2Tab = AdvancedFingerTab()
        self.h2c1Tab = AdvancedFingerTab()
        self.h2c2Tab = AdvancedFingerTab()

        handTab = QTabWidget()
        handTab.setStyleSheet(style)
        handTab.addTab(self.h1c1Tab, 'Hand1Config1')
        handTab.addTab(self.h1c2Tab, 'Hand1Config2')
        handTab.addTab(self.h2c1Tab, 'Hand2Config1')
        handTab.addTab(self.h2c2Tab, 'Hand2Config2')

        self.logicPanel = LogicRadioButtonGroup('horizontal', 'all', 'Signs should contain',
                                                all='All four hand/configuration specifications',
                                                any='Any of the four hand/configuration specifications')

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(handTab)
        mainLayout.addWidget(self.logicPanel)

    def value(self):
        return {
            'h1c1': self.h1c1Tab.value(),
            'h1c2': self.h1c2Tab.value(),
            'h2c1': self.h2c1Tab.value(),
            'h2c2': self.h2c2Tab.value(),
            'logic': self.logicPanel.value()
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
        self.default = QPushButton('Return to default')
        self.default.clicked.connect(self.setToDefault)

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(self.fingerConfigPanel, 0, 0, 1, 2)
        mainLayout.addWidget(self.fingerNumberPanel, 1, 0, 1, 2)
        mainLayout.addWidget(self.relationlogicPanel, 2, 0, 2, 1)
        mainLayout.addWidget(self.modePanel, 2, 1, 1, 1)
        mainLayout.addWidget(self.default, 3, 1, 1, 1)

    def setToDefault(self):
        self.fingerConfigPanel.setToDefault()
        self.fingerNumberPanel.setToDefault()
        self.relationlogicPanel.setToDefault('Apply both')
        self.modePanel.setToDefault('Positive')

    def value(self):
        return {
            'fingerConfigRegExps': self.fingerConfigPanel.generateRegExp(),
            'fingerNumberRegExps': self.fingerNumberPanel.generateRegExp(),
            'relationLogic': self.relationlogicPanel.value(),
            'searchMode': self.modePanel.value()
        }


class ExtendedFingerSearchDialog(FunctionDialog):
    header = ['Sign', 'Match', 'Token frequency']
    about = 'Extended finger search'
    name = 'extended finger search'

    fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
    fingerConfigDict = {'thumb': {'Extended': r'(?P<thumb>_(?P<thumb_opposition>[LU]).(?<thumb_mcp>[HEe]).)..\u2205/......',
                                  'Not extended': r'(?P<thumb>_(?P<thumb_opposition_1>[^LU]).(?<thumb_mcp_1>[HEe]).|_(?P<thumb_opposition_2>[LU]).(?<thumb_mcp_2>[^HEe]).|_(?P<thumb_opposition_3>[^LU]).(?<thumb_mcp_3>[^HEe]).)..\u2205/......',
                                  'Either': r'(?P<thumb>_(?P<thumb_opposition>.).(?<thumb_mcp>.).)..\u2205/......'},
                        'index': {'Extended': r'(?P<index>1(?P<index_mcp>[HEe])..)',
                                  'Not extended': r'(?P<index>1(?P<index_mcp>[^HEe])..)',
                                  'Either': r'(?P<index>1(?P<index_mcp>.)..)'},
                        'middle': {'Extended': r'(?P<middle>.2(?P<middle_mcp>[HEe])..)',
                                   'Not extended': r'(?P<middle>.2(?P<middle_mcp>[^HEe])..)',
                                   'Either': r'(?P<middle>.2(?P<middle_mcp>.)..)'},
                        'ring': {'Extended': r'(?P<ring>.3(?P<ring_mcp>[HEe])..)',
                                 'Not extended': r'(?P<ring>.3(?P<ring_mcp>[^HEe])..)',
                                 'Either': r'(?P<ring>.3(?P<ring_mcp>.)..)'},
                        'pinky': {'Extended': r'(?P<pinky>.4(?P<pinky_mcp>[HEe])..)',
                                  'Not extended': r'(?P<pinky>.4(?P<pinky_mcp>[^HEe])..)',
                                  'Either': r'(?P<pinky>.4(?P<pinky_mcp>.)..)'}}

    def __init__(self, corpus, parent, settings, recent):
        super().__init__(parent, settings, EFWorker())

        self.corpus = corpus
        self.recent = recent

        mainLayout = QGridLayout()

        self.basicTab = BasicSearchTab()
        self.advancedTab = AdvancedSearchTab()

        self.searchTab = QTabWidget()
        #self.searchTab.currentChanged.connect(self.curTabChange)
        self.searchTab.addTab(self.basicTab, 'Basic search')
        self.searchTab.addTab(self.advancedTab, 'Advanced search')

        mainLayout.addWidget(self.searchTab, 0, 0)
        #self.testWidget = ExtendedFingerPanel()

        #configTab = QTabWidget()
        #configTab.addTab(self.testWidget, 'Test')
        #mainLayout.addWidget(configTab)

        #self.fingerConfigGroup = ExtendedFingerPanel()
        #mainLayout.addWidget(self.fingerConfigGroup, 0, 0, 1, 2)

        #self.fingerNumberGroup = NumExtendedFingerPanel()
        #mainLayout.addWidget(self.fingerNumberGroup, 1, 0, 1, 2)

        #self.relationlogicGroup = LogicRadioButtonGroup('vertical', 'a', title='Relation between finger configuration and '
        #                                                                  'number of extended fingers',
        #                                           a='Apply both',
        #                                           o='Apply either',
        #                                           fg='Apply only the finger configuration',
        #                                           nf='Apply only the number of extended fingers')
        #mainLayout.addWidget(self.relationlogicGroup, 2, 0, 1, 1)

        #self.modeGroup = LogicRadioButtonGroup('vertical', 'p', title='Search mode', p='Positive', n='Negative')
        #mainLayout.addWidget(self.modeGroup, 2, 1, 1, 1)

        self.testButton = QPushButton('test')
        mainLayout.addWidget(self.testButton, 1, 0)
        self.testButton.clicked.connect(self.test)

        self.layout().insertLayout(0, mainLayout)
        #self.curTabChange(0)

    #def curTabChange(self, index):
    #    for i in range(self.searchTab.count()):
    #        if i == index:
    #            self.searchTab.widget(i).setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    #        else:
    #            self.searchTab.widget(i).setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def test(self):
        res = self.generateKwargs()
        #pprint(res)
        ret = extended_finger_search(self.corpus, res['h1c1'], res['h2c1'], res['h1c2'], res['h2c2'], res['logic'])
        pprint(ret)


    def generateRegExp(self):
        def generate_subset(s, n):
            return list(combinations(s, n))

        fingerConfig = self.fingerConfigGroup.value()

        extendedFingers = list()
        for finger in self.fingers:
            if fingerConfig[finger] == 'Extended':
                extendedFingers.append(finger)

        fingerConfigLogic = fingerConfig['logic']

        fingerConfigRegExps = list()
        if fingerConfigLogic == 'All of the extensions':
            fingerConfigRegExp = r''
            for finger in self.fingers:
                reg = self.fingerConfigDict[finger][fingerConfig[finger]]
                fingerConfigRegExp += reg
            fingerConfigRegExps.append(fingerConfigRegExp)
        else:  ## 'Any of the extendions'
            for n in range(len(extendedFingers) + 1):
                combs = generate_subset(extendedFingers, n)
                for comb in combs:
                    fingers_reg = r''
                    for finger in self.fingers:
                        if finger in comb:
                            reg = self.fingerConfigDict[finger]['Extended']
                            fingers_reg += reg
                        elif finger in extendedFingers:
                            reg = self.fingerConfigDict[finger]['Either']
                            fingers_reg += reg
                        else:
                            reg = self.fingerConfigDict[finger][fingerConfig[finger]]
                            fingers_reg += reg
                    fingerConfigRegExps.append(fingers_reg)

        fingerNumRegExps = list()

        numFingers = self.fingerNumberGroup.value()
        for num in numFingers:
            combs = generate_subset(self.fingers, num)
            for comb in combs:
                fingers_reg = r''
                for finger in self.fingers:
                    if finger in comb:
                        reg = self.fingerConfigDict[finger]['Extended']
                        fingers_reg += reg
                    else:
                        reg = self.fingerConfigDict[finger]['Not extended']
                        fingers_reg += reg
                fingerNumRegExps.append(fingers_reg)

        #relationLogic = self.relationlogicGroup.value()

        #if relationLogic == 'Apply both':
        #    regExps = set(fingerConfigRegExps) & set(fingerNumRegExps)
        #elif relationLogic == 'Apply either':
        #    regExps = set(fingerConfigRegExps) | set(fingerNumRegExps)
        #elif relationLogic == 'Apply only the finger configuration':
        #    regExps = set(fingerConfigRegExps)
        #else:
        #    regExps = set(fingerNumRegExps)

        return set(fingerConfigRegExps), set(fingerNumRegExps)

    def generateKwargs(self):
        kwargs = dict()

        tab = self.searchTab.currentIndex()  # 0 = basic and 1 = advanced
        if tab == 0:  # basic
            value = self.basicTab.value()
        else:
            value = self.advancedTab.value()

        kwargs['h1c1'] = value['h1c1']
        kwargs['h1c2'] = value['h1c2']
        kwargs['h2c1'] = value['h2c1']
        kwargs['h2c2'] = value['h2c2']
        kwargs['logic'] = value['logic']
        return kwargs


class NumExtendedFingerPanel(QGroupBox):
    fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']
    fingerConfigDict = {
        'thumb': {'Extended': r'(?P<thumb>_(?P<thumb_opposition>[LU]).(?<thumb_mcp>[HEe]).)..\u2205/......',
                  'Not extended': r'(?P<thumb>_(?P<thumb_opposition_1>[^LU]).(?<thumb_mcp_1>[HEe]).|_(?P<thumb_opposition_2>[LU]).(?<thumb_mcp_2>[^HEe]).|_(?P<thumb_opposition_3>[^LU]).(?<thumb_mcp_3>[^HEe]).)..\u2205/......',
                  'Either': r'(?P<thumb>_(?P<thumb_opposition>.).(?<thumb_mcp>.).)..\u2205/......'},
        'index': {'Extended': r'(?P<index>1(?P<index_mcp>[HEe])..)',
                  'Not extended': r'(?P<index>1(?P<index_mcp>[^HEe])..)',
                  'Either': r'(?P<index>1(?P<index_mcp>.)..)'},
        'middle': {'Extended': r'(?P<middle>.2(?P<middle_mcp>[HEe])..)',
                   'Not extended': r'(?P<middle>.2(?P<middle_mcp>[^HEe])..)',
                   'Either': r'(?P<middle>.2(?P<middle_mcp>.)..)'},
        'ring': {'Extended': r'(?P<ring>.3(?P<ring_mcp>[HEe])..)',
                 'Not extended': r'(?P<ring>.3(?P<ring_mcp>[^HEe])..)',
                 'Either': r'(?P<ring>.3(?P<ring_mcp>.)..)'},
        'pinky': {'Extended': r'(?P<pinky>.4(?P<pinky_mcp>[HEe])..)',
                  'Not extended': r'(?P<pinky>.4(?P<pinky_mcp>[^HEe])..)',
                  'Either': r'(?P<pinky>.4(?P<pinky_mcp>.)..)'}
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

    def generateRegExp(self):
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
                    if finger in comb:
                        reg = self.fingerConfigDict[finger]['Extended']
                        fingers_reg += reg
                    else:
                        reg = self.fingerConfigDict[finger]['Not extended']
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
    #fingers = ['thumb', 'index', 'middle', 'ring', 'pinky']

    def __init__(self):
        super().__init__('Finger configuration')
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        fingerExtensionSpecificationLayout = QHBoxLayout()
        mainLayout.addLayout(fingerExtensionSpecificationLayout)

        # TODO: might want to reimplement this by loop through the list
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

    def generateRegExp(self):
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
                self.optionsForT.generateRegExp() +
                self.optionsForI.generateRegExp() +
                self.optionsForM.generateRegExp() +
                self.optionsForR.generateRegExp() +
                self.optionsForP.generateRegExp())
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
                            reg = option.getExtendedRegExp()
                            fingers_reg += reg
                        elif finger in extendedFingers:  # the finger not in comb but still specified as extended
                            reg = option.getNotExtendedRegExp()
                            fingers_reg += reg
                        else:  # else just get its original specification
                            reg = option.generateRegExp()
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




class AdvancedOptionDialog(QDialog):
    def __init__(self):
        super().__init__()
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        numberOfExtendedFingerGroup = QGroupBox('Number of extended fingers')
        mainLayout.addWidget(numberOfExtendedFingerGroup)

        groupLayout = QVBoxLayout()
        numberOfExtendedFingerGroup.setLayout(groupLayout)

        buttonLayout = QHBoxLayout()
        groupLayout.addLayout(buttonLayout)

        zero = QCheckBox('0')
        one = QCheckBox('1')
        two = QCheckBox('2')
        three = QCheckBox('3')
        four = QCheckBox('4')
        five = QCheckBox('5')
        zero.setChecked(True)
        one.setChecked(True)
        two.setChecked(True)
        three.setChecked(True)
        four.setChecked(True)
        five.setChecked(True)

        buttonLayout.addWidget(zero)
        buttonLayout.addWidget(one)
        buttonLayout.addWidget(two)
        buttonLayout.addWidget(three)
        buttonLayout.addWidget(four)
        buttonLayout.addWidget(five)

        logicLayoyt = QHBoxLayout()
        logicHeading = QLabel('Signs should contain:')
        logicGroup = LogicRadioButtonGroup('horizontal', 'a', a='All of the above', o='Any of the above')
        logicLayoyt.addWidget(logicHeading, alignment=Qt.AlignLeft)
        logicLayoyt.addWidget(logicGroup, alignment=Qt.AlignLeft)
        groupLayout.addLayout(logicLayoyt)

        # bolded the relevant part / from the main window
        relationGroup = QGroupBox('Relation between the specifications for extended fingers and the number of fingers')
        mainLayout.addWidget(relationGroup)

        relationGroupLayout = QHBoxLayout()
        relationGroup.setLayout(relationGroupLayout)

        relationlogicGroup = LogicRadioButtonGroup('vertical', 'a', a='Both apply', o='Either applies')
        relationGroupLayout.addWidget(relationlogicGroup)


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
    fingerOptionDict = {
        'thumb': {'Extended': r'(?P<thumb>_(?P<thumb_opposition>[LU]).(?<thumb_mcp>[HEe]).)..\u2205/......',
                  'Not extended': r'(?P<thumb>_(?P<thumb_opposition_1>[^LU]).(?<thumb_mcp_1>[HEe]).|_(?P<thumb_opposition_2>[LU]).(?<thumb_mcp_2>[^HEe]).|_(?P<thumb_opposition_3>[^LU]).(?<thumb_mcp_3>[^HEe]).)..\u2205/......',
                  'Either': r'(?P<thumb>_(?P<thumb_opposition>.).(?<thumb_mcp>.).)..\u2205/......'},
        'index': {'Extended': r'(?P<index>1(?P<index_mcp>[HEe])..)',
                  'Not extended': r'(?P<index>1(?P<index_mcp>[^HEe])..)',
                  'Either': r'(?P<index>1(?P<index_mcp>.)..)'},
        'middle': {'Extended': r'(?P<middle>.2(?P<middle_mcp>[HEe])..)',
                   'Not extended': r'(?P<middle>.2(?P<middle_mcp>[^HEe])..)',
                   'Either': r'(?P<middle>.2(?P<middle_mcp>.)..)'},
        'ring': {'Extended': r'(?P<ring>.3(?P<ring_mcp>[HEe])..)',
                 'Not extended': r'(?P<ring>.3(?P<ring_mcp>[^HEe])..)',
                 'Either': r'(?P<ring>.3(?P<ring_mcp>.)..)'},
        'pinky': {'Extended': r'(?P<pinky>.4(?P<pinky_mcp>[HEe])..)',
                  'Not extended': r'(?P<pinky>.4(?P<pinky_mcp>[^HEe])..)',
                  'Either': r'(?P<pinky>.4(?P<pinky_mcp>.)..)'}
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

    def getExtendedRegExp(self):
        finger = self.title().lower()
        return self.fingerOptionDict[finger]['Extended']

    def getEitherRegExp(self):
        finger = self.title().lower()
        return self.fingerOptionDict[finger]['Either']

    def getNotExtendedRegExp(self):
        finger = self.title().lower()
        return self.fingerOptionDict[finger]['Not extended']

    def generateRegExp(self):
        finger = self.title()
        chosen = self.buttonGroup.checkedButton().text()

        if finger == 'Thumb':
            regExp = self.fingerOptionDict['thumb'][chosen]
        elif finger == 'Index':
            regExp = self.fingerOptionDict['index'][chosen]
        elif finger == 'Middle':
            regExp = self.fingerOptionDict['middle'][chosen]
        elif finger == 'Ring':
            regExp = self.fingerOptionDict['ring'][chosen]
        else:
            regExp = self.fingerOptionDict['pinky'][chosen]

        return regExp


    def value(self):
        checked = self.buttonGroup.checkedButton()
        return checked.text()





#app = QApplication(sys.argv)
#main = ExtendedFingerSearchDialog(None, None, None, None)
#main.show()
#sys.exit(app.exec_())


