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
        self.slot4 = TranscriptionSlot(4, 2, '[EFHi]', list('EFHi'))
        self.slot5 = TranscriptionSlot(5, 2, '[EFHi]', list('EFHi'))

        #FIELD 3 (Thumb/Finger Contact)
        self.slot6 = TranscriptionSlot(6, 3, '[fbru]', list('fbru'))
        self.slot7 = TranscriptionSlot(7, 3, '[tdpM]', list('tdpM'))
        self.slot8 = TranscriptionSlot(8, 3, NULL, [NULL])
        self.slot9 = TranscriptionSlot(9, 3, '/', ['/'])
        self.slot10 = TranscriptionSlot(10, 3, '[fbru]', list('fbru'))
        self.slot11 = TranscriptionSlot(11, 3, '[tdmpM]', list('tdmpM'))
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
        self.regex = regex
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

        if self.num == 8:
            self.setText(NULL)
            self.setEnabled(False)
            self.setToolTip('Slot 8. Represents the thumb. Always marked as {}.'.format(NULL))
        elif self.num == 9:
            self.setText('/')
            self.setEnabled(False)
            self.setToolTip('Slot 9. Represents contact. Always marked as /.')
        elif self.num == 16:
            self.setText('1')
            self.setEnabled(False)
            self.setToolTip('Slot 16. Represents index finger. Always marked as 1.')
        elif self.num == 21:
            self.setText('2')
            self.setEnabled(False)
            self.setToolTip('Slot 21. Represents middle finger. Always marked as 2.')
        elif self.num == 26:
            self.setText('3')
            self.setEnabled(False)
            self.setToolTip('Slot 26. Represents ring finger. Always marked as 3.')
        elif self.num == 31:
            self.setText('4')
            self.setEnabled(False)
            self.setToolTip('Slot 31. Represents pinky finger. Always marked as 4.')

    def __eq__(self, other):
        return self.text() == other.text()

    def __ne__(self, other):
        return not self.__eq__(other)

    @Slot(bool)
    def changeValidatorState(self, unrestricted):
        if unrestricted:
            self.setValidator(QRegExpValidator(QRegExp('.*')))
        else:
            self.setValidator(QRegExpValidator(QRegExp(self.regex)))

    def completerActivated(self, e):
        self.setText(e)
        #add automatic tab to next widget

    def focusInEvent(self, e):
        self.completer().complete()
        self.slotSelectionChanged.emit(self.num)

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

