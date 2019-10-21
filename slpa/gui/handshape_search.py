from imports import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QButtonGroup,
                     QRadioButton, QApplication, QGridLayout, QTabWidget, QWidget, QPixmap, QScrollArea,
                     QSizePolicy, Qt, Slot, QListWidget, QListView, QListWidgetItem, QIcon, QImage, QPoint,
                     QStandardItemModel, QStandardItem, QSize, QLineEdit, QMenu, QAction, QMimeData, QDrag, QEvent)
from constants import GLOBAL_OPTIONS
import sys
import os
from gui.function_windows import FunctionDialog, FunctionWorker
from gui.helperwidgets import LogicRadioButtonGroup
from image import getMediaFilePath
import regex as re
from pprint import pprint


class ConfigHandList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.makeMenu()

        any = QListWidgetItem('any', self)
        any.setIcon(QIcon(os.path.join(os.path.join(os.path.dirname(os.getcwd()), 'media'), 'any.png')))

    def getSetOfItemLabels(self):
        labels = set()
        numItems = self.count()
        for i in range(numItems):
            label = self.item(i).text()
            labels.add(label)
        return labels

    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().hasImage():
            label = event.mimeData().text()
            if label in self.getSetOfItemLabels():
                event.ignore()
            else:
                event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().hasImage():
            label = event.mimeData().text()
            if label in self.getSetOfItemLabels():
                event.ignore()
            else:
                event.setDropAction(Qt.CopyAction)
                event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().hasImage():
            label = event.mimeData().text()
            if label in self.getSetOfItemLabels():
                event.ignore()
            else:
                if label == 'any' or label == 'empty':
                    while self.count() > 0:
                        item = self.takeItem(0)
                        del item
                else:
                    if 'any' in self.getSetOfItemLabels() or 'empty' in self.getSetOfItemLabels():
                        item = self.takeItem(0)
                        del item

                symbol = QListWidgetItem(label, self)
                img = event.mimeData().imageData()
                symbol.setIcon(QIcon(QPixmap(img)))

                event.setDropAction(Qt.CopyAction)
                event.accept()
        else:
            event.ignore()

    def showContextMenu(self, point):
        self.popMenu.exec_(self.mapToGlobal(point))

    def removeSelectedItem(self):
        selected = self.selectedItems()
        if not selected:
            return False
        for item in selected:
            self.takeItem(self.row(item))
            del item
        return True

    def makeMenu(self):
        self.popMenu = QMenu(self)
        self.removeAct = QAction('Remove', self, triggered=self.removeSelectedItem, checkable=False)
        self.popMenu.addAction(self.removeAct)


