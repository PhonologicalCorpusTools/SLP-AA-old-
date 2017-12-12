from collections import defaultdict
from math import log2 as log
from transcriptions import STANDARD_SYMBOLS
from imports import (QDialog, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QButtonGroup, QPushButton,
                    QStackedWidget, QWidget, QComboBox, QMessageBox, QLabel, QLineEdit)


class FunctionalLoadDialog(QDialog):

    def __init__(self, corpus):
        super().__init__()
        self.corpus = corpus

        self.setWindowTitle('Functional Load')
        layout = QVBoxLayout()

        #Set up top row of radio button options
        contrastBox = QGroupBox('Contrast')
        contrastLayout = QHBoxLayout()
        self.contrastGroup = QButtonGroup()
        flexionOption = QRadioButton('Degrees of flexion')
        flexionOption.click()
        ductionOption = QRadioButton('Degree of duction')
        oppositionOption = QRadioButton('Thumb opposition')
        contactOption = QRadioButton('Thumb/finger contact')
        customOption = QRadioButton('Custom options')
        self.contrastGroup.addButton(flexionOption, id=0)
        self.contrastGroup.addButton(ductionOption, id=1)
        self.contrastGroup.addButton(oppositionOption, id=2)
        self.contrastGroup.addButton(contactOption, id=3)
        self.contrastGroup.addButton(customOption, id=4)
        contrastLayout.addWidget(flexionOption)
        contrastLayout.addWidget(ductionOption)
        contrastLayout.addWidget(oppositionOption)
        contrastLayout.addWidget(contactOption)
        contrastLayout.addWidget(customOption)
        contrastBox.setLayout(contrastLayout)

        #set up stacked widgets
        self.middleWidget = QStackedWidget()

        #Collapse degress of flexion
        flexionWidget = QWidget()
        flexionLayout = QHBoxLayout()
        self.flexionFingerSelection = QComboBox()
        self.flexionFingerSelection.addItems(['Thumb', 'Index', 'Middle', 'Pinky', 'Ring', 'All'])
        self.flexionJointSelection = QComboBox()
        self.flexionJointSelection.addItems(['Proximal', 'Medial', 'Distal', 'All'])
        #note: Thumb+Proximal not possible, and there's an alert window that will pop up if this combination is chosen
        flexionLayout.addWidget(self.flexionFingerSelection)
        flexionLayout.addWidget(self.flexionJointSelection)
        flexionWidget.setLayout(flexionLayout)

        #Collapse degrees of duction
        ductionWidget = QWidget()
        ductionLayout = QHBoxLayout()
        self.ductionFingerSelection = QComboBox()
        self.ductionFingerSelection.addItems(['Thumb/Finger', 'Index/Middle', 'Middle/Ring', 'Ring/Pinky', 'All'])
        ductionLayout.addWidget(self.ductionFingerSelection)
        ductionWidget.setLayout(ductionLayout)

        #Collapse thumb opposition
        oppositionWidget = QWidget()
        oppositionLayout = QHBoxLayout()
        oppositionWidget.setLayout(oppositionLayout)

        #Collapse thumb/finger contact
        contactWidget = QWidget()
        contactLayout = QHBoxLayout()
        contactWidget.setLayout(contactLayout)

        #Collapse custom slots
        customWidget = QWidget()
        customLayout = QHBoxLayout()
        customLayout.addWidget(QLabel('Merge this symbol: '))
        self.customSymbo1A = QComboBox()
        self.customSymbo1A.addItem('')
        self.customSymbo1A.addItems(STANDARD_SYMBOLS)
        self.customSymbo1A.setEditable(True)
        customLayout.addWidget(self.customSymbo1A)
        customLayout.addWidget(QLabel('with this symbol: '))
        self.customSymbolB = QComboBox()
        self.customSymbolB.addItem('')
        self.customSymbolB.addItems(STANDARD_SYMBOLS)
        self.customSymbolB.setEditable(True)
        customLayout.addWidget(self.customSymbolB)
        customLayout.addWidget(QLabel('in these slots: '))
        self.customSlots = QLineEdit()
        customLayout.addWidget(self.customSlots)
        customLayout.addWidget(QLabel('(separate numbers with commas, leave blank to merge symbols everywhere)'))
        customWidget.setLayout(customLayout)

        #Build up middle widget
        self.middleWidget.addWidget(flexionWidget)
        self.middleWidget.addWidget(ductionWidget)
        self.middleWidget.addWidget(oppositionWidget)
        self.middleWidget.addWidget(contactWidget)
        self.middleWidget.addWidget(customWidget)

        #Connect slots and signals
        flexionOption.clicked.connect(self.changeMiddleWidget)
        ductionOption.clicked.connect(self.changeMiddleWidget)
        oppositionOption.clicked.connect(self.changeMiddleWidget)
        contactOption.clicked.connect(self.changeMiddleWidget)
        customOption.clicked.connect(self.changeMiddleWidget)

        #Bottom buttons (OK/Cancel)
        buttonLayout = QHBoxLayout()
        ok = QPushButton('OK')
        ok.clicked.connect(self.accept)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)

        layout.addWidget(contrastBox)
        layout.addWidget(self.middleWidget)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def changeMiddleWidget(self, e):
        self.middleWidget.setCurrentIndex(self.contrastGroup.id(self.sender()))

    def accept(self):
        index = self.middleWidget.currentIndex()
        if index == 0:
            if (self.flexionFingerSelection.currentText() == 'Thumb'
                    and self.flexionJointSelection.currentText() == 'Proximal'):
                alert = QMessageBox()
                alert.setWindowTitle('Incompatible Options')
                alert.setText('Thumbs cannot be selected for proximal joint. Choose either "Medial" or "Distal"')
                alert.exec_()
                return
            self.calcByFlexion()
        elif index == 1:
            self.calcByDuction()

        elif index == 4:
            self.calcCustom()

        super().accept()

    def calculateEntropy(self):
        corpus_size = len(self.corpus)
        return corpus_size, sum([1 / corpus_size * log(1 / corpus_size) for n in range(corpus_size)]) * -1


    def calcByDuction(self):
        corpus_size, starting_h = self.calculateEntropy()
        duction = self.ductionFingerSelection.currentText()
        if duction == 'Thumb/Finger':
            slot = 2
        elif duction == 'Index/Middle':
            slot = 19
        elif duction == 'Middle/Ring':
            slot = 24
        elif duction == 'Ring/Pinky':
            slot = 29
        elif duction == 'All':
            slot = -1

        if slot > 1:
            print('{} DUCTION'.format(duction.upper()))
            print('Starting size = {}\nStarting entropy = {}'.format(corpus_size, starting_h))
            new_corpus = defaultdict(int)
            for word in self.corpus:
                ch = word.config1hand1.copy()
                ch[slot] = 'X'
                new_corpus[''.join(ch)] += 1
            new_corpus_size = len(new_corpus)
            ending_h = sum([new_corpus[word] / new_corpus_size * log(new_corpus[word] / new_corpus_size)
                            for word in new_corpus]) * -1
            print('After merging size = {}\nAfter merging entropy = {}'.format(len(new_corpus), ending_h))
            print('Change in entropy = {}\n'.format(starting_h - ending_h))
        else:
            print('{} DUCTION'.format(duction.upper()))
            print('Starting size = {}\nStarting entropy = {}'.format(corpus_size, starting_h))
            new_corpus = defaultdict(int)
            for word in self.corpus:
                ch = word.config1hand1.copy()
                ch[2] = 'X'
                ch[19] = 'X'
                ch[24] = 'X'
                ch[29] = 'X'
                new_corpus[''.join(ch)] += 1
            new_corpus_size = len(new_corpus)
            ending_h = sum([new_corpus[word] / new_corpus_size * log(new_corpus[word] / new_corpus_size)
                            for word in new_corpus]) * -1
            print('After merging size = {}\nAfter merging entropy = {}'.format(len(new_corpus), ending_h))
            print('Change in entropy = {}\n'.format(starting_h - ending_h))

    def calcCustom(self):
        corpus_size, starting_h = self.calculateEntropy()

        slots = self.customSlots.text()
        if slots:
            slots = [int(n)-1 for n in slots.split(',')]
        else:
            slots = [n for n in range(34)]
        #minus 1 because slot numbers starts at 1 but list indices start at 0
        symbolA = self.customSymbo1A.currentText()
        symbolB = self.customSymbolB.currentText()

        print('Merging {} and {}'.format(symbolA, symbolB))
        print('Starting size = {}\nStarting entropy = {}'.format(corpus_size, starting_h))
        new_corpus = defaultdict(int)
        for word in self.corpus:
            ch = word.config1hand1.copy()
            for slot in slots:
                if ch[slot] in [symbolA, symbolB]:
                    ch[slot] = 'X'

            new_corpus[''.join(ch)] += 1

        new_corpus_size = len(new_corpus)
        ending_h = sum([new_corpus[word] / new_corpus_size * log(new_corpus[word] / new_corpus_size)
                        for word in new_corpus]) * -1
        print('After merging size = {}\nAfter merging entropy = {}'.format(len(new_corpus), ending_h))
        print('Change in entropy = {}\n'.format(starting_h - ending_h))


    def calcByFlexion(self):
        corpus_size, starting_h = self.calculateEntropy()

        finger = self.flexionFingerSelection.currentText()
        joint = self.flexionJointSelection.currentText()

        jointDict = {'Proximal': 0,
                     'Medial': 1,
                     'Distal': 2,
                     'All': -1}

        fingerDict = {'Thumb':2,
                      'Index': 16,
                      'Middle': 21,
                      'Ring': 26,
                      'Pinky': 31,
                      'All': -1}

        offset = jointDict[joint]
        slot = fingerDict[finger]
        slot += offset

        if slot > 0:#user chose particular fingers

            print('{} {} JOINTS'.format(finger.upper(), joint.upper()))
            print('Starting size = {}\nStarting entropy = {}'.format(corpus_size, starting_h))
            new_corpus = defaultdict(int)
            for word in self.corpus:
                ch = word.config1hand1.copy()
                ch[slot] = 'X'
                new_corpus[''.join(ch)] += 1

            new_corpus_size = len(new_corpus)
            ending_h = sum([new_corpus[word] / new_corpus_size * log(new_corpus[word] / new_corpus_size)
                            for word in new_corpus]) * -1
            print('After merging size = {}\nAfter merging entropy = {}'.format(len(new_corpus), ending_h))
            print('Change in entropy = {}\n'.format(starting_h - ending_h))

        else: #user chose an "All" option

            if joint == 'All' and finger != 'All':
                #all the joints on a particular finger

                slot = fingerDict[finger]

                print('ALL {} JOINTS'.format(finger.upper()))
                print('Starting size = {}\nStarting entropy = {}'.format(corpus_size, starting_h))
                new_corpus = defaultdict(int)
                for word in self.corpus:
                    ch = word.config1hand1.copy()
                    ch[slot] = 'X' #proximal
                    ch[slot+2] = 'X' #medial
                    ch[slot+3] = 'X' #distal
                    new_corpus[''.join(ch)] += 1

                new_corpus_size = len(new_corpus)
                ending_h = sum([new_corpus[word]/new_corpus_size*log(new_corpus[word]/new_corpus_size)
                                for word in new_corpus])*-1
                print('After merging size = {}\nAfter merging entropy = {}'.format(len(new_corpus), ending_h))
                print('Change in entropy = {}\n'.format(starting_h-ending_h))

            elif finger == 'All' and joint != 'All':
                #a particular joint on all the fingers

                if joint == 'Proximal':
                    slot = 17
                elif joint == 'Medial':
                    slot = 18
                elif joint == 'Distal':
                    slot = 19

                print('ALL {} JOINTS'.format(joint.upper()))
                print('Starting size = {}\nStarting entropy = {}'.format(corpus_size, starting_h))
                # for finger,slot in [('INDEX', 17), ('MIDDLE',22), ('RING',27), ('PINKY',32)]:
                new_corpus = defaultdict(int)
                for word in self.corpus:
                    ch = word.config1hand1.copy()
                    ch[slot] = 'X'
                    ch[slot+5] = 'X'
                    ch[slot+10] = 'X'
                    ch[slot+15] = 'X'
                    new_corpus[''.join(ch)] += 1

                    new_corpus_size = len(new_corpus)
                    ending_h = sum([new_corpus[word]/new_corpus_size*log(new_corpus[word]/new_corpus_size)
                                    for word in new_corpus])*-1
                print('After merging size = {}\nAfter merging entropy = {}'.format(len(new_corpus), ending_h))
                print('Change in entropy = {}\n'.format(starting_h-ending_h))


            elif finger == 'All' and joint == 'All':

                for finger, slot in [('INDEX', 17), ('MIDDLE', 22), ('RING', 27), ('PINKY', 31)]:
                    print('ALL {} JOINTS'.format(joint.upper()))
                    print('Starting size = {}\nStarting entropy = {}'.format(corpus_size, starting_h))
                    new_corpus = defaultdict(int)
                    for word in self.corpus:
                        ch = word.config1hand1.copy()
                        ch[slot] = 'X'
                        ch[slot+1] = 'X'
                        ch[slot+2] = 'X'
                        new_corpus[''.join(ch)] += 1

                    new_corpus_size = len(new_corpus)
                    ending_h = sum([new_corpus[word]/new_corpus_size*log(new_corpus[word]/new_corpus_size)
                                    for word in new_corpus])*-1
                    print('After merging size = {}\nAfter merging entropy = {}'.format(len(new_corpus), ending_h))
                    print('Change in entropy = {}\n'.format(starting_h-ending_h))