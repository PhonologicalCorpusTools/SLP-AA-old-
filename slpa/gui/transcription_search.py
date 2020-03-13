from datetime import date
from imports import (QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QLabel, QCheckBox,
                     QGridLayout, QWidget, Qt, Slot, QLineEdit, QMenu, QAction)
from gui.function_windows import FunctionDialog, FunctionWorker
from pprint import pprint
from gui.helperwidgets import LogicRadioButtonGroup
from analysis.transcription_search import transcription_search


NULL = '\u2205'
X_IN_BOX = '\u2327'


class TransField(QHBoxLayout):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self.left_bracket = QLabel('[')
        self.addWidget(self.left_bracket)

        self.right_bracket = QLabel(']<font size="5"><b><sub>{}</sub></b></font>'.format(self.number))
        self.addWidget(self.right_bracket)

    def addSlot(self, slot):
        position = self.count() - 1
        self.insertWidget(position, slot)

    def value(self):
        results = list()
        for i in range(1, self.count()-1):
            slot = self.itemAt(i).widget()
            results.append(slot.value())
        return tuple(results)


class TransSlot(QPushButton):

    def __init__(self, number, field, options):
        super().__init__()

        self.number = number
        self.field = field

        self.setContentsMargins(0, 0, 0, 0)

        self.initialSymbol = '*'
        self.setText(self.initialSymbol)
        self.setFixedWidth(35)

        # 1: True, 0: Either, -1:False
        self.isUncertain = 0
        self.isEstimate = 0

        self.positive = True

        self.menu = QMenu()

        self.options = options

        for option in self.options:
            symbol = QAction(option, self, checkable=True, triggered=self.updateSymbol)
            self.menu.addAction(symbol)

        self.menu.addSeparator()
        selectAllAction = QAction('Select all', self, checkable=False, triggered=self.selectAll)
        self.menu.addAction(selectAllAction)
        resetToStarAction = QAction('Reset to *', self, checkable=False, triggered=self.resetToStar)
        self.menu.addAction(resetToStarAction)

        self.menu.addSeparator()
        self.negAction = QAction('Set negative', self, checkable=True, triggered=self.setNeg)
        self.menu.addAction(self.negAction)
        self.setMenu(self.menu)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.makeMenu()

        if self.number == 8:
            self.setText(NULL)
            self.setEnabled(False)
            style = 'QPushButton{padding: 4px; background: white; border: 1px solid grey; color: grey;}' \
                    'QPushButton::menu-indicator{image: none;}'
        elif self.number == 9:
            self.setText('/')
            self.setEnabled(False)
            style = 'QPushButton{padding: 4px; background: white; border: 1px solid grey; color: grey;}' \
                    'QPushButton::menu-indicator{image: none;}'
        elif self.number == 16:
            self.setText('1')
            self.setEnabled(False)
            style = 'QPushButton{padding: 4px; background: white; border: 1px solid grey; color: grey;}' \
                    'QPushButton::menu-indicator{image: none;}'
        elif self.number == 21:
            self.setText('2')
            self.setEnabled(False)
            style = 'QPushButton{padding: 4px; background: white; border: 1px solid grey; color: grey;}' \
                    'QPushButton::menu-indicator{image: none;}'
        elif self.number == 26:
            self.setText('3')
            self.setEnabled(False)
            style = 'QPushButton{padding: 4px; background: white; border: 1px solid grey; color: grey;}' \
                    'QPushButton::menu-indicator{image: none;}'
        elif self.number == 31:
            self.setText('4')
            self.setEnabled(False)
            style = 'QPushButton{padding: 4px; background: white; border: 1px solid grey; color: grey;}' \
                    'QPushButton::menu-indicator{image: none;}'
        else:
            self.styleSheetString = 'QPushButton{{padding: 4px; background: {}; border: {}; color: {}; font: {}}}'
            self.defaultBackground = 'white'
            self.defaultBorder = '1px solid grey'
            self.defaultTextColor = 'black'

            self.flaggedBackground = 'grey'
            self.notFlaggedBackground = 'pink'

            self.flaggedBorder = '2px dashed black'
            self.notFlaggedBorder = '2px dashed red'

            self.multipleTextColor = 'green'
            self.positiveFont = 'normal'
            self.negativeFont = 'italic'

            self.background = self.defaultBackground
            self.border = self.defaultBorder
            self.textColor = self.defaultTextColor
            self.textFont = self.positiveFont

            style = self.styleSheetString.format(self.background, self.border, self.textColor, self.textFont)

        self.setStyleSheet(style)

    def resetToStar(self):
        for act in self.menu.actions()[:-3]:
            act.setChecked(False)
        self.updateSymbol()

    def selectAll(self):
        for act in self.menu.actions()[:-3]:
            act.setChecked(True)
        self.updateSymbol()

    def setNeg(self):
        if self.negAction.isChecked():
            self.positive = False
            self.textFont = self.negativeFont
        else:
            self.positive = True
            self.textFont = self.positiveFont

        style = self.styleSheetString.format(self.background, self.border, self.textColor, self.textFont)
        self.setStyleSheet(style)

    def makeMenu(self):
        self.popMenu = QMenu(self)

        self.changeEstimateAct = QAction('Flagged as estimate', self, triggered=self.changeEstimate, checkable=True)
        self.notEstimateAct = QAction('NOT flagged as estimate', self, triggered=self.notEstimate, checkable=True)

        self.changeUncertaintyAct = QAction('Flagged as uncertain', self, triggered=self.changeUncertainty,
                                            checkable=True)
        self.notUncertaintyAct = QAction('NOT flagged as uncertain', self, triggered=self.notUncertainty,
                                         checkable=True)

        self.popMenu.addAction(self.changeEstimateAct)
        self.popMenu.addAction(self.notEstimateAct)
        self.popMenu.addSeparator()
        self.popMenu.addAction(self.changeUncertaintyAct)
        self.popMenu.addAction(self.notUncertaintyAct)

    def notEstimate(self):
        # estimate checked
        if self.changeEstimateAct.isChecked():
            # not estimate checked
            if self.notEstimateAct.isChecked():
                self.changeEstimateAct.setChecked(False)
                self.isEstimate = -1
                self.border = self.notFlaggedBorder
            else:
                self.isEstimate = 1
                self.border = self.flaggedBorder
        # estimate not checked
        else:
            # not estimate checked
            if self.notEstimateAct.isChecked():
                self.isEstimate = -1
                self.border = self.notFlaggedBorder
            else:
                self.isEstimate = 0
                self.border = self.defaultBorder

        style = self.styleSheetString.format(self.background, self.border, self.textColor, self.textFont)
        self.setStyleSheet(style)

    def notUncertainty(self):
        # uncertainty checked
        if self.changeUncertaintyAct.isChecked():
            # not uncertainty checked
            if self.notUncertaintyAct.isChecked():
                self.changeUncertaintyAct.setChecked(False)
                self.isUncertain = -1
                self.background = self.notFlaggedBackground
            else:
                self.isUncertain = 1
                self.background = self.flaggedBackground
        # uncertainty not checked
        else:
            # not uncertainty checked
            if self.notUncertaintyAct.isChecked():
                self.isUncertain = -1
                self.background = self.notFlaggedBackground
            else:
                self.isUncertain = 0
                self.background = self.defaultBackground

        style = self.styleSheetString.format(self.background, self.border, self.textColor, self.textFont)
        self.setStyleSheet(style)

    def showContextMenu(self, point):
        self.popMenu.exec_(self.mapToGlobal(point))

    def changeEstimate(self):
        # estimate checked
        if self.changeEstimateAct.isChecked():
            # not estimate checked
            if self.notEstimateAct.isChecked():
                self.notEstimateAct.setChecked(False)
                self.isEstimate = 1
                self.border = self.flaggedBorder
            else:
                self.isEstimate = 1
                self.border = self.flaggedBorder
        # estimate not checked
        else:
            # not estimate checked
            if self.notEstimateAct.isChecked():
                self.isEstimate = -1
                self.border = self.notFlaggedBorder
            else:
                self.isEstimate = 0
                self.border = self.defaultBorder

        style = self.styleSheetString.format(self.background, self.border, self.textColor, self.textFont)
        self.setStyleSheet(style)

    def changeUncertainty(self):
        # uncertainty checked
        if self.changeUncertaintyAct.isChecked():
            # not uncertainty checked
            if self.notUncertaintyAct.isChecked():
                self.notUncertaintyAct.setChecked(False)
                self.isUncertain = 1
                self.background = self.notFlaggedBackground
            else:
                self.isUncertain = 1
                self.background = self.flaggedBackground
        # uncertainty not checked
        else:
            # not uncertainty checked
            if self.notUncertaintyAct.isChecked():
                self.isUncertain = -1
                self.background = self.notFlaggedBackground
            else:
                self.isUncertain = 0
                self.background = self.defaultBackground

        style = self.styleSheetString.format(self.background, self.border, self.textColor, self.textFont)
        self.setStyleSheet(style)

    def getSelectedSymbols(self):
        selectedSymbols = list()
        for act in self.menu.actions():
            if act.isChecked():
                selectedSymbols.append(act.text())
        if 'Set negative' in selectedSymbols:
            selectedSymbols.remove('Set negative')
        return selectedSymbols

    def updateSymbol(self):
        selectedSymbols = self.getSelectedSymbols()
        if selectedSymbols:
            first = selectedSymbols[0]
            self.setText(first)
            if len(selectedSymbols) >= 2:
                self.textColor = self.multipleTextColor
            else:
                self.textColor = self.defaultTextColor
        else:
            self.setText(self.initialSymbol)
            self.textColor = self.defaultTextColor

        style = self.styleSheetString.format(self.background, self.border, self.textColor, self.textFont)
        self.setStyleSheet(style)

    def value(self):
        symbols = set(self.getSelectedSymbols()) | {self.text()}
        results = {'selected': symbols,
                   'options': self.options,
                   'positive': self.positive,
                   'flag_estimate': self.isEstimate,
                   'flag_uncertain': self.isUncertain}
        return results


