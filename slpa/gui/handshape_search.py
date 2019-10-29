from imports import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QButtonGroup,
                     QRadioButton, QApplication, QGridLayout, QTabWidget, QWidget, QPixmap, QScrollArea,
                     QSizePolicy, Qt, Slot, QListWidget, QListView, QListWidgetItem, QIcon, QImage, QPoint,
                     QStandardItemModel, QStandardItem, QSize, QLineEdit, QMenu, QAction, QMimeData, QDrag, QEvent)
from constants import GLOBAL_OPTIONS
from gui.function_windows import FunctionDialog, FunctionWorker
from gui.helperwidgets import LogicRadioButtonGroup
from analysis.handshape_search import handshape_search
import sys
from pprint import pprint
from image import getMediaFilePath


class ConfigHandList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEnabled(True)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.makeMenu()
        self.setToSpecified('any')

    def setToSpecified(self, specified):
        while self.count() > 0:
            item = self.takeItem(0)
            del item

        spec = QListWidgetItem(specified, self)
        spec.setIcon(QIcon(getMediaFilePath(specified + '.png')))

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

        if self.count() == 0:
            self.setToSpecified('any')
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

    def value(self):
        labels = set()
        numItems = self.selectionList.count()
        for i in range(numItems):
            label = self.selectionList.item(i).text()
            labels.add(label)
        return labels


class HandshapePanel(QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        self.handshapeList = HandshapeList(parent=self)
        unmarkedLayout = QVBoxLayout()
        unmarkedLayout.addWidget(self.handshapeList)
        self.setLayout(unmarkedLayout)

    def addHandshape(self, symbol):
        self.handshapeList.addHandshape(symbol)


class HandshapeList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(100, 100))
        self.setViewMode(QListView.IconMode)
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setMinimumHeight(125)

    def addHandshape(self, symbol):
        item = QListWidgetItem(symbol, self)
        item.setIcon(QIcon(getMediaFilePath(symbol + '.png')))

    def startDrag(self, e):
        selectedshape = self.selectedItems()[0]
        symbol = selectedshape.text()
        icon = selectedshape.icon().pixmap(100, 100)

        mime = QMimeData()
        mime.setImageData(QImage(getMediaFilePath(symbol + '.png')))
        mime.setText(symbol)

        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.setPixmap(icon)
        drag.setHotSpot(QPoint(icon.width()/2, icon.height()/2))
        drag.exec_(Qt.CopyAction)


class HSWorker(FunctionWorker):
    def run(self):
        corpus = self.kwargs.pop('corpus')
        forearm = self.kwargs.pop('forearm')
        estimated = self.kwargs.pop('estimated')
        uncertain = self.kwargs.pop('uncertain')
        incomplete = self.kwargs.pop('incomplete')
        configuration = self.kwargs.pop('configuration')
        hand = self.kwargs.pop('hand')
        logic = self.kwargs.pop('logic')
        c1h1 = self.kwargs.pop('config1hand1')
        c1h2 = self.kwargs.pop('config1hand2')
        c2h1 = self.kwargs.pop('config2hand1')
        c2h2 = self.kwargs.pop('config2hand2')

        results = handshape_search(corpus, forearm, estimated, uncertain, incomplete, configuration, hand, logic, c1h1, c1h2, c2h1, c2h2)
        self.dataReady.emit(results)


