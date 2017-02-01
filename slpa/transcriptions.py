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
        self.fields = list()
        self.lineLayout = QHBoxLayout()
        self.lineLayout.setContentsMargins(-1,0,-1,-1)

        self.generateSlots()

        #FIELD 1 (Forearm)
        self.lineLayout.addWidget(QLabel('['))
        self.field1 = TranscriptionCheckBox(1)
        self.lineLayout.addWidget(self.field1)
        self.fields.append(self.field1)
        self.lineLayout.addWidget(QLabel(']<font size="5"><b><sub>1</sub></b></font>'))
        self.addLayout(self.lineLayout)

        #FIELD 2 (Thumb)
        self.field2 = TranscriptionField(number=2)
        for j in range(2,6):
            self.field2.addSlot(getattr(self, 'slot{}'.format(j)))
        self.lineLayout.addLayout(self.field2)
        self.fields.append(self.field2)

        #FIELD 3 (Thumb/Finger contact)
        self.field3 = TranscriptionField(number=3)
        for j in range(6,16):
            self.field3.addSlot(getattr(self, 'slot{}'.format(j)))
        self.lineLayout.addLayout(self.field3)
        self.fields.append(self.field3)

        #FIELD 4 (Index)
        self.field4 = TranscriptionField(number=4)
        for j in range(16,20):
            self.field4.addSlot(getattr(self, 'slot{}'.format(j)))
        self.lineLayout.addLayout(self.field4)
        self.fields.append(self.field4)

        #FIELD 5 (Middle)
        self.field5 = TranscriptionField(number=5)
        for j in range(20,25):
            self.field5.addSlot(getattr(self, 'slot{}'.format(j)))
        self.lineLayout.addLayout(self.field5)
        self.fields.append(self.field5)

        #FIELD 6 (Ring)
        self.field6 = TranscriptionField(number=6)
        for j in range(25,30):
            self.field6.addSlot(getattr(self, 'slot{}'.format(j)))
        self.lineLayout.addLayout(self.field6)
        self.fields.append(self.field6)

        #FIELD 7 (Pinky)
        self.field7 = TranscriptionField(number=7)
        for j in range(30,35):
            self.field7.addSlot(getattr(self, 'slot{}'.format(j)))
        self.lineLayout.addLayout(self.field7)
        self.fields.append(self.field7)

    def generateSlots(self):
        #FIELD 1 (Forearm)
        #This field is a check box, and does not contain any slots

        #FIELD 2 (Thumb)
        self.slot2 = TranscriptionSlot(2, '[LUO]', list('LUO'))
        self.slot3 = TranscriptionSlot(3, '[{<=]', list('{<='))
        self.slot4 = TranscriptionSlot(4, '[HEefF]', list('HEefF'))
        self.slot5 = TranscriptionSlot(5, '[HEefF]', list('HEefF'))

        #FIELD 3 (Thumb/Finger Contact)
        self.slot6 = TranscriptionSlot(6, '[ftbru]', list('ftbru'))
        self.slot7 = TranscriptionSlot(7, '[tdpM]', list('tdpM'))
        self.slot8 = TranscriptionSlot(8, '[fbru]', list('fbru'))
        self.slot9 = TranscriptionSlot(9, '[tdmpM]', list('tdmpM'))
        self.slot10 = TranscriptionSlot(10, '\u2205', ['\u2205'])
        self.slot11 = TranscriptionSlot(11, '/', ['/'])
        self.slot12 = TranscriptionSlot(12, '[-1\s]', ['-','1'])
        self.slot13 = TranscriptionSlot(13, '[-2\s]', ['-','2'])
        self.slot14 = TranscriptionSlot(14, '[-3\s]', ['-','3'])
        self.slot15 = TranscriptionSlot(15, '[-4\s]', ['-','4'])

        #FIELD 4 (Index)
        self.slot16 = TranscriptionSlot(16, '1', ['1'])
        self.slot17 = TranscriptionSlot(17, '[EFHi]', list('EFHi'))
        self.slot18 = TranscriptionSlot(18, '[EFHi]', list('EFHi'))
        self.slot19 = TranscriptionSlot(19, '[EFHi]', list('EFHi'))

        #FIELD 5 (Middle)
        self.slot20 = TranscriptionSlot(20, '[{<=x(x+)(x-)\u2327]', ['{','<','=','x','x+','x-','\u2327'])
        self.slot21 = TranscriptionSlot(21, '2', ['2'])
        self.slot22 = TranscriptionSlot(22, '[EFHi]', list('EFHi'))
        self.slot23 = TranscriptionSlot(23, '[EFHi]', list('EFHi'))
        self.slot24 = TranscriptionSlot(24, '[EFHi]', list('EFHi'))

        #FIELD 6 (Ring)
        self.slot25 = TranscriptionSlot(25, '[{<=x(x+)(x-)\u2327]', ['{','<','=','x','x+','x-','\u2327'])
        self.slot26 = TranscriptionSlot(26, '3', ['3'])
        self.slot27 = TranscriptionSlot(27, '[EFHi]', list('EFHi'))
        self.slot28 = TranscriptionSlot(28, '[EFHi]', list('EFHi'))
        self.slot29 = TranscriptionSlot(29, '[EFHi]', list('EFHi'))

        #FIELD 7 (Middle)
        self.slot30 = TranscriptionSlot(30, '[{<=x(x+)(x-)\u2327]', ['{','<','=','x','x+','x-','\u2327'])
        self.slot31 = TranscriptionSlot(31, '4', ['4'])
        self.slot32 = TranscriptionSlot(32, '[EFHi]', list('EFHi'))
        self.slot33 = TranscriptionSlot(33, '[EFHi]', list('EFHi'))
        self.slot34 = TranscriptionSlot(34, '[EFHi]', list('EFHi'))

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