class TransLayout(QHBoxLayout):
    def __init__(self, hand):
        super().__init__()
        self.hand = hand
        self.setContentsMargins(0, 0, 0, 0)
        self.generateSlots()
        self.generateFields()

    def fillPredeterminedSlots(self):
        self.slot8.setText(NULL)
        self.slot9.setText('/')
        self.slot16.setText('1')
        self.slot21.setText('2')
        self.slot26.setText('3')
        self.slot31.setText('4')

    def generateSlots(self):
        #FIELD 2 (Thumb)
        self.slot2 = TransSlot(2, 2, list('LUO?'))
        self.slot3 = TransSlot(3, 2, list('{<=?'))
        self.slot4 = TransSlot(4, 2, list('HEeiFf?'))
        self.slot5 = TransSlot(5, 2, list('HEeiFf?'))

        #FIELD 3 (Thumb/Finger Contact)
        self.slot6 = TransSlot(6, 3, ['-', 't', 'fr', 'b', 'r', 'u', '?'])
        self.slot7 = TransSlot(7, 3, list('-dpM?'))
        self.slot8 = TransSlot(8, 3, [NULL])
        self.slot9 = TransSlot(9, 3, ['/'])
        self.slot10 = TransSlot(10, 3, ['-', 't', 'fr', 'b', 'r', 'u', '?'])
        self.slot11 = TransSlot(11, 3, list('-dmpM?'))
        self.slot12 = TransSlot(12, 3, ['-', '1', '?'])
        self.slot13 = TransSlot(13, 3, ['-', '2', '?'])
        self.slot14 = TransSlot(14, 3, ['-', '3', '?'])
        self.slot15 = TransSlot(15, 3, ['-', '4', '?'])

        #FIELD 4 (Index)
        self.slot16 = TransSlot(16, 4, ['1'])
        self.slot17 = TransSlot(17, 4, list('HEeiFf?'))
        self.slot18 = TransSlot(18, 4, list('HEeiFf?'))
        self.slot19 = TransSlot(19, 4, list('HEeiFf?'))

        #FIELD 5 (Middle)
        self.slot20 = TransSlot(20, 5, ['{', '<', '=', 'x', 'x+', 'x-', X_IN_BOX, '?'])
        self.slot21 = TransSlot(21, 5, ['2'])
        self.slot22 = TransSlot(22, 5, list('HEeiFf?'))
        self.slot23 = TransSlot(23, 5, list('HEeiFf?'))
        self.slot24 = TransSlot(24, 5, list('HEeiFf?'))

        #FIELD 6 (Ring)
        self.slot25 = TransSlot(25, 6, ['{', '<', '=', 'x', 'x+', 'x-', X_IN_BOX, '?'])
        self.slot26 = TransSlot(26, 6, ['3'])
        self.slot27 = TransSlot(27, 6, list('HEeiFf?'))
        self.slot28 = TransSlot(28, 6, list('HEeiFf?'))
        self.slot29 = TransSlot(29, 6, list('HEeiFf?'))

        #FIELD 7 (Middle)
        self.slot30 = TransSlot(30, 7, ['{', '<', '=', 'x', 'x+', 'x-', X_IN_BOX, '?'])
        self.slot31 = TransSlot(31, 7, ['4'])
        self.slot32 = TransSlot(32, 7, list('HEeiFf?'))
        self.slot33 = TransSlot(33, 7, list('HEeiFf?'))
        self.slot34 = TransSlot(34, 7, list('HEeiFf?'))

    def generateFields(self):
        #FIELD 2 (Thumb)
        self.field2 = TransField(number=2)
        for j in range(2, 6):
            slot = getattr(self, 'slot{}'.format(j))
            self.field2.addSlot(slot)
        self.addLayout(self.field2)

        #FIELD 3 (Thumb/Finger contact)
        self.field3 = TransField(number=3)
        for j in range(6, 16):
            slot = getattr(self, 'slot{}'.format(j))
            self.field3.addSlot(slot)
        self.addLayout(self.field3)

        #FIELD 4 (Index)
        self.field4 = TransField(number=4)
        for j in range(16, 20):
            slot = getattr(self, 'slot{}'.format(j))
            self.field4.addSlot(slot)
        self.addLayout(self.field4)

        #FIELD 5 (Middle)
        self.field5 = TransField(number=5)
        for j in range(20, 25):
            slot = getattr(self, 'slot{}'.format(j))
            self.field5.addSlot(slot)
        self.addLayout(self.field5)

        #FIELD 6 (Ring)
        self.field6 = TransField(number=6)
        for j in range(25, 30):
            slot = getattr(self, 'slot{}'.format(j))
            self.field6.addSlot(slot)
        self.addLayout(self.field6)

        #FIELD 7 (Pinky)
        self.field7 = TransField(number=7)
        for j in range(30, 35):
            slot = getattr(self, 'slot{}'.format(j))
            self.field7.addSlot(slot)
        self.addLayout(self.field7)

    def value(self):
        return (self.field2.value(),
                self.field3.value(),
                self.field4.value(),
                self.field5.value(),
                self.field6.value(),
                self.field7.value())