class TranscriptionInfo(QGridLayout):

    def __init__(self):
        super().__init__()

        titleFont = QFont('Arial', 15)
        infoFont = QFont('Arial', 12)

        self.fieldTypeTitle = QLabel('Field type')
        self.fieldTypeTitle.setFont(titleFont)
        self.fieldTypeInfo = QLabel('None selected')
        self.fieldTypeInfo.setFont(infoFont)

        self.fieldNumberTitle = QLabel('Field number')
        self.fieldNumberTitle.setFont(titleFont)
        self.fieldNumberInfo = QLabel('None selected')
        self.fieldNumberInfo.setFont(infoFont)

        self.slotNumberTitle = QLabel('Slot number')
        self.slotNumberTitle.setFont(titleFont)
        self.slotNumberInfo = QLabel('None selected')
        self.slotNumberInfo.setFont(infoFont)

        self.slotTypeTitle = QLabel('Slot type')
        self.slotTypeInfo = QLabel('None selected')
        self.slotTypeTitle.setFont(titleFont)
        self.slotTypeInfo.setFont(infoFont)
        self.slotTypeInfo.setWordWrap(True)

        self.slotOptionsTitle = QLabel('Permitted characters')
        self.slotOptionsInfo = QLabel('None selected')
        self.slotOptionsTitle.setFont(titleFont)
        self.slotOptionsInfo.setFont(infoFont)
        self.slotOptionsInfo.setWordWrap(True)

        tuples = [(self.fieldNumberTitle, self.fieldNumberInfo), (self.fieldTypeTitle, self.fieldTypeInfo),
                  (self.slotNumberTitle, self.slotNumberInfo), (self.slotTypeTitle, self.slotTypeInfo),
                  (self.slotOptionsTitle, self.slotOptionsInfo)]
        for row in range(5):
            title,info = tuples.pop(0)
            self.addWidget(title, row, 0)
            self.addWidget(info, row, 1)

        self.purposeDict = {1: 'Shows if forearm is involved',
                            2: 'Thumb oppositional positions (CM rotation)',
                            3: 'Thumb abduction/adduction(CM adduction)',
                            4: 'Thumb MCP flexion',
                            5: 'Thumb DIP flexion',
                            6: 'Thumb surface options',
                            7: 'Thumb bone options',
                            #8 always null
                            #9 always forward slash
                            10: 'Finger surface options',
                            11: 'Finger bone options',
                            12: 'Index/thumb contact',
                            13: 'Middle/thumb contact',
                            14: 'Ring/thumb contact',
                            15: 'Pinky/thumb contact',
                            #16 always 1,
                            17: 'Index MCP flexion',
                            18: 'Index PIP flexion',
                            19: 'Index DIP flexion',
                            20: 'Index/middle contact',
                            #21 always 2,
                            22: 'Middle MCP flexion',
                            23: 'Middle PIP flexion',
                            24: 'Middle DIP flexion',
                            25: 'Middle/ring contact',
                            #26 always 3
                            27: 'Ring MCP flexion',
                            28: 'Ring PIP flexion',
                            29: 'Ring DIP flexion',
                            30: 'Ring/pinky contact',
                            #31 always 4
                            32: 'Pinky MCP flexion',
                            33: 'Pinky PIP flexion',
                            34: 'Pinky DIP flexion'}
        self.optionsDict = {1: 'Either on or off (checkbox)',
                              2: 'L (lateral)\nU (unopposed)\nO (opposed)',
                              3: '{ (full abduction)\n< (neutral)\n= (adducted)',
                              4: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              5: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              6: 'f (friction surface)\nb (back surface)\nr (radial surface)\nu (ulnar surface)',
                              7: 't (tip)\nd (distal)\np (proximal)\nM (meta-carpal)',
                              #8 always null,
                              #9 always forward slash,
                              10: 'f (friction surface)\nb (back surface)\nr (radial surface)\nu (ulnar surface)',
                              11: 't (tip)\nd (distal)\nm (medial)\np (proximal)\nM (meta-carpal)',
                              12: '1 (if contact with index)\n- (if no contact)',
                              13: '2 (if contact with middle)\n- (if no contact)',
                              14: '3 (if contact with ring)\n- (if no contact)',
                              15: '4 (if contact with pinky)\n- (if no contact)',
                              #16 always 1,
                              17: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              18: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              19: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              20: ('{ (full abduction)\n< (neutral)\n= (adducted)\nx- (slightly crossed with contact)\n'
                                    'x (crossed with contact)\nx+ (ultracrossed)\n\u2327 (crossed without contact)'),
                              #21 always 2,
                              22: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              23: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              24: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              25: ('{ (full abduction)\n< (neutral)\n= (adducted)\nx- (slightly crossed with contact)\n'
                                    'x (crossed with contact)\nx+ (ultracrossed)\n\u2327 (crossed without contact)'),
                              #26 always 3,
                              27: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              28: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              29: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              30: ('{ (full abduction)\n< (neutral)\n= (adducted)\nx- (slightly crossed with contact)\n'
                                    'x (crossed with contact)\nx+ (ultracrossed)\n\u2327 (crossed without contact)'),
                              #31 always 4,
                              32: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              33: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)',
                              34: 'H (hyperextended)\nE (extended)\ni (intermediate)\nF (flexed)'
                              }

    @Slot(int)
    def transcriptionSlotChanged(self, e):
        if e == 1:
            self.fieldTypeInfo.setText('Forearm')
            self.fieldNumberInfo.setText('1')
        elif e < 6:
            self.fieldTypeInfo.setText('Thumb')
            self.fieldNumberInfo.setText('2')
        elif e < 16:
            self.fieldTypeInfo.setText('Thumb/finger contact')
            self.fieldNumberInfo.setText('3')
        elif e < 19:
            self.fieldTypeInfo.setText('Index finger')
            self.fieldNumberInfo.setText('4')
        elif e < 25:
            self.fieldTypeInfo.setText('Middle finger')
            self.fieldNumberInfo.setText('5')
        elif e < 30:
            self.fieldTypeInfo.setText('Ring finger')
            self.fieldNumberInfo.setText('6')
        else:
            self.fieldTypeInfo.setText('Pinky finger')
            self.fieldNumberInfo.setText('7')
        self.slotNumberInfo.setText(str(e))
        self.slotTypeInfo.setText(self.purposeDict[e])
        self.slotOptionsInfo.setText(self.optionsDict[e])