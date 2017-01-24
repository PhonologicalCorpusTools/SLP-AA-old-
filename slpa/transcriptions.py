from .imports import *
from .handshapes import Fingers


class TranscriptionCheckBox(QCheckBox):

    slotSelectionChanged = Signal(int)

    def __init__(self, slot_id, parent=None):
        super().__init__(parent)
        self.slot_id = slot_id
        self.stateChanged.connect(lambda x: self.slotSelectionChanged.emit(0))

class TranscriptionLayout(QVBoxLayout):

    defaultFont = QFont('Arial', 12)
    fontMetric = QFontMetricsF(defaultFont)

    def __init__(self, hand=None):
        QVBoxLayout.__init__(self)

        self.hand = hand
        self.slots = list()
        self.lineLayout = QHBoxLayout()
        self.lineLayout.setContentsMargins(-1,0,-1,-1)

        #SLOT 1
        self.lineLayout.addWidget(QLabel('['))
        self.slot1 = TranscriptionCheckBox(1)
        self.lineLayout.addWidget(self.slot1)
        self.slots.append(self.slot1)
        self.lineLayout.addWidget(QLabel(']<font size="5"><b><sub>1</sub></b></font>'))
        self.addLayout(self.lineLayout)

        #SLOT 2
        self.slot2 = TranscriptionSlot(number=2, max_length=4)
        self.lineLayout.addLayout(self.slot2)
        self.slots.append(self.slot2)

        #SLOT 3
        self.slot3 = TranscriptionSlot(number=3, max_length=8)
        self.lineLayout.addLayout(self.slot3)
        self.slots.append(self.slot3)
        # self.lineLayout.addWidget(QLabel('['))
        # self.slot3a = TranscriptionLineEdit(3)
        # self.slot3a.setMaxLength(2)
        # self.slot3a.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot3a.maxLength() + 1)).width()
        # self.slot3a.setFixedWidth(width)
        # self.slot3a.setPlaceholderText('_ '*self.slot3a.maxLength())
        # self.lineLayout.addWidget(self.slot3a)
        # nulltext = QLineEdit()
        # nulltext.setText(u'\u2205/')
        # nulltext.setEnabled(False)
        # nulltext.setFixedWidth(fontMetric.boundingRect('_ _').width())
        # self.lineLayout.addWidget(nulltext)#(QLabel(u'\u2205/'))
        # self.slot3b = TranscriptionLineEdit(3)
        # self.slot3b.setMaxLength(6)
        # self.slot3b.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot3b.maxLength() + 1)).width()
        # self.slot3b.setFixedWidth(width)
        # self.slot3b.setPlaceholderText('_ '*self.slot3b.maxLength())
        # self.lineLayout.addWidget(self.slot3b)
        # self.lineLayout.addWidget(QLabel(']<font size="5"><b><sub>3</sub></b></font>'))

        # #SLOT 4
        self.slot4 = TranscriptionSlot(number=4, max_length=4)
        self.lineLayout.addLayout(self.slot4)
        self.slots.append(self.slot4)
        # self.lineLayout.addWidget(QLabel('[1'))
        # self.slot4 = TranscriptionLineEdit(4)
        # self.slot4.setMaxLength(3)
        # self.slot4.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot4.maxLength() + 1)).width()
        # self.slot4.setFixedWidth(width)
        # self.slot4.setPlaceholderText('_ '*self.slot4.maxLength())
        # self.lineLayout.addWidget(self.slot4)
        # self.lineLayout.addWidget(QLabel(']<font size="5"><b><sub>4</sub></b></font>'))
        #
        # #SLOT 5
        self.slot5 = TranscriptionSlot(number=5, max_length=4)
        self.lineLayout.addLayout(self.slot5)
        self.slots.append(self.slot5)
        # self.lineLayout.addWidget(QLabel('['))
        # self.slot5a = TranscriptionLineEdit(5)
        # self.slot5a.setMaxLength(1)
        # self.slot5a.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot5a.maxLength() + 1)).width()
        # self.slot5a.setFixedWidth(width)
        # self.slot5a.setPlaceholderText(('_'*self.slot5a.maxLength()))
        # self.lineLayout.addWidget(self.slot5a)
        # self.lineLayout.addWidget(QLabel('2'))
        # self.slot5b = TranscriptionLineEdit(5)
        # self.slot5b.setMaxLength(3)
        # self.slot5b.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot5b.maxLength() + 1)).width()
        # self.slot5b.setFixedWidth(width)
        # self.slot5b.setPlaceholderText('_ '*self.slot5b.maxLength())
        # self.lineLayout.addWidget(self.slot5b)
        # self.lineLayout.addWidget(QLabel(']<font size="5"><b><sub>5</sub></b></font>'))
        #
        # #SLOT 6
        self.slot6 = TranscriptionSlot(number=6, max_length=4)
        self.lineLayout.addLayout(self.slot6)
        self.slots.append(self.slot6)
        # self.lineLayout.addWidget(QLabel('['))
        # self.slot6a = TranscriptionLineEdit(6)
        # self.slot6a.setMaxLength(1)
        # self.slot6a.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot6a.maxLength() + 1)).width()
        # self.slot6a.setFixedWidth(width)
        # self.slot6a.setPlaceholderText('_ '*self.slot6a.maxLength())
        # self.lineLayout.addWidget(self.slot6a)
        # self.lineLayout.addWidget(QLabel('3'))
        # self.slot6b = TranscriptionLineEdit(6)
        # self.slot6b.setMaxLength(3)
        # self.slot6b.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot6b.maxLength() + 1)).width()
        # self.slot6b.setFixedWidth(width)
        # self.slot6b.setPlaceholderText('_ '*self.slot6b.maxLength())
        # self.lineLayout.addWidget(self.slot6b)
        # self.lineLayout.addWidget(QLabel(']<font size="5"><b><sub>6</sub></b></font>'))
        #
        # #SLOT 7
        self.slot7 = TranscriptionSlot(number=7, max_length=4)
        self.lineLayout.addLayout(self.slot7)
        self.slots.append(self.slot7)
        # self.lineLayout.addWidget(QLabel('['))
        # self.slot7a = TranscriptionLineEdit(7)
        # self.slot7a.setMaxLength(1)
        # self.slot7a.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot7a.maxLength() + 1)).width()
        # self.slot7a.setFixedWidth(width)
        # self.slot7a.setPlaceholderText('_'*self.slot7a.maxLength())
        # self.lineLayout.addWidget(self.slot7a)
        # self.lineLayout.addWidget(QLabel('4'))
        # self.slot7b = TranscriptionLineEdit(7)
        # self.slot7b.setMaxLength(3)
        # self.slot7b.setFont(defaultFont)
        # width = fontMetric.boundingRect('_ ' * (self.slot7b.maxLength() + 1)).width()
        # self.slot7b.setFixedWidth(width)
        # self.slot7b.setPlaceholderText('_ '*self.slot7b.maxLength())
        # self.lineLayout.addWidget(self.slot7b)
        # self.lineLayout.addWidget(QLabel(']<font size="5"><b><sub>7</sub></b></font>'))

    def setComboBoxes(self, boxes):
        self.indexBox, self.middleBox, self.ringBox, self.pinkyBox = boxes

    def values(self):
        return [self.slot1.isChecked(), self.slot2.text(), self.slot3a.text(), self.slot3b.text(), self.slot4.text(),
                self.slot5a.text(), self.slot5b.text(), self.slot6a.text(), self.slot6b.text(),
                self.slot7a.text(), self.slot7b.text()]

    def __str__(self):
        value = self.values()
        if value[0]:
            values = ['Yes']
        else:
            values = ['No']
        values.extend(value[1:])
        values = ';'.join(values)
        return values

    def updateFromComboBoxes(self):
        indexText = self.indexBox.currentText().replace(',','')
        self.slot4.setText(indexText)
        middleText = self.middleBox.currentText().replace(',','')
        #self.slot5a.setText(middleText[0])
        self.slot5b.setText(middleText)#[1:])
        ringText = self.ringBox.currentText().replace(',','')
        #self.slot6a.setText(ringText[0])
        self.slot6b.setText(ringText)#[1:])
        pinkyText = self.pinkyBox.currentText().replace(',','')
        #self.slot7a.setText(pinkyText[0])
        self.slot7b.setText(pinkyText)#[1:])