class TransConfigTab(QWidget):
    def __init__(self):
        super().__init__()

        self.hand1Trans = TransLayout(1)
        self.hand2Trans = TransLayout(2)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.hand1Trans)
        mainLayout.addLayout(self.hand2Trans)
        self.setLayout(mainLayout)

    def value(self):
        hand1 = list()
        for field in self.hand1Trans.value():
            for slot in field:
                slot_dict = dict()
                slot_dict['flag_estimate'] = slot['flag_estimate']
                slot_dict['flag_uncertain'] = slot['flag_uncertain']
                if slot['positive']:
                    if slot['selected'] == {'*'}:
                        slot_dict['allowed'] = {r'.+'}
                    else:
                        slot_dict['allowed'] = set(slot['selected'])
                else:
                    if slot['selected'] == {'*'}:
                        slot_dict['allowed'] = set()
                    else:
                        slot_dict['allowed'] = set(slot['options']) - set(slot['selected'])
                hand1.append(slot_dict)

        hand2 = list()
        for field in self.hand2Trans.value():
            for slot in field:
                slot_dict = dict()
                slot_dict['flag_estimate'] = slot['flag_estimate']
                slot_dict['flag_uncertain'] = slot['flag_uncertain']
                if slot['positive']:
                    if slot['selected'] == {'*'}:
                        slot_dict['allowed'] = {r'.+'}
                    else:
                        slot_dict['allowed'] = set(slot['selected'])
                else:
                    if slot['selected'] == {'*'}:
                        slot_dict['allowed'] = set()
                    else:
                        slot_dict['allowed'] = set(slot['options']) - set(slot['selected'])
                hand2.append(slot_dict)

        return tuple(hand1), tuple(hand2)


