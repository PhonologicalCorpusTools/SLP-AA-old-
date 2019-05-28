from imports import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QButtonGroup,
                     QRadioButton, QApplication, QGridLayout, QTabWidget, QWidget,
                     QSizePolicy, Qt, Slot, QListWidget, QListView, QListWidgetItem, QIcon,
                     QStandardItemModel, QStandardItem, QSize, QLineEdit)
from constants import GLOBAL_OPTIONS
import sys
import os
from gui.function_windows import FunctionDialog, FunctionWorker
from gui.phonological_search import LogicRadioButtonGroup
from image import getMediaFilePath
import regex as re
from pprint import pprint


class HSWorker(FunctionWorker):
    def run(self):
        # TODO: implement this
        pass


class HandshapeSearchDialog(FunctionDialog):
    header = ['Corpus', 'Sign', 'Token frequency']
    about = 'Handshape search'
    name = 'handshape search'
    mediaPath = os.path.join(os.path.dirname(os.getcwd()), 'media')

    def __init__(self, corpus, parent, settings, recent):
        super().__init__(parent, settings, HSWorker())

        self.corpus = corpus
        self.recent = recent

        # TODO: implement remove action
        self.c1h1Group = QGroupBox('Config1Hand1')
        self.c1h1List = QListWidget()
        self.c1h1List.setAcceptDrops(True)
        self.c1h1List.setDragEnabled(True)
        #self.c1h1List.supportedDropActions()
        c1h1Layout = QVBoxLayout()
        c1h1Layout.addWidget(self.c1h1List)
        self.c1h1Group.setLayout(c1h1Layout)

        self.c1h2Group = QGroupBox('Config1Hand2')
        self.c1h2List = QListWidget()
        self.c1h2List.setAcceptDrops(True)
        self.c1h2List.setDragEnabled(True)
        c1h2Layout = QVBoxLayout()
        c1h2Layout.addWidget(self.c1h2List)
        self.c1h2Group.setLayout(c1h2Layout)

        self.c2h1Group = QGroupBox('Config2Hand1')
        self.c2h1List = QListWidget()
        self.c2h1List.setAcceptDrops(True)
        self.c2h1List.setDragEnabled(True)
        c2h1Layout = QVBoxLayout()
        c2h1Layout.addWidget(self.c2h1List)
        self.c2h1Group.setLayout(c2h1Layout)

        self.c2h2Group = QGroupBox('Config2Hand2')
        self.c2h2List = QListWidget()
        self.c2h2List.setAcceptDrops(True)
        self.c2h2List.setDragEnabled(True)
        c2h2Layout = QVBoxLayout()
        c2h2Layout.addWidget(self.c2h2List)
        self.c2h2Group.setLayout(c2h2Layout)

        self.otherGroup = QGroupBox('Others')
        self.otherList = QListWidget(self)
        self.otherList.setIconSize(QSize(50, 50))
        #self.otherList.setUniformItemSizes(True)
        self.otherList.setViewMode(QListView.IconMode)
        self.otherList.setDragEnabled(True)
        self.otherList.setAcceptDrops(False)

        everything = QListWidgetItem('all', self.otherList)
        everything.setIcon(QIcon(os.path.join(self.mediaPath, 'all.png')))

        empty = QListWidgetItem('empty', self.otherList)
        empty.setIcon(QIcon(os.path.join(self.mediaPath, 'empty.png')))

        otherLayout = QVBoxLayout()
        otherLayout.addWidget(self.otherList)
        self.otherGroup.setLayout(otherLayout)

        self.unmarkedGroup = QGroupBox('Unmarked handshapes')
        self.unmarkedList = QListWidget(self)
        self.unmarkedList.setIconSize(QSize(100, 100))
        self.unmarkedList.setViewMode(QListView.IconMode)
        self.unmarkedList.setDragEnabled(True)
        self.unmarkedList.setAcceptDrops(False)
        self.unmarkedList.setMinimumHeight(125)

        A = QListWidgetItem('A', self.unmarkedList)
        A.setIcon(QIcon(os.path.join(self.mediaPath, 'A.png')))

        B = QListWidgetItem('B', self.unmarkedList)
        B.setIcon(QIcon(os.path.join(self.mediaPath, 'B.png')))

        w = QListWidgetItem('w', self.unmarkedList)
        w.setIcon(QIcon(os.path.join(self.mediaPath, 'w.png')))

        one = QListWidgetItem('1', self.unmarkedList)
        one.setIcon(QIcon(os.path.join(self.mediaPath, '1.png')))

        six = QListWidgetItem('6', self.unmarkedList)
        six.setIcon(QIcon(os.path.join(self.mediaPath, '6.png')))

        less = QListWidgetItem('<', self.unmarkedList)
        less.setIcon(QIcon(os.path.join(self.mediaPath, '<.png')))

        more = QListWidgetItem('>', self.unmarkedList)
        more.setIcon(QIcon(os.path.join(self.mediaPath, '>.png')))

        unmarkedLayout = QVBoxLayout()
        unmarkedLayout.addWidget(self.unmarkedList)
        self.unmarkedGroup.setLayout(unmarkedLayout)

        self.markedGroup = QGroupBox('Marked handshapes')
        self.markedList = QListWidget()
        self.markedList.setIconSize(QSize(100, 100))
        self.markedList.setViewMode(QListView.IconMode)
        self.markedList.setDragEnabled(True)
        self.markedList.setAcceptDrops(False)
        self.markedList.setMinimumHeight(125)

        g = QListWidgetItem('g', self.markedList)
        g.setIcon(QIcon(os.path.join(self.mediaPath, 'g.png')))

        seven = QListWidgetItem('7', self.markedList)
        seven.setIcon(QIcon(os.path.join(self.mediaPath, '7.png')))

        markedLayout = QVBoxLayout()
        markedLayout.addWidget(self.markedList)
        self.markedGroup.setLayout(markedLayout)

        self.logicPanel = LogicRadioButtonGroup('vertical',
                                           'any',
                                           title='Signs should contain...',
                                           any='Any of the above configurations',
                                           all='All of the above configurations')
        self.notePanel = QLineEdit()
        self.notePanel.setPlaceholderText('Enter notes here...')

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.c1h1Group, 0, 0, 1, 1)
        mainLayout.addWidget(self.c1h2Group, 0, 1, 1, 1)
        mainLayout.addWidget(self.c2h1Group, 0, 2, 1, 1)
        mainLayout.addWidget(self.c2h2Group, 0, 3, 1, 1)
        mainLayout.addWidget(self.logicPanel, 1, 0, 1, 2)
        mainLayout.addWidget(self.otherGroup, 1, 2, 1, 2)
        mainLayout.addWidget(self.unmarkedGroup, 2, 0, 1, 4)
        mainLayout.addWidget(self.markedGroup, 3, 0, 1, 4)
        mainLayout.addWidget(self.notePanel, 4, 0, 1, 4)

        #####This part should be removed later#####
        #self.testButton = QPushButton('test')
        #mainLayout.addWidget(self.testButton, 1, 0)
        #self.testButton.clicked.connect(self.test)
        #####This part should be removed later#####

        self.layout().insertLayout(0, mainLayout)

    #def test(self):
    #    res = self.generateKwargs()
    #    ret = extended_finger_search(self.corpus, res['c1h1'], res['c1h2'], res['c2h1'], res['c2h2'], res['logic'])
    #    pprint(ret)

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
                                 'Token frequency': 1})
        self.accept()

#app = QApplication(sys.argv)
#main = HandshapeSearchDialog(None, None, None, None)
#main.show()
#sys.exit(app.exec_())