class TranscriptionData():

    def __init__(self, info):
        self.slot1 = True if info[0] == 'Yes' else False
        self.slot2 = info[1]
        self.slot3a = info[2]
        self.slot3b = info[3]
        self.slot4 = info[4]
        self.slot5a = info[5]
        self.slot5b = info[6]
        self.slot6a = info[7]
        self.slot6b = info[8]
        self.slot7a = info[9]
        self.slot7b = info[10]

    @property
    def slots(self):
        return ['slot1', 'slot2', 'slot3a', 'slot3b', 'slot4',
                'slot5a', 'slot5b', 'slot6a', 'slot6b', 'slot7a', 'slot7b']

class TranscriptionHint(QToolTip):

    def __init__(self):
        super().__init__()
        self.setText('The allowable symbols are:...')

class TranscriptionValidator(QRegExpValidator):

    def __init__(self, expression):
        super().__init__(expression)

    def validate(self,string, position):
        #note that position starts counting at 1, not 0
        result = super().validate(string, position)
        if result == QRegExpValidator.Invalid:
            pass

        return result

class TranscriptionCompleter(QCompleter):

    def __init__(self, options):
        super().__init__(options)



class TranscriptionLineEdit(QLineEdit):

    slotSelectionChanged = Signal(int)

    def __init__(self, slot_id, parent=None):
        super().__init__(parent)
        self.slot_id = slot_id
        self.style = 'border:0px;background:#ffffff'
        self.setStyleSheet(self.style)
        self.setFocusPolicy(Qt.TabFocus)
        for finger in Fingers:
            if finger.num == slot_id:
                self.regex = QRegExp(finger.symbols)
                break
        else:
            self.regex = QRegExp('.*')
        validator = TranscriptionValidator(self.regex)# QRegExpValidator(self.regex)
        self.setValidator(validator)

    def focusInEvent(self, e):
        self.slotSelectionChanged.emit(self.slot_id)
        self.setStyleSheet('background: pink')

    def focusOutEvent(self, e):
        self.setStyleSheet(self.style)

    def mousePressEvent(self, e):
        self.setFocus(Qt.TabFocusReason)
        pos = self.cursorPosition()
        print(pos)
        #TranscriptionLineEdit objects don't allow you to set focus by with the mouse, since
        #that has the side-effect that mousing away while typing can change the focus.
        #the purpose of this method is to trick the application into thinking the user tabbed-in instead of clicking

    def enterEvent(self, e):
        pass

    def leaveEvent(self, e):
        pass