class CoderSlot(QPushButton):
    def __init__(self, corpus):
        super().__init__()
        self.corpus = corpus

        self.setContentsMargins(0, 0, 0, 0)
        self.positive = True
        self.textFont = 'normal'
        self.styleSheetString = 'QPushButton{{font: {}}}'
        style = self.styleSheetString.format(self.textFont)
        self.setStyleSheet(style)

        self.default = 'All coders'
        self.setText(self.default)

        self.setFixedWidth(250)

        self.menu = QMenu()

        self.options = sorted(list({sign.coder for sign in self.corpus}))

        for option in self.options:
            if not option:
                option = '(empty)'
            coder = QAction(option, self, checkable=True, triggered=self.updateText)
            coder.setChecked(True)
            self.menu.addAction(coder)

        self.menu.addSeparator()
        selectAllAction = QAction('Select all coders', self, checkable=False, triggered=self.selectAll)
        self.menu.addAction(selectAllAction)
        deselectAllAction = QAction('Deselect all coders', self, checkable=False, triggered=self.deselectAll)
        self.menu.addAction(deselectAllAction)

        self.menu.addSeparator()
        self.negAction = QAction('Set negative', self, checkable=True, triggered=self.setNeg)
        self.menu.addAction(self.negAction)
        self.setMenu(self.menu)

    def getSelectedCoders(self):
        selectedCoders = list()
        for act in self.menu.actions()[:-3]:
            if act.isChecked():
                selectedCoders.append(act.text())
        return selectedCoders

    def updateText(self):
        selectedCoders = self.getSelectedCoders()
        if selectedCoders:
            if selectedCoders == self.options:
                self.setText(self.default)
            else:
                first = selectedCoders[0]
                if len(selectedCoders) == 1:
                    self.setText(first)
                else:
                    self.setText(first + '+')
        else:
            self.setText('Please select at least one coder')

    def deselectAll(self):
        for act in self.menu.actions()[:-3]:
            act.setChecked(False)
        self.updateText()

    def selectAll(self):
        for act in self.menu.actions()[:-3]:
            act.setChecked(True)
        self.updateText()

    def setNeg(self):
        if self.negAction.isChecked():
            self.positive = False
            self.textFont = 'italic'
        else:
            self.positive = True
            self.textFont = 'normal'

        style = self.styleSheetString.format(self.textFont)
        self.setStyleSheet(style)

    def value(self):
        selected = {'' if coder == '(empty)' else coder for coder in self.getSelectedCoders()}
        if self.positive:
            return selected
        else:
            return set(self.options) - selected


