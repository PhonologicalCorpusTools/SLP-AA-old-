from imports import (QGroupBox, QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, Signal, QDialog, QListWidget,
                     QSize, QListView, QIcon, QListWidgetItem, Qt)
from image import getMediaFilePath
from analysis.unmarked_handshapes import Handshape5


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
        '1': Handshape5,
        '5': Handshape5,
        'g': Handshape5
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

    def fillSlots(self, item):
        config1 = self.parent().parent().configTabs.widget(0)
        config2 = self.parent().parent().configTabs.widget(1)

        selected = self.parent().parent().selected.checkedId()
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
        self.setIconSize(QSize(100, 100))
        self.setViewMode(QListView.IconMode)
        self.setMinimumHeight(125)

    def addHandshape(self, symbol):
        item = QListWidgetItem(symbol, self)
        item.setIcon(QIcon(getMediaFilePath(symbol + '.png')))


class PredefinedHandshapeDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint |
                            Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        unmarkedhandshape = HandshapePanel('Unmarked handshapes', parent=self)
        unmarkedhandshape.addHandshape('1')
        unmarkedhandshape.addHandshape('5')
        mainLayout.addWidget(unmarkedhandshape)

        markedhandshape = HandshapePanel('Marked handshapes', parent=self)
        markedhandshape.addHandshape('g')
        mainLayout.addWidget(markedhandshape)
