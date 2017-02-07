from .imports import *
from .handshapes import Fingers
X_IN_BOX = '\u2327'
NULL = '\u2205'


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
        self.slots = list()
        self.lineLayout = QHBoxLayout()
        self.lineLayout.setContentsMargins(-1,0,-1,-1)

        self.generateSlots()

        #FIELD 1 (Forearm)
        self.lineLayout.addWidget(QLabel('['))
        self.field1 = TranscriptionCheckBox(1)
        self.slot1 = self.field1
        self.slots.append(self.slot1)
        self.lineLayout.addWidget(self.field1)
        self.fields.append(self.field1)
        self.lineLayout.addWidget(QLabel(']<font size="5"><b><sub>1</sub></b></font>'))
        self.addLayout(self.lineLayout)

        #FIELD 2 (Thumb)
        self.field2 = TranscriptionField(number=2)
        for j in range(2,6):
            slot = getattr(self, 'slot{}'.format(j))
            self.field2.addSlot(slot)
            self.slots.append(slot)
        self.lineLayout.addLayout(self.field2)
        self.fields.append(self.field2)

        #FIELD 3 (Thumb/Finger contact)
        self.field3 = TranscriptionField(number=3)
        for j in range(6,16):
            slot = getattr(self, 'slot{}'.format(j))
            self.field3.addSlot(slot)
            self.slots.append(slot)
        self.lineLayout.addLayout(self.field3)
        self.fields.append(self.field3)

        #FIELD 4 (Index)
        self.field4 = TranscriptionField(number=4)
        for j in range(16,20):
            slot = getattr(self, 'slot{}'.format(j))
            self.field4.addSlot(slot)
            self.slots.append(slot)
        self.lineLayout.addLayout(self.field4)
        self.fields.append(self.field4)

        #FIELD 5 (Middle)
        self.field5 = TranscriptionField(number=5)
        for j in range(20,25):
            slot = getattr(self, 'slot{}'.format(j))
            self.field5.addSlot(slot)
            self.slots.append(slot)
        self.lineLayout.addLayout(self.field5)
        self.fields.append(self.field5)

        #FIELD 6 (Ring)
        self.field6 = TranscriptionField(number=6)
        for j in range(25,30):
            slot = getattr(self, 'slot{}'.format(j))
            self.field6.addSlot(slot)
            self.slots.append(slot)
        self.lineLayout.addLayout(self.field6)
        self.fields.append(self.field6)

        #FIELD 7 (Pinky)
        self.field7 = TranscriptionField(number=7)
        for j in range(30,35):
            slot = getattr(self, 'slot{}'.format(j))
            self.field7.addSlot(slot)
            self.slots.append(slot)
        self.lineLayout.addLayout(self.field7)
        self.fields.append(self.field7)

    def generateSlots(self):
        #FIELD 1 (Forearm)
        #This field is a check box, and does not contain any slots

        #FIELD 2 (Thumb)
        self.slot2 = TranscriptionSlot(2, 2, '[LUO]', list('LUO'))
        self.slot3 = TranscriptionSlot(3, 2, '[{<=]', list('{<='))
        self.slot4 = TranscriptionSlot(4, 2, '[HEefF]', list('HEefF'))
        self.slot5 = TranscriptionSlot(5, 2, '[HEefF]', list('HEefF'))

        #FIELD 3 (Thumb/Finger Contact)
        self.slot6 = TranscriptionSlot(6, 3, '[ftbru]', list('ftbru'))
        self.slot7 = TranscriptionSlot(7, 3, '[tdpM]', list('tdpM'))
        self.slot8 = TranscriptionSlot(8, 3, '[fbru]', list('fbru'))
        self.slot9 = TranscriptionSlot(9, 3, '[tdmpM]', list('tdmpM'))
        self.slot10 = TranscriptionSlot(10, 3, NULL, [NULL])
        self.slot11 = TranscriptionSlot(11, 3, '/', ['/'])
        self.slot12 = TranscriptionSlot(12, 3, '[-1\s]', ['-','1'])
        self.slot13 = TranscriptionSlot(13, 3, '[-2\s]', ['-','2'])
        self.slot14 = TranscriptionSlot(14, 3, '[-3\s]', ['-','3'])
        self.slot15 = TranscriptionSlot(15, 3, '[-4\s]', ['-','4'])

        #FIELD 4 (Index)
        self.slot16 = TranscriptionSlot(16, 4, '1', ['1'])
        self.slot17 = TranscriptionSlot(17, 4, '[EFHi]', list('EFHi'))
        self.slot18 = TranscriptionSlot(18, 4, '[EFHi]', list('EFHi'))
        self.slot19 = TranscriptionSlot(19, 4, '[EFHi]', list('EFHi'))

        #FIELD 5 (Middle)
        self.slot20 = TranscriptionSlot(20, 5, '[{<=\u2327x(?=-+$)]', ['{','<','=','x','x+','x-','\u2327'])
        self.slot21 = TranscriptionSlot(21, 5, '2', ['2'])
        self.slot22 = TranscriptionSlot(22, 5, '[EFHi]', list('EFHi'))
        self.slot23 = TranscriptionSlot(23, 5, '[EFHi]', list('EFHi'))
        self.slot24 = TranscriptionSlot(24, 5, '[EFHi]', list('EFHi'))

        #FIELD 6 (Ring)
        self.slot25 = TranscriptionSlot(25, 6, '[{<=x(x+)(x-)\u2327]', ['{','<','=','x','x+','x-','\u2327'])
        self.slot26 = TranscriptionSlot(26, 6, '3', ['3'])
        self.slot27 = TranscriptionSlot(27, 6, '[EFHi]', list('EFHi'))
        self.slot28 = TranscriptionSlot(28, 6, '[EFHi]', list('EFHi'))
        self.slot29 = TranscriptionSlot(29, 6, '[EFHi]', list('EFHi'))

        #FIELD 7 (Middle)
        self.slot30 = TranscriptionSlot(30, 7, '[{<=x(x+)(x-)\u2327]', ['{','<','=','x','x+','x-','\u2327'])
        self.slot31 = TranscriptionSlot(31, 7, '4', ['4'])
        self.slot32 = TranscriptionSlot(32, 7, '[EFHi]', list('EFHi'))
        self.slot33 = TranscriptionSlot(33, 7, '[EFHi]', list('EFHi'))
        self.slot34 = TranscriptionSlot(34, 7, '[EFHi]', list('EFHi'))


    def __str__(self):
        return ','.join(self.values())

    def values(self):
        data = [self.slot1.isChecked()]
        data.extend([slot.text() for slot in self.slots[1:]])
        return data

