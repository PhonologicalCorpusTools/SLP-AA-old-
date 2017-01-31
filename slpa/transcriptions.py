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


        # #SLOT 4
        self.slot4 = TranscriptionSlot(number=4, max_length=4)
        self.lineLayout.addLayout(self.slot4)
        self.slots.append(self.slot4)

        #SLOT 5
        self.slot5 = TranscriptionSlot(number=5, max_length=4)
        self.lineLayout.addLayout(self.slot5)
        self.slots.append(self.slot5)

        # #SLOT 6
        self.slot6 = TranscriptionSlot(number=6, max_length=4)
        self.lineLayout.addLayout(self.slot6)
        self.slots.append(self.slot6)

        # #SLOT 7
        self.slot7 = TranscriptionSlot(number=7, max_length=4)
        self.lineLayout.addLayout(self.slot7)
        self.slots.append(self.slot7)


    def setComboBoxes(self, boxes):
        self.indexBox, self.middleBox, self.ringBox, self.pinkyBox = boxes

    def values(self):
        return [self.slot1.isChecked(), self.slot2.text(), self.slot3.text(), self.slot4.text(),
                self.slot5.text(), self.slot6.text(), self.slot7.text()]

    def __str__(self):
        value = self.values()
        if value[0]:
            values = ['Yes']
        else:
            values = ['No']
        values.extend(value[1:])
        values = ';'.join(values)
        return values


class TranscriptionData():

    def __init__(self, info):
        for n in range(1,8):
            setattr(self, 'slot{}'.format(n), info.pop())
        self.slot1 = True if self.slot1 == 'Yes' else False

    @property
    def slots(self):
        return ['slot1', 'slot2', 'slot3', 'slot4',
                'slot5', 'slot6', 'slot7']

class TranscriptionHint(QToolTip):

    def __init__(self):
        super().__init__()
        self.setText('The allowable symbols are:...')

class TranscriptionSlot2Validator(QRegExpValidator):

    def __init__(self, expression):
        super().__init__(expression)

    def validate(self, string, position):
        prefix,suffix = string.split('\u2205/')

class TranscriptionValidator(QRegExpValidator):

    def __init__(self, expression):
        super().__init__(expression)

    def validate(self,string, position):
        #string is the full string entered so far
        #position is the position that was changed recently
        #note that position starts counting at 1, not 0
        if '/' in string:
            print(self.regExp())
            string = string.strip()
            pass #this transcription slot can contain spaces, don't do anything
        else:
            string = string.strip()
        result = super().validate(string, position)
        print(result)
        # if result[0] == 0:
        #     return QRegExpValidator.Invalid
        # elif result[0] == 1:
        #     return QRegExpValidator.Intermediate
        # else:
        #     return QRegExpValidator.Acceptable
    #     #result[0] == INVALID, INTERMEDIATE, ACCEPTABLE
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
        # else:
        #     self.regex = QRegExp('.*')
        validator = TranscriptionValidator(self.regex)# QRegExpValidator(self.regex)
        self.setValidator(validator)
        self.cursor

    def focusInEvent(self, e):
        self.slotSelectionChanged.emit(self.slot_id)
    #     self.setStyleSheet('background: pink')
    #
    # def focusOutEvent(self, e):
    #     self.setStyleSheet(self.style)

    def mousePressEvent(self, e):
        self.setFocus(Qt.TabFocusReason)
        #TranscriptionLineEdit objects don't allow you to set focus by with the mouse, since
        #that has the side-effect that mousing away while typing can change the focus.
        #the purpose of this method is to trick the application into thinking the user tabbed-in instead of clicking


class TranscriptionSlot(QHBoxLayout):

    slotSelectionChanged = Signal(int)
    #masks = {2: 'AXAA', 3: 'AAAA{}/dddd'.format('\u2205'), 4: '1AAA', 5: 'A2AA', 6: 'AA3A', 7: 'AAA4'}
    masks = {2: 'AXAA', 3: 'AAAA{}dddd'.format('\u2205'), 4: '1AAA', 5: 'A2AA', 6: 'AA3A', 7: 'AAA4'}

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
        #self.transcription.setPlaceholderText('_ ' * self.transcription.maxLength())

        self.addWidget(self.left_bracket)
        self.addWidget(self.transcription)
        self.addWidget(self.right_bracket)

        try:
            mask = TranscriptionSlot.masks[self.number]
            self.transcription.setInputMask(mask)
        except KeyError:
            pass #slot1 is a checkbox and doesn't have a mask

    def text(self):
        return self.transcription.text()