class TranscriptionSlot(QHBoxLayout):

    slotSelectionChanged = Signal(int)
    masks = {2: 'AXAA', 3: 'AAA{}/dddd'.format(u'\u2205'), 4: '1AAA', 5: 'A2AA', 6: 'AA3A', 7: 'AAA4'}

    def __init__(self, number, max_length):
        super().__init__()
        self.number = number
        self.name = 'slot{}'.format(self.number)
        self.left_bracket = QLabel('[')
        self.right_bracket = QLabel(']<font size="5"><b><sub>{}</sub></b></font>'.format(self.number))
        self.transcription = TranscriptionLineEdit(self.number)
        self.transcription.setMaxLength(max_length)
        self.transcription.setFont(TranscriptionLayout.defaultFont)
        width = TranscriptionLayout.fontMetric.boundingRect('_ ' * (self.transcription.maxLength() + 1)).width()
        self.transcription.setFixedWidth(width)
        self.transcription.setPlaceholderText('_ ' * self.transcription.maxLength())

        self.addWidget(self.left_bracket)
        self.addWidget(self.transcription)
        self.addWidget(self.right_bracket)

        try:
            mask = TranscriptionSlot.masks[self.number]
            self.transcription.setInputMask(mask)

        except KeyError:
            pass #slot1 is a checkbox and this doesn't apply


