from imports import (QGroupBox, QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, Signal, QDialog, QListWidget,
                     QSize, QListView, QIcon, QListWidgetItem, Qt, QTabWidget, QWidget, QSizePolicy, QAbstractTableModel,
                     QTableView, QAbstractItemView, QColor)
from image import getMediaFilePath
from analysis.unmarked_handshapes import (Handshape1, Handshape5, HandshapeA, HandshapeB1, HandshapeB2, HandshapeC,
                                          HandshapeO, HandshapeS, HandshapeEmpty)
from analysis.marked_handshapes import (HandshapeExtendedU, HandshapeCIndex, HandshapeD, HandshapeG, HandshapeCombinedILY,
                                        HandshapeK, HandshapeL, HandshapeExtended8, HandshapeW, HandshapeY,
                                        HandshapeClawedF, HandshapeClawedL, HandshapeClawedV, HandshapeCombinedIPlusOne, HandshapeI,
                                        HandshapeF, HandshapeClosedW, HandshapeClawedW, HandshapeClawedSpreadC, HandshapeBentI,
                                        HandshapeBentThumbL, HandshapeBentV, HandshapeClawedExtendedV, HandshapeDoubleCIndex, HandshapeFlatC,
                                        HandshapeMiddleFinger, HandshapeOIndex, HandshapeOpenF, Handshape8, HandshapeClawedI,
                                        HandshapeDoubleModifiedG, HandshapeCovered8, HandshapeSlantedB, HandshapeX,
                                        HandshapeExtendedC, HandshapeClosedModifiedG, HandshapeFlatCombinedIPlusOne, Handshape3,
                                        HandshapeExtendedB, Handshape4, HandshapeClosedDoubleModifiedG, HandshapeOpen8,
                                        HandshapeU, HandshapeClawed3, HandshapeExtendedA, HandshapeR, HandshapeV,
                                        HandshapeClosedAIndex, HandshapeModifiedF, HandshapeBentExtendedB, HandshapeClawedC,
                                        HandshapeCoveredF, HandshapeN, HandshapeT, HandshapeContractedUIndex, HandshapeCurvedW,
                                        HandshapeSpreadExtendedC, HandshapeClawedExtendedB, HandshapeCombinedYAndMiddle,
                                        HandshapeContractedC, HandshapeE, HandshapeOpenE, HandshapeM, HandshapeBent1,
                                        HandshapeContracted5, HandshapeCrookedF)


class MyTableModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.colLabels = ['Handshape',
                          'Bent',
                          'Clawed', 'Closed', 'Combined', 'Contracted', 'Covered', 'Crooked', 'Curved',
                          'Extended',
                          'Flat',
                          'Index',
                          'Modified',
                          'Offset', 'Open',
                          'Slanted', 'Spread']

        self.dataCached = [
            ['A',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             'extended-A',  # extended
             '',  # flat
             'A-index',  # index
             '',  # modified
             '', 'open-A',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             'closed-A-index',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['B1',
             'bent-B',  # bent
             'clawed-extended-B', '', '', 'contracted-B', '', 'crooked-extended-B', '',  # 7 slots
             'extended-B',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             'slanted-B', ''],  # slanted, spread
            ['B2',
             'bent-extended-B',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['C',
             '',  # bent
             'clawed-C', '', '', 'contracted-C', '', 'crooked-C', '',  # 7 slots
             'extended-C',  # extended
             'flat-C',  # flat
             'C-index',  # index
             '',  # modified
             '', '',  # offset, open
             '', 'spread-C'],  # slanted, spread
            ['',
             '',  # bent
             'clawed-spread-C', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             'double-C-index',  # index
             '',  # modified
             '', '',  # offset, open
             '', 'spread-extended-C'],  # slanted, spread
            ['D',
             'bent-D',  # bent
             '', 'closed-bent-D', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['E',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', 'open-E',  # offset, open
             '', ''],  # slanted, spread
            ['F',
             '',  # bent
             'clawed-F', '', '', '', 'covered-F', 'crooked-F', '',  # 7 slots
             '',  # extended
             'flat-F',  # flat
             '',  # index
             'modified-F',  # modified
             'offset-F', 'open-F',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             'flat-open-F',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             'flat-clawed-F',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['G',
             '',  # bent
             '', 'closed-modified-G', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'modified-G',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', 'closed-double-modified-G', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'double-modified-G',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['I',
             'bent-I',  # bent
             'clawed-I', '', 'combined-I+1', '', '', '', '',  # 7 slots
             '',  # extended
             'flat-combined-I+1',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             'bent-combined-I+1',  # bent
             '', '', 'combined-ILY', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['K',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             'extended-K',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['L',
             'bent-L',  # bent
             'clawed-L', '', '', 'contracted-L', '', 'crooked-L', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             'bent-thumb-L',  # bent
             '', '', '', 'double-contracted-L', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['M',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             'flat-M',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['N',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['O',
             '',  # bent
             '', '', '', '', 'covered-O', '', '',  # 7 slots
             '',  # extended
             'flat-O',  # flat
             'O-index',  # index
             'modified-O',  # modified
             'offset-O', 'open-spread-O',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', 'open-O-index',  # offset, open
             '', ''],  # slanted, spread
            ['R',
             'bent-R',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             'extended-R',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['S',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['T',
             '',  # bent
             '', '', '', '', 'covered-T', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['U',
             'bent-U',  # bent
             'clawed-U', '', 'combined-U&Y', 'contracted-U', '', 'crooked-U', '',  # 7 slots
             'extended-U',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             'bent-extended-U',  # bent
             '', '', '', 'contracted-U-index', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['V',
             'bent-V',  # bent
             'clawed-V', 'closed-V', '', '', '', 'crooked-V', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             'slanted-V', ''],  # slanted, spread
            ['',
             'bent-extended-V',  # bent
             'clawed-extended-V', '', '', '', '', 'crooked-extended-V', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['W',
             '',  # bent
             'clawed-W', 'closed-W', '', '', '', '', 'curved-W',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['X',
             '',  # bent
             'closed-X', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['Y',
             '',  # bent
             '', '', 'combined-Y&middle', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'modified-Y',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['1',
             'bent-1',  # bent
             '', '', '', '', '', 'crooked-1', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['3',
             '',  # bent
             'clawed-3', '', '', 'contracted-3', '', '', '',  # 7 slots
             '',  # extended
             'flat-open-F',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['4',
             'bent-4',  # bent
             'clawed-4', '', '', '', '', 'crooked-4', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             'slanted-4', ''],  # slanted, spread
            ['5',
             'bent-5',  # bent
             'clawed-5', '', '', 'contracted-5', '', 'crooked-5', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'modified-5',  # modified
             '', '',  # offset, open
             'slanted-5', ''],  # slanted, spread
            ['',
             'bent-midfinger-5',  # bent
             '', '', '', 'relaxed-contracted-5', '', 'crooked-slanted-5', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['8',
             '',  # bent
             '', '', '', '', 'covered-8', '', '',  # 7 slots
             'extended-8',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', 'open-8',  # offset, open
             '', ''],  # slanted, spread
            ['middle-finger',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
        ]

    def rowCount(self, parent):
        return len(self.dataCached)

    def columnCount(self, parent):
        return len(self.colLabels)

    def get_value(self, index):
        i = index.row()
        j = index.column()
        return self.dataCached[i][j]

    def data(self, index, role=None):
        if not index.isValid():
            return None
        value = self.get_value(index)
        if role == Qt.DisplayRole:# or role == Qt.EditRole:
            return value
        #elif role == Qt.TextAlignmentRole:
        #    return Qt.AlignCenter
        elif role == Qt.DecorationRole:
            return QIcon(getMediaFilePath(value + '.png'))
        elif role == Qt.BackgroundRole:
            if value in {'1', '5', 'A', 'B1', 'B2', 'C', 'O', 'S'}:
                return QColor('#90ee90')
        return None

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            self.dataCached[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.colLabels[section]
            return header
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)

        return None


class FreezeTableWidget(QTableView):
    def __init__(self, parent=None, *args):
        QTableView.__init__(self, parent, *args)

        #self.setMinimumSize(800, 600)
        self.setIconSize(QSize(50, 50))

        # set the table model
        tm = MyTableModel(self)

        # set the proxy model
        pm = tm
        #pm = QSortFilterProxyModel(self)
        #pm.setSourceModel(tm)

        self.setModel(pm)

        self.frozenTableView = QTableView(self)
        self.frozenTableView.setIconSize(QSize(50, 50))
        self.frozenTableView.setModel(pm)
        self.frozenTableView.verticalHeader().hide()
        #self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        # self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        #self.frozenTableView.setStyleSheet('''border: none; background-color: #CCC''')
        self.frozenTableView.setSelectionModel(QAbstractItemView.selectionModel(self))

        # so there are no scroll bars in the frozen panel
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.viewport().stackUnder(self.frozenTableView)

        #self.setEditTriggers(QAbstractItemView.SelectedClicked)

        # hide grid
        self.setShowGrid(False)

        #self.setStyleSheet('font: 10pt "Courier New"')
        self.setStyleSheet('font: 10pt')

        hh = self.horizontalHeader()
        hh.setDefaultAlignment(Qt.AlignCenter)
        hh.setStretchLastSection(True)

        ncol = tm.columnCount(self)
        for col in range(ncol):
            if col == 0:
                self.horizontalHeader().resizeSection(col, 100)
                # self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
                self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
            #elif col == 1:
            #    self.horizontalHeader().resizeSection(col, 150)
                # self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
            #    self.frozenTableView.setColumnWidth(col, self.columnWidth(col))
            else:
                self.horizontalHeader().resizeSection(col, 125)
                self.frozenTableView.setColumnHidden(col, True)

        #self.frozenTableView.setSortingEnabled(True)
        #self.frozenTableView.sortByColumn(0, Qt.AscendingOrder)

        self.setAlternatingRowColors(True)

        vh = self.verticalHeader()
        vh.setDefaultSectionSize(25)
        vh.setDefaultAlignment(Qt.AlignCenter)
        vh.setVisible(True)
        self.frozenTableView.verticalHeader().setDefaultSectionSize(vh.defaultSectionSize())

        # nrows = tm.rowCount(self)
        # for row in range(nrows):
        #     self.setRowHeight(row, 25)

        self.frozenTableView.show()
        self.updateFrozenTableGeometry()

        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # connect the headers and scrollbars of both tableviews together
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

        self.resizeRowsToContents()

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex == 0: #or logicalIndex == 1:
            self.frozenTableView.setColumnWidth(logicalIndex, newSize)
            self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        QTableView.resizeEvent(self, event)
        self.updateFrozenTableGeometry()

    def scrollTo(self, index, hint):
        if index.column() > 1:
            QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                             self.frameWidth(),
                                             self.columnWidth(0), #+ self.columnWidth(1),
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableView.setGeometry(self.frameWidth(),
                                             self.frameWidth(),
                                             self.columnWidth(0), # + self.columnWidth(1),
                                             self.viewport().height() + self.horizontalHeader().height())

    def moveCursor(self, cursorAction, modifiers):
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        x = self.visualRect(current).topLeft().x()
        frozen_width = self.frozenTableView.columnWidth(0) + self.frozenTableView.columnWidth(1)
        if cursorAction == self.MoveLeft and current.column() > 1 and x < frozen_width:
            new_value = self.horizontalScrollBar().value() + x - frozen_width
            self.horizontalScrollBar().setValue(new_value)
        return current


class LogicRadioButtonGroup(QGroupBox):
    chosen = Signal(str)

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
            button.clicked.connect(self.selected)
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

    def selected(self):
        self.chosen.emit(self.buttonGroup.checkedButton().text())


class PredefinedHandshapeDialog(QDialog):
    closeSignal = Signal(str)
    handshape_mapping = {
        '': HandshapeEmpty,
        '1': Handshape1,
        'extended-U': HandshapeExtendedU,
        '5': Handshape5,
        'A': HandshapeA,
        'B1': HandshapeB1,
        'B2': HandshapeB2,
        'C': HandshapeC,
        'C-index': HandshapeCIndex,
        'D': HandshapeD,
        'G': HandshapeG,
        'combined-ILY': HandshapeCombinedILY,
        'K': HandshapeK,
        'L': HandshapeL,
        'O': HandshapeO,
        'S': HandshapeS,
        'extended-8': HandshapeExtended8,
        'W': HandshapeW,
        'Y': HandshapeY,
        'clawed-F': HandshapeClawedF,
        'clawed-L': HandshapeClawedL,
        'clawed-V': HandshapeClawedV,
        'combined-I+1': HandshapeCombinedIPlusOne,
        'I': HandshapeI,
        'F': HandshapeF,
        'closed-W': HandshapeClosedW,
        'clawed-W': HandshapeClawedW,
        'clawed-spread-C': HandshapeClawedSpreadC,
        'bent-I': HandshapeBentI,
        'bent-thumb-L': HandshapeBentThumbL,
        'bent-V': HandshapeBentV,
        'clawed-extended-V': HandshapeClawedExtendedV,
        'double-C-index': HandshapeDoubleCIndex,
        'flat-C': HandshapeFlatC,
        'middle-finger': HandshapeMiddleFinger,
        'O-index': HandshapeOIndex,
        'open-F': HandshapeOpenF,
        '8': Handshape8,
        'clawed-I': HandshapeClawedI,
        'double-modified-G': HandshapeDoubleModifiedG,
        'covered-8': HandshapeCovered8,
        'slanted-B': HandshapeSlantedB,
        'X': HandshapeX,
        'extended-C': HandshapeExtendedC,
        'closed-modified-G': HandshapeClosedModifiedG,
        'flat-combined-I+1': HandshapeFlatCombinedIPlusOne,
        '3': Handshape3,
        'extended-B': HandshapeExtendedB,
        '4': Handshape4,
        'closed-double-modified-G': HandshapeClosedDoubleModifiedG,
        'open-8': HandshapeOpen8,
        'U': HandshapeU,
        'clawed-3': HandshapeClawed3,
        'extended-A': HandshapeExtendedA,
        'R': HandshapeR,
        'V': HandshapeV,
        'closed-A-index': HandshapeClosedAIndex,
        'modified-F': HandshapeModifiedF,
        'bent-extended-B': HandshapeBentExtendedB,
        'clawed-C': HandshapeClawedC,
        'covered-F': HandshapeCoveredF,
        'N': HandshapeN,
        'T': HandshapeT,
        'contracted-U-index': HandshapeContractedUIndex,
        'curved-W': HandshapeCurvedW,
        'spread-extended-C': HandshapeSpreadExtendedC,
        'clawed-extended-B': HandshapeClawedExtendedB,
        'combined-Y&middle': HandshapeCombinedYAndMiddle,
        'contracted-C': HandshapeContractedC,
        'E': HandshapeE,
        'open-E': HandshapeOpenE,
        'M': HandshapeM,
        'bent-1': HandshapeBent1,
        'contracted-5': HandshapeContracted5,
        'crooked-F': HandshapeCrookedF
    }

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.resize(750, 750)
        self.setWindowTitle('Predefined handshapes')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window | Qt.WindowTitleHint |
                            Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        # create table
        table = FreezeTableWidget(self)
        table.clicked.connect(self.fillSlots)
        table.frozenTableView.clicked.connect(self.fillSlots)
        #table.itemClicked.connect(self.fillSlots)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)

    def closeEvent(self, QCloseEvent):
        self.closeSignal.emit('closed')
        super().closeEvent(QCloseEvent)

    def fillSlots(self, clicked):
        config1 = self.parent().configTabs.widget(0)
        config2 = self.parent().configTabs.widget(1)
        selected = self.parent().selected.checkedId()

        if selected == 1:
            transcription = config1.hand1Transcription
        elif selected == 2:
            transcription = config1.hand2Transcription
        elif selected == 3:
            transcription = config2.hand1Transcription
        elif selected == 4:
            transcription = config2.hand2Transcription

        for slot, symbol in zip(transcription.slots, PredefinedHandshapeDialog.handshape_mapping.get(clicked.data(), HandshapeEmpty).canonical):
            if slot.num == 1:
                slot.setChecked(False)
            else:
                slot.setText(symbol)