class ConfigHandPanel(QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        self.selectionList = ConfigHandList(parent=self)
        Layout = QVBoxLayout()
        Layout.addWidget(self.selectionList)
        self.setLayout(Layout)


class HandshapePanel(QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        self.handshapeList = HandshapeList(os.path.join(os.path.dirname(os.getcwd()), 'media'))
        unmarkedLayout = QVBoxLayout()
        unmarkedLayout.addWidget(self.handshapeList)
        self.setLayout(unmarkedLayout)

    def addHandshape(self, symbol):
        self.handshapeList.addHandshape(symbol)


class HandshapeList(QListWidget):
    def __init__(self, mediaPath, parent=None):
        super().__init__(parent)
        self.mediaPath = mediaPath
        self.setIconSize(QSize(100, 100))
        self.setViewMode(QListView.IconMode)
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setMinimumHeight(125)

    def addHandshape(self, symbol):
        item = QListWidgetItem(symbol, self)
        item.setIcon(QIcon(os.path.join(self.mediaPath, symbol + '.png')))

    def startDrag(self, e):
        selectedshape = self.selectedItems()[0]
        symbol = selectedshape.text()
        icon = selectedshape.icon().pixmap(100, 100)

        mime = QMimeData()
        mime.setImageData(QImage(os.path.join(self.mediaPath, symbol + '.png')))
        mime.setText(symbol)

        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.setPixmap(icon)
        drag.setHotSpot(QPoint(icon.width()/2, icon.height()/2))
        drag.exec_(Qt.CopyAction)


class HSWorker(FunctionWorker):
    def run(self):
        # TODO: implement this
        pass


class HandshapeSearchDialog(FunctionDialog):
    header = ['Corpus', 'Sign', 'Token frequency', 'Note']
    about = 'Handshape search'
    name = 'handshape search'
    mediaPath = os.path.join(os.path.dirname(os.getcwd()), 'media')

    def __init__(self, corpus, parent, settings, recent):
        super().__init__(parent, settings, HSWorker())

        self.corpus = corpus
        self.recent = recent

        # container widget for scroll
        container = QWidget()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        globalFrame = QGroupBox('Global options')
        globalLayout = QHBoxLayout()
        globalFrame.setLayout(globalLayout)

        self.forearmLogic = LogicRadioButtonGroup('vertical', 'e',
                                                  title='Forearm',
                                                  y='Yes', n='No', e='Either')

        self.estimateLogic = LogicRadioButtonGroup('vertical', 'e',
                                                   title='Estimated',
                                                   y='Yes', n='No', e='Either')

        self.uncertainLogic = LogicRadioButtonGroup('vertical', 'e',
                                                    title='Uncertain',
                                                    y='Yes', n='No', e='Either')

        self.incompleteLogic = LogicRadioButtonGroup('vertical', 'e',
                                                     title='Incomplete',
                                                     y='Yes', n='No', e='Either')
        globalLayout.addWidget(self.forearmLogic)
        globalLayout.addWidget(self.estimateLogic)
        globalLayout.addWidget(self.uncertainLogic)
        globalLayout.addWidget(self.incompleteLogic)

        self.configLogic = LogicRadioButtonGroup('vertical', 'e',
                                                 title='Configuration',
                                                 one='One-config signs', two='Two-config signs', e='Either')

        self.handLogic = LogicRadioButtonGroup('vertical', 'e',
                                               title='Hand',
                                               one='One-hand signs', two='Two-hand signs', e='Either')


        self.createConfigHand()
        self.createHandshapes()

        self.logicPanel = LogicRadioButtonGroup('vertical',
                                                'any',
                                                title='Signs should contain...',
                                                any='Any of the above configurations',
                                                all='All of the above configurations')

        self.notePanel = QLineEdit()
        self.notePanel.setPlaceholderText('Enter notes here...')

        mainLayout = QGridLayout()
        mainLayout.addWidget(globalFrame, 0, 0, 1, 2)
        mainLayout.addWidget(self.configLogic, 0, 2, 1, 1)
        mainLayout.addWidget(self.handLogic, 0, 3, 1, 1)
        mainLayout.addWidget(self.c1h1Group, 1, 0, 1, 1)
        mainLayout.addWidget(self.c1h2Group, 1, 1, 1, 1)
        mainLayout.addWidget(self.c2h1Group, 1, 2, 1, 1)
        mainLayout.addWidget(self.c2h2Group, 1, 3, 1, 1)
        mainLayout.addWidget(self.logicPanel, 2, 0, 1, 2)
        mainLayout.addWidget(self.otherGroup, 2, 2, 1, 2)
        mainLayout.addWidget(self.unmarkedGroup, 3, 0, 1, 4)
        mainLayout.addWidget(self.markedGroup, 4, 0, 1, 4)
        mainLayout.addWidget(self.notePanel, 5, 0, 1, 4)
        container.setLayout(mainLayout)

        #####This part should be removed later#####
        #self.testButton = QPushButton('test')
        #mainLayout.addWidget(self.testButton, 1, 0)
        #self.testButton.clicked.connect(self.test)
        #####This part should be removed later#####
        self.layout().insertWidget(0, scroll)
        #self.layout().insertLayout(0, mainLayout)

    #def test(self):
    #    res = self.generateKwargs()
    #    ret = extended_finger_search(self.corpus, res['c1h1'], res['c1h2'], res['c2h1'], res['c2h2'], res['logic'])
    #    pprint(ret)

    def createConfigHand(self):
        self.c1h1Group = ConfigHandPanel('Config1Hand1')
        self.c1h2Group = ConfigHandPanel('Config1Hand2')
        self.c2h1Group = ConfigHandPanel('Config2Hand1')
        self.c2h2Group = ConfigHandPanel('Config2Hand2')

    def createHandshapes(self):
        # unmarked handshapes
        self.unmarkedGroup = HandshapePanel('Unmarked handshapes')
        self.unmarkedGroup.addHandshape('A_O')
        self.unmarkedGroup.addHandshape('B_1')
        self.unmarkedGroup.addHandshape('w_B')
        self.unmarkedGroup.addHandshape('1_A')
        self.unmarkedGroup.addHandshape('6_S')
        self.unmarkedGroup.addHandshape('<_C')
        self.unmarkedGroup.addHandshape('>_5')

        # marked handshapes
        self.markedGroup = HandshapePanel('Marked handshapes')
        self.markedGroup.addHandshape('g')
        self.markedGroup.addHandshape('7')

        # other
        self.otherGroup = HandshapePanel('Others')
        self.otherGroup.addHandshape('any')
        self.otherGroup.addHandshape('empty')

    def generateKwargs(self):
        # TODO: implement this
        pass

    @Slot(object)
    def setResults(self, results):
        #TODO: need to modify token frequency when implemented (right not there is not frquency info)
        #TODO: double check thread method to properly place accept()
        self.results = list()
        for sign in results:
            self.results.append({'Corpus': self.corpus.name,
                                 'Sign': sign.gloss,
                                 'Token frequency': 1,
                                 'Note': self.notePanel.text()})
        self.accept()

app = QApplication(sys.argv)
main = HandshapeSearchDialog(None, None, None, None)
main.show()
sys.exit(app.exec_())