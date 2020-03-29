from imports import (QGroupBox, QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, Signal, QDialog, QListWidget,
                     QSize, QListView, QIcon, QListWidgetItem, Qt, QTabWidget, QWidget, QSizePolicy)
from image import getMediaFilePath
from analysis.unmarked_handshapes import (Handshape1, Handshape5, HandshapeA, HandshapeB1, HandshapeB2, HandshapeC,
                                          HandshapeO, HandshapeS)
from analysis.marked_handshapes import (Handshape3, HandshapeCIndex, HandshapeD, HandshapeG, HandshapeILY,
                                        HandshapeK, HandshapeL, HandshapeSick, HandshapeW, HandshapeY,
                                        HandshapeClawedF, HandshapeClawedL, HandshapeClawedV, HandshapeCombinedIPlusOne)


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


class HandshapePanel(QGroupBox):

    handshape_mapping = {
        '1': Handshape1,
        '3': Handshape3,
        '5': Handshape5,
        'A': HandshapeA,
        'B1': HandshapeB1,
        'B2': HandshapeB2,
        'C': HandshapeC,
        'C-index': HandshapeCIndex,
        'D': HandshapeD,
        'G': HandshapeG,
        'ILY': HandshapeILY,
        'K': HandshapeK,
        'L': HandshapeL,
        'O': HandshapeO,
        'S': HandshapeS,
        'sick': HandshapeSick,
        'W': HandshapeW,
        'Y': HandshapeY,
        'clawed-F': HandshapeClawedF,
        'clawed-L': HandshapeClawedL,
        'clawed-V': HandshapeClawedV,
        'combined-I+1': HandshapeCombinedIPlusOne
    }

    def __init__(self, title, parent=None):
        super().__init__(title, parent=parent)
        self.handshapeList = HandshapeList(parent=self)
        self.handshapeList.itemClicked.connect(self.fillSlots)
        layout = QVBoxLayout()
        layout.addWidget(self.handshapeList)
        self.setLayout(layout)

    def addHandshape(self, symbol):
        self.handshapeList.addHandshape(symbol)

    def sizeHint(self):
        return QSize(self.parent().parent().width(), super().sizeHint().height())

    def fillSlots(self, item):
        config1 = self.parent().parent().parent().configTabs.widget(0)
        config2 = self.parent().parent().parent().configTabs.widget(1)

        selected = self.parent().parent().parent().selected.checkedId()
        if selected == 1:
            transcription = config1.hand1Transcription
        elif selected == 2:
            transcription = config1.hand2Transcription
        elif selected == 3:
            transcription = config2.hand1Transcription
        elif selected == 4:
            transcription = config2.hand2Transcription

        for slot, symbol in zip(transcription.slots, HandshapePanel.handshape_mapping[item.text()].canonical):
            if slot.num == 1:
                slot.setChecked(False)
            else:
                slot.setText(symbol)


class HandshapeList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(50, 50))
        self.setViewMode(QListView.IconMode)

    def addHandshape(self, symbol):
        item = QListWidgetItem(symbol, self)
        item.setIcon(QIcon(getMediaFilePath(symbol + '.png')))

    def sizeHint(self):
        return QSize(self.parent().width(), super().sizeHint().height())


class PredefinedHandshapeDialog(QDialog):
    closeSignal = Signal(str)
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.resize(750, 250)
        self.setWindowTitle('Predefined handshapes')
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window | Qt.WindowTitleHint |
                            Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        languageTab = QTabWidget()
        mainLayout.addWidget(languageTab)

        ASLHandshapeInventory = HandshapeInventory(parent=self)
        ASLHandshapeInventory.addUnmarkedHandshape('1')
        ASLHandshapeInventory.addUnmarkedHandshape('5')
        ASLHandshapeInventory.addUnmarkedHandshape('A')
        ASLHandshapeInventory.addUnmarkedHandshape('B1')
        ASLHandshapeInventory.addUnmarkedHandshape('B2')
        ASLHandshapeInventory.addUnmarkedHandshape('C')
        ASLHandshapeInventory.addUnmarkedHandshape('O')
        ASLHandshapeInventory.addUnmarkedHandshape('S')

        ASLHandshapeInventory.addMarkedHandshape('3')
        ASLHandshapeInventory.addMarkedHandshape('C-index')
        ASLHandshapeInventory.addMarkedHandshape('D')
        ASLHandshapeInventory.addMarkedHandshape('G')
        ASLHandshapeInventory.addMarkedHandshape('ILY')
        ASLHandshapeInventory.addMarkedHandshape('K')
        ASLHandshapeInventory.addMarkedHandshape('L')
        ASLHandshapeInventory.addMarkedHandshape('sick')
        ASLHandshapeInventory.addMarkedHandshape('W')
        ASLHandshapeInventory.addMarkedHandshape('Y')
        ASLHandshapeInventory.addMarkedHandshape('clawed-F')
        ASLHandshapeInventory.addMarkedHandshape('clawed-L')
        ASLHandshapeInventory.addMarkedHandshape('clawed-V')
        ASLHandshapeInventory.addMarkedHandshape('combined-I+1')

        languageTab.addTab(ASLHandshapeInventory, 'ASL')

        KSLHandshapeInventory = HandshapeInventory(parent=self)
        KSLHandshapeInventory.addUnmarkedHandshape('1')

        languageTab.addTab(KSLHandshapeInventory, 'KSL')

    def closeEvent(self, QCloseEvent):
        self.closeSignal.emit('closed')
        super().closeEvent(QCloseEvent)

        #unmarkedhandshape = HandshapePanel('Unmarked handshapes', parent=self)
        #unmarkedhandshape.addHandshape('1')
        #unmarkedhandshape.addHandshape('5')
        #unmarkedhandshape.addHandshape('A')
        #unmarkedhandshape.addHandshape('B1')
        #unmarkedhandshape.addHandshape('B2')
        #unmarkedhandshape.addHandshape('C')
        #unmarkedhandshape.addHandshape('O')
        #unmarkedhandshape.addHandshape('S')
        #mainLayout.addWidget(unmarkedhandshape)

        #markedhandshape = HandshapePanel('Marked handshapes', parent=self)
        #markedhandshape.addHandshape('g')
        #mainLayout.addWidget(markedhandshape)


class HandshapeInventory(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parentW = parent

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.unmarkedhandshape = HandshapePanel('Unmarked handshapes', parent=self)
        self.markedhandshape = HandshapePanel('Marked handshapes', parent=self)

        layout.addWidget(self.unmarkedhandshape)
        layout.addWidget(self.markedhandshape)

    def addUnmarkedHandshape(self, label):
        self.unmarkedhandshape.addHandshape(label)

    def addMarkedHandshape(self, label):
        self.markedhandshape.addHandshape(label)

    def parent(self):
        return self.parentW