class TranscriptionCompleter(QCompleter):

    def __init__(self, options, lineEditWidget):
        super().__init__(options, lineEditWidget)
        self.setCaseSensitivity(Qt.CaseSensitive)
        self.setCompletionMode(QCompleter.UnfilteredPopupCompletion)

class TranscriptionSlot(QLineEdit):

    def __init__(self, num, regex, completer_options):
        super().__init__()
        self.num = num
        self.setValidator(QRegExpValidator(QRegExp(regex)))
        self.setMaxLength(1)
        self.setFixedWidth(30)
        self.setFocusPolicy(Qt.TabFocus)
        completer = TranscriptionCompleter(completer_options, self)
        self.setCompleter(completer)
        self.completer().activated.connect(self.setText)

        if self.num == 10:
            self.setText('\u2205')
            self.setEnabled(False)
        elif self.num == 11:
            self.setText('/')
            self.setEnabled(False)
        elif self.num == 16:
            self.setText('1')
            self.setEnabled(False)
        elif self.num == 21:
            self.setText('2')
            self.setEnabled(False)
        elif self.num == 26:
            self.setText('3')
            self.setEnabled(False)
        elif self.num == 31:
            self.setText('4')
            self.setEnabled(False)

    def focusInEvent(self, e):
        self.completer().complete()

    def mousePressEvent(self, e):
        self.setFocus(Qt.TabFocusReason)

    def keyPressEvent(self, e):
        self.completer().complete()
        super().keyPressEvent(e)

class TranscriptionField(QHBoxLayout):

    slotSelectionChanged = Signal(int)
    masks = {2: 'AXAA', 3: 'AAAA{}dddd'.format('\u2205'), 4: '1AAA', 5: 'A2AA', 6: 'AA3A', 7: 'AAA4'}

    def __init__(self, number):
        super().__init__()
        self.number = number
        self.name = 'field{}'.format(self.number)
        self.left_bracket = QLabel('[')
        self.right_bracket = QLabel(']<font size="5"><b><sub>{}</sub></b></font>'.format(self.number))
        self.transcription = QHBoxLayout()
        # self.transcription = TranscriptionLineEdit(self.number)
        # self.transcription.setMaxLength(max_length)
        # self.transcription.setFont(TranscriptionLayout.defaultFont)
        # width = TranscriptionLayout.fontMetric.boundingRect('_ ' * (self.transcription.maxLength() + 1)).width()
        # self.transcription.setFixedWidth(width)
        #self.transcription.setPlaceholderText('_ ' * self.transcription.maxLength())

        self.addWidget(self.left_bracket)
        self.addLayout(self.transcription)
        self.addWidget(self.right_bracket)

    # def text(self):
    #     return self.transcription.text()

    def addSlot(self, slot):
        self.transcription.addWidget(slot)