class HandshapeSearchDialog(FunctionDialog):
    header = ['Corpus', 'Sign', 'Token frequency', 'Note']
    about = 'Handshape search'
    name = 'handshape search'

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
        self.configLogic.chosen.connect(self.handleConfigChange)

        self.handLogic = LogicRadioButtonGroup('vertical', 'e',
                                               title='Hand',
                                               one='One-hand signs', two='Two-hand signs', e='Either')
        self.handLogic.chosen.connect(self.handleHandChange)


        self.createConfigHand()
        self.createHandshapes()

        self.logicPanel = LogicRadioButtonGroup('vertical',
                                                'all',
                                                title='Signs should contain...',
                                                all='All of the above configurations',
                                                any='Any of the above configurations')

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
        #mainLayout.addWidget(self.testButton, 6, 0, 1, 1)
        #self.testButton.clicked.connect(self.test)
        #####This part should be removed later#####
        self.layout().insertWidget(0, scroll)

    def handleConfigChange(self, option):
        if option == 'One-config signs':
            self.c2h1Group.selectionList.setToSpecified('empty')
            self.c2h2Group.selectionList.setToSpecified('empty')
            #self.c2h1Group.selectionList.setEnabled(False)
            #self.c2h2Group.selectionList.setEnabled(False)
            self.c2h1Group.setEnabled(False)
            self.c2h2Group.setEnabled(False)
        else:
            if self.handLogic.value() == 'One-hand signs':
                #self.c2h1Group.selectionList.setEnabled(True)
                self.c2h1Group.setEnabled(True)
            else:
                #self.c2h1Group.selectionList.setEnabled(True)
                #self.c2h2Group.selectionList.setEnabled(True)
                self.c2h1Group.setEnabled(True)
                self.c2h2Group.setEnabled(True)


    def handleHandChange(self, option):
        if option == 'One-hand signs':
            self.c1h2Group.selectionList.setToSpecified('empty')
            self.c2h2Group.selectionList.setToSpecified('empty')
            #self.c1h2Group.selectionList.setEnabled(False)
            #self.c2h2Group.selectionList.setEnabled(False)
            self.c1h2Group.setEnabled(False)
            self.c2h2Group.setEnabled(False)
        else:
            if self.configLogic.value() == 'One-config signs':
                #self.c1h2Group.selectionList.setEnabled(True)
                self.c1h2Group.setEnabled(True)
            else:
                #self.c1h2Group.selectionList.setEnabled(True)
                #self.c2h2Group.selectionList.setEnabled(True)
                self.c1h2Group.setEnabled(True)
                self.c2h2Group.setEnabled(True)

    #def test(self):
    #    res = self.generateKwargs()
    #    ret = extended_finger_search(self.corpus, res['c1h1'], res['c1h2'], res['c2h1'], res['c2h2'], res['logic'])
    #    pprint(res)

    def createConfigHand(self):
        self.c1h1Group = ConfigHandPanel('Config1Hand1')
        self.c1h2Group = ConfigHandPanel('Config1Hand2')
        self.c2h1Group = ConfigHandPanel('Config2Hand1')
        self.c2h2Group = ConfigHandPanel('Config2Hand2')

    def createHandshapes(self):
        # unmarked handshapes
        self.unmarkedGroup = HandshapePanel('Unmarked handshapes')
        self.unmarkedGroup.addHandshape('O')
        self.unmarkedGroup.addHandshape('1')
        self.unmarkedGroup.addHandshape('B1')
        self.unmarkedGroup.addHandshape('A')
        self.unmarkedGroup.addHandshape('S')
        self.unmarkedGroup.addHandshape('C')
        self.unmarkedGroup.addHandshape('5')
        self.unmarkedGroup.addHandshape('B2')

        # marked handshapes
        self.markedGroup = HandshapePanel('Marked handshapes')
        self.markedGroup.addHandshape('g')
        self.markedGroup.addHandshape('7')

        # other
        self.otherGroup = HandshapePanel('Others')
        self.otherGroup.addHandshape('any')
        self.otherGroup.addHandshape('empty')

    def generateKwargs(self):
        kwargs = dict()

        kwargs['corpus'] = self.corpus
        kwargs['forearm'] = self.forearmLogic.value()
        kwargs['estimated'] = self.estimateLogic.value()
        kwargs['uncertain'] = self.uncertainLogic.value()
        kwargs['incomplete'] = self.incompleteLogic.value()
        kwargs['configuration'] = self.configLogic.value()
        kwargs['hand'] = self.handLogic.value()
        kwargs['logic'] = self.logicPanel.value()
        kwargs['config1hand1'] = self.c1h1Group.value()
        kwargs['config1hand2'] = self.c1h2Group.value()
        kwargs['config2hand1'] = self.c2h1Group.value()
        kwargs['config2hand2'] = self.c2h2Group.value()
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
                                 'Token frequency': 1,
                                 'Note': self.notePanel.text()})
        self.accept()

#app = QApplication(sys.argv)
#main = HandshapeSearchDialog(None, None, None, None)
#main.show()
#sys.exit(app.exec_())