class LastUpdateSlot(QPushButton):
    def __init__(self, corpus):
        super().__init__()
        self.corpus = corpus

        self.setContentsMargins(0, 0, 0, 0)
        self.positive = True
        self.textFont = 'normal'
        self.styleSheetString = 'QPushButton{{font: {}}}'
        style = self.styleSheetString.format(self.textFont)
        self.setStyleSheet(style)

        self.default = 'All dates'
        self.setText(self.default)

        self.setFixedWidth(250)

        self.menu = QMenu()

        self.options = sorted(list({str(sign.lastUpdated) for sign in self.corpus}))

        for option in self.options:
            if not option:
                option = '(empty)'
            date = QAction(option, self, checkable=True, triggered=self.updateText)
            date.setChecked(True)
            self.menu.addAction(date)

        self.menu.addSeparator()
        selectAllAction = QAction('Select all dates', self, checkable=False, triggered=self.selectAll)
        self.menu.addAction(selectAllAction)
        deselectAllAction = QAction('Deselect all dates', self, checkable=False, triggered=self.deselectAll)
        self.menu.addAction(deselectAllAction)

        self.menu.addSeparator()
        self.negAction = QAction('Set negative', self, checkable=True, triggered=self.setNeg)
        self.menu.addAction(self.negAction)
        self.setMenu(self.menu)

    def getSelectedDates(self):
        selectedDates = list()
        for act in self.menu.actions()[:-3]:
            if act.isChecked():
                selectedDates.append(act.text())
        return selectedDates

    def updateText(self):
        selectedDates = self.getSelectedDates()
        if selectedDates:
            if selectedDates == self.options:
                self.setText(self.default)
            else:
                first = selectedDates[0]
                if len(selectedDates) == 1:
                    self.setText(first)
                else:
                    self.setText(first + '+')
        else:
            self.setText('Please select at least one date')

    def deselectAll(self):
        for act in self.menu.actions()[:-3]:
            act.setChecked(False)
        self.updateText()

    def selectAll(self):
        for act in self.menu.actions()[:-3]:
            act.setChecked(True)
        self.updateText()

    def setNeg(self):
        if self.negAction.isChecked():
            self.positive = False
            self.textFont = 'italic'
        else:
            self.positive = True
            self.textFont = 'normal'

        style = self.styleSheetString.format(self.textFont)
        self.setStyleSheet(style)

    def value(self):
        options = set()
        for d in self.options:
            year, month, day = tuple(d.split(sep='-'))
            options.add(date(int(year), int(month), int(day)))
        #print('options:')
        #pprint(options)

        selected = set()
        for d in self.getSelectedDates():
            year, month, day = tuple(d.split(sep='-'))
            selected.add(date(int(year), int(month), int(day)))
        #print('selected:')
        #pprint(selected)

        #selected = {'' if date == '(empty)' else date for date in self.getSelectedDates()}
        if self.positive:
            return selected
        else:
            return options - selected


