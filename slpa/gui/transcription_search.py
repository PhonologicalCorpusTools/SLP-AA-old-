from imports import (QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QPushButton, QLabel, QButtonGroup,
                     QRadioButton, QApplication, QGridLayout, QTabWidget, QWidget,
                     QSizePolicy, Qt, Slot, QListWidget, QListView, QListWidgetItem, QIcon,
                     QStandardItemModel, QStandardItem, QSize, QLineEdit)
from constants import GLOBAL_OPTIONS
import sys
import os
from gui.function_windows import FunctionDialog, FunctionWorker
from gui.transcriptions import TranscriptionConfigTab
from gui.phonological_search import LogicRadioButtonGroup
from image import getMediaFilePath
import regex as re
from pprint import pprint
from completer_test import TransConfigTab


class TSWorker(FunctionWorker):
    def run(self):
        # TODO: implement this
        pass


class TranscriptionSearchDialog(FunctionDialog):
    header = ['Corpus', 'Sign', 'Token frequency', 'Note']
    about = 'Transcription search'
    name = 'transcription search'

    def __init__(self, corpus, parent, settings, recent):
        super().__init__(parent, settings, TSWorker())

        self.corpus = corpus
        self.recent = recent

        globalFrame = QGroupBox('Global options')
        globalLayout = QHBoxLayout()
        globalFrame.setLayout(globalLayout)

        forearmButton = QCheckBox('Forearm')
        globalLayout.addWidget(forearmButton)
        estimatedButton = QCheckBox('Estimated')
        globalLayout.addWidget(estimatedButton)
        uncertainButton = QCheckBox('Uncertain')
        globalLayout.addWidget(uncertainButton)
        incompleteButton = QCheckBox('Incomplete')
        globalLayout.addWidget(incompleteButton)

        config1Frame = QGroupBox('Config 1')
        config1Layout = QVBoxLayout()
        config1Frame.setLayout(config1Layout)

        #config1 = TranscriptionConfigTab(1)
        config1 = TransConfigTab()
        config1Layout.addWidget(config1)

        config2Frame = QGroupBox('Config 2')
        config2Layout = QVBoxLayout()
        config2Frame.setLayout(config2Layout)

        #config2 = TranscriptionConfigTab(2)
        config2 = TransConfigTab()
        config2Layout.addWidget(config2)

        mainLayout = QGridLayout()
        self.setLayout(mainLayout)
        mainLayout.addWidget(globalFrame, 0, 0)
        mainLayout.addWidget(config1Frame, 1, 0)
        mainLayout.addWidget(config2Frame, 2, 0)
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

app = QApplication(sys.argv)
main = TranscriptionSearchDialog(None, None, None, None)
main.show()
sys.exit(app.exec_())