class TranscriptionCompleter(QCompleter):

    def __init__(self, options, lineEditWidget):
        super().__init__(options, lineEditWidget)
        self.setCaseSensitivity(Qt.CaseSensitive)
        self.setCompletionMode(QCompleter.UnfilteredPopupCompletion)

class TranscriptionSlot(QLineEdit):

    slotSelectionChanged = Signal(int)

    def __init__(self, num, field, regex, completer_options):
        super().__init__()
        self.num = num
        self.field = field
        self.setValidator(QRegExpValidator(QRegExp(regex)))
        if self.num in [20,25,30]:
            self.setMaxLength(2)
            #these slots are the only ones that can contain digraphs, namely 'x+' and 'x-'
        else:
            self.setMaxLength(1)
        self.setFixedWidth(30)
        self.setFocusPolicy(Qt.TabFocus)
        completer = TranscriptionCompleter(completer_options, self)
        self.setCompleter(completer)
        self.completer().activated.connect(self.completerActivated)

        if self.num == 10:
            self.setText(NULL)
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

    def completerActivated(self, e):
        self.setText(e)
        #add automatic tab to next widget

    def focusInEvent(self, e):
        self.completer().complete()
        self.slotSelectionChanged.emit(self.field)

    def mousePressEvent(self, e):
        self.setFocus(Qt.TabFocusReason)

    def keyPressEvent(self, e):
        key = e.key()
        if self.num in [20, 25, 30]:
            if key == 90:# == Qt.Key_Z:
                self.completer().setCurrentRow(5)
                self.setText('x-')
            elif key == 67:# == Qt.Key_C
                self.completer().setCurrentRow(4)
                self.setText('x+')
            elif key == 83:# == Qt.Key_S
                self.completer().setCurrentRow(6)
                self.setText(X_IN_BOX)
        self.completer().complete()
        super().keyPressEvent(e)


class TranscriptionField(QHBoxLayout):

    slotSelectionChanged = Signal(int)

    def __init__(self, number):
        super().__init__()
        self.number = number
        self.name = 'field{}'.format(self.number)
        self.left_bracket = QLabel('[')
        self.right_bracket = QLabel(']<font size="5"><b><sub>{}</sub></b></font>'.format(self.number))
        self.transcription = QHBoxLayout()

        self.addWidget(self.left_bracket)
        self.addLayout(self.transcription)
        self.addWidget(self.right_bracket)

    def addSlot(self, slot):
        self.transcription.addWidget(slot)