class TSWorker(FunctionWorker):
    def run(self):
        corpus = self.kwargs.pop('corpus')
        forearm = self.kwargs.pop('forearm')
        estimated = self.kwargs.pop('estimated')
        uncertain = self.kwargs.pop('uncertain')
        incomplete = self.kwargs.pop('incomplete')
        configuration = self.kwargs.pop('configuration')
        hand = self.kwargs.pop('hand')
        config1 = self.kwargs.pop('config1')
        config2 = self.kwargs.pop('config2')
        frequency_range = self.kwargs.pop('frequency_range')
        coder = self.kwargs.pop('coder')
        lastUpdated = self.kwargs.pop('lastUpdated')

        results = transcription_search(corpus, forearm, estimated, uncertain, incomplete, configuration, hand,
                                       frequency_range, config1, config2, coder, lastUpdated)
        self.dataReady.emit(results)


class TranscriptionSearchDialog(FunctionDialog):
    header = ['Corpus', 'Sign', 'Coder', 'Last updated', 'Token frequency', 'Note']
    about = 'Transcription search'
    name = 'transcription search'

    def __init__(self, corpus, parent, settings, recent):
        super().__init__(parent, settings, TSWorker())

        self.corpus = corpus
        self.recent = recent

        globalFrame = QGroupBox('Global options')
        globalFrame.setFixedWidth(500)
        globalLayout = QHBoxLayout()
        globalFrame.setLayout(globalLayout)

        self.forearmLogic = LogicRadioButtonGroup('vertical', 'e', title='Forearm', y='Yes', n='No', e='Either')
        self.estimateLogic = LogicRadioButtonGroup('vertical', 'e', title='Estimated', y='Yes', n='No', e='Either')
        self.uncertainLogic = LogicRadioButtonGroup('vertical', 'e', title='Uncertain', y='Yes', n='No', e='Either')
        self.incompleteLogic = LogicRadioButtonGroup('vertical', 'e', title='Incomplete', y='Yes', n='No', e='Either')

        self.configLogic = LogicRadioButtonGroup('vertical', 'e', title='Configuration', one='One-config signs', two='Two-config signs', e='Either')
        #self.configLogic.setFixedWidth(150)

        self.handCheckboxGroup = QGroupBox('Hand')
        self.box1 = QCheckBox('One-hand signs')
        self.box2 = QCheckBox('Two-hand signs (H1 == H2)')
        self.box3 = QCheckBox('Two-hand signs (H1 != H2)')

        self.box1.setChecked(True)
        self.box2.setChecked(True)
        self.box3.setChecked(True)

        vBox = QVBoxLayout()
        vBox.addWidget(self.box1)
        vBox.addWidget(self.box2)
        vBox.addWidget(self.box3)
        self.handCheckboxGroup.setLayout(vBox)
        # TODO: implement function to handle the hand widget
        #self.handCheckboxGroup.setFixedWidth(150)

        #self.handLogic = LogicRadioButtonGroup('vertical', 'e', title='Hand', one='One-hand signs', two='Two-hand signs', e='Either')
        #self.handLogic.setFixedWidth(150)

        frequencyGroup = QGroupBox('Frequency')
        frequencyGroup.setFixedWidth(100)
        freqeuncyLayout = QVBoxLayout()
        frequencyGroup.setLayout(freqeuncyLayout)
        self.minLineEdit = QLineEdit(str(self.corpus.getFrequencyRange()[0]))
        self.maxLineEdit = QLineEdit(str(self.corpus.getFrequencyRange()[1]))
        freqeuncyLayout.addWidget(QLabel('From:'))
        freqeuncyLayout.addWidget(self.minLineEdit)
        freqeuncyLayout.addWidget(QLabel('To:'))
        freqeuncyLayout.addWidget(self.maxLineEdit)

        globalLayout.addWidget(self.forearmLogic)
        globalLayout.addWidget(self.estimateLogic)
        globalLayout.addWidget(self.uncertainLogic)
        globalLayout.addWidget(self.incompleteLogic)

        config1Frame = QGroupBox('Config 1')
        config1Layout = QVBoxLayout()
        config1Frame.setLayout(config1Layout)

        self.config1 = TransConfigTab()
        self.config1.setFixedWidth(1250)
        config1Layout.addWidget(self.config1)

        config2Frame = QGroupBox('Config 2')
        config2Layout = QVBoxLayout()
        config2Frame.setLayout(config2Layout)

        self.config2 = TransConfigTab()
        self.config2.setFixedWidth(1250)
        config2Layout.addWidget(self.config2)

        self.notePanel = QLineEdit()
        self.notePanel.setPlaceholderText('Enter notes here...')

        metaInfoGroup = QGroupBox()
        metaInfoLayout = QHBoxLayout()
        metaInfoGroup.setLayout(metaInfoLayout)
        self.coderSlot = CoderSlot(self.corpus)
        self.lastUpdatedSlot = LastUpdateSlot(self.corpus)
        metaInfoLayout.addWidget(QLabel('Coder:'))
        metaInfoLayout.addWidget(self.coderSlot)
        metaInfoLayout.addWidget(QLabel('Last updated:'))
        metaInfoLayout.addWidget(self.lastUpdatedSlot)

        mainLayout = QGridLayout()
        #self.setLayout(mainLayout)
        mainLayout.addWidget(globalFrame, 0, 0, 1, 1)
        mainLayout.addWidget(frequencyGroup, 0, 1, 1, 1)
        mainLayout.addWidget(self.configLogic, 0, 2, 1, 1)
        #mainLayout.addWidget(self.handLogic, 0, 3, 1, 1)
        mainLayout.addWidget(self.handCheckboxGroup, 0, 3, 1, 1)
        mainLayout.addWidget(config1Frame, 1, 0, 1, 4)
        mainLayout.addWidget(config2Frame, 2, 0, 1, 4)
        mainLayout.addWidget(metaInfoGroup, 3, 0, 1, 2)
        mainLayout.addWidget(self.notePanel, 3, 2, 1, 2)

        #self.testButton = QPushButton('test')
        #mainLayout.addWidget(self.testButton, 4, 0)
        #self.testButton.clicked.connect(self.test)
        self.layout().insertLayout(0, mainLayout)

    #def test(self):
    #    pprint(self.lastUpdatedSlot.value())
    #     results = {'forearmLogic': self.forearmLogic.value(),
    #                'estimated': self.estimateLogic.value(),
    #                'uncertain': self.uncertainLogic.value(),
    #                'incomplete': self.incompleteLogic.value(),
    #                'configuration': self.configLogic.value(),
    #                'hand': self.handLogic.value(),
    #                'config1': self.config1.value(),
    #                'config2': self.config2.value()}
    #     pprint(results)
    #
    #     return results

    def generateKwargs(self):
        kwargs = dict()

        kwargs['corpus'] = self.corpus
        kwargs['forearm'] = self.forearmLogic.value()
        kwargs['estimated'] = self.estimateLogic.value()
        kwargs['uncertain'] = self.uncertainLogic.value()
        kwargs['incomplete'] = self.incompleteLogic.value()
        kwargs['configuration'] = self.configLogic.value()
        kwargs['hand'] = self.handLogic.value()
        kwargs['config1'] = self.config1.value()
        kwargs['config2'] = self.config2.value()
        kwargs['frequency_range'] = (float(self.minLineEdit.text()), float(self.maxLineEdit.text()))
        kwargs['coder'] = self.coderSlot.value()
        kwargs['lastUpdated'] = self.lastUpdatedSlot.value()
        self.note = self.notePanel.text()

        return kwargs

    @Slot(object)
    def setResults(self, results):
        #TODO: need to modify token frequency when implemented (right not there is not frquency info)
        #TODO: double check thread method to properly place accept()
        self.results = list()
        for sign in results:
            self.results.append({'Corpus': self.corpus.name,
                                 'Sign': sign.gloss,
                                 'Coder': sign.coder,
                                 'Last updated': str(sign.lastUpdated),
                                 'Token frequency': sign.frequency,
                                 'Note': self.note})
        self.accept()


#app = QApplication(sys.argv)
#main = TranscriptionSearchDialog(None, None, None, None)
#main.show()
#sys.exit(app.exec_())
