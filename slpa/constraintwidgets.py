from constraints import *
from imports import (QWidget, QDialog, QVBoxLayout, QHBoxLayout, QComboBox, QStackedWidget,
                     QPushButton, QCheckBox, QLabel, QTabWidget)

class ConstraintTab(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

class ConstraintsDialog(QDialog):
    def __init__(self, constraints):
        super().__init__()
        self.setWindowTitle('Select constraints')
        self.constraints = constraints
        layout = QVBoxLayout()

        self.transcriptionPage = QWidget()
        self.populateTranscriptionPage()
        self.simplePage = QWidget()
        self.populateSimplePage()
        self.conditionalPage = QWidget()
        self.populateConditionalPage()

        self.pageSelection = QComboBox()
        self.pageSelection.addItem('Transcription Constraints')
        self.pageSelection.addItem('Simple Constraints')
        self.pageSelection.addItem('Conditional Constraints')
        layout.addWidget(self.pageSelection)

        self.pages = QStackedWidget()
        self.pages.addWidget(self.transcriptionPage)
        self.pages.addWidget(self.simplePage)
        self.pages.addWidget(self.conditionalPage)
        self.pageSelection.currentIndexChanged.connect(self.pages.setCurrentIndex)
        self.pages.setCurrentIndex(0)
        layout.addWidget(self.pages)

        buttonLayout = QHBoxLayout()
        selectThisPageButton = QPushButton('Select all (this page)')
        selectThisPageButton.clicked.connect(self.selectThisPage)
        buttonLayout.addWidget(selectThisPageButton)
        selectAllButton = QPushButton('Select all (global)')
        selectAllButton.clicked.connect(self.selectAll)
        buttonLayout.addWidget(selectAllButton)
        removeThisPageButton = QPushButton('Unselect all (this page)')
        removeThisPageButton.clicked.connect(self.removeThisPage)
        buttonLayout.addWidget(removeThisPageButton)
        removeAllButton = QPushButton('Unselect all (global)')
        removeAllButton.clicked.connect(self.removeAll)
        buttonLayout.addWidget(removeAllButton)
        okCancelLayout = QHBoxLayout()
        ok = QPushButton('OK')
        cancel = QPushButton('Cancel')
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)
        okCancelLayout.addWidget(ok)
        okCancelLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)
        layout.addLayout(okCancelLayout)

        self.setLayout(layout)

    def populateTranscriptionPage(self):
        layout = QVBoxLayout()
        for c in MasterConstraintList:
            if c[1].constraint_type == 'transcription':
                checkBox = QCheckBox(c[1].explanation)
                setattr(self, c[0], checkBox)
                if self.constraints[c[0]]:
                    checkBox.setChecked(True)
                layout.addWidget(checkBox)
        self.transcriptionPage.setLayout(layout)

    def populateSimplePage(self):
        layout = QVBoxLayout()
        for c in MasterConstraintList:
            if c[1].constraint_type == 'simple':
                checkBox = QCheckBox(c[1].explanation)
                setattr(self, c[0], checkBox)
                if self.constraints[c[0]]:
                    checkBox.setChecked(True)
                layout.addWidget(checkBox)
        self.simplePage.setLayout(layout)

    def populateConditionalPage(self):
        layout = QVBoxLayout()
        for c in MasterConstraintList:
            if c[1].constraint_type == 'conditional':
                checkBox = QCheckBox(c[1].explanation)
                setattr(self, c[0], checkBox)
                if self.constraints[c[0]]:
                    checkBox.setChecked(True)
                layout.addWidget(checkBox)
        self.conditionalPage.setLayout(layout)

    def selectThisPage(self):
        thisPage = self.pages.currentIndex()
        if thisPage == 0:
            constraints = [c for c in MasterConstraintList if c[1].constraint_type == 'transcription']
        elif thisPage == 1:
            constraints = [c for c in MasterConstraintList if c[1].constraint_type == 'simple']
        elif thisPage == 2:
            constraints = [c for c in MasterConstraintList if c[1].constraint_type == 'conditional']
        for c in constraints:
            getattr(self, c[0]).setChecked(True)


    def removeThisPage(self):
        thisPage = self.pages.currentIndex()
        if thisPage == 0:
            constraints = [c for c in MasterConstraintList if c[1].constraint_type == 'transcription']
        elif thisPage == 1:
            constraints = [c for c in MasterConstraintList if c[1].constraint_type == 'simple']
        elif thisPage == 2:
            constraints = [c for c in MasterConstraintList if c[1].constraint_type == 'conditional']
        for c in constraints:
            getattr(self, c[0]).setChecked(False)

    def selectAll(self):
        for c in MasterConstraintList:
            getattr(self, c[0]).setChecked(True)

    def removeAll(self):
        for c in MasterConstraintList:
            getattr(self, c[0]).setChecked(False)

class ConstraintCheckMessageBox(QDialog):

    def __init__(self, constraints, configTabs):
        super().__init__()
        self.setWindowTitle('Transcription verification')
        layout = QVBoxLayout()
        if all([not value for value in constraints.values()]):
            layout.addWidget(QLabel('There were no problems detected with your transcription, '
                            'because no constraints have been selected. '
                          '\nTo set constraints, go to the Settings menu.'))
            buttonLayout = QHBoxLayout()
            ok = QPushButton('OK')
            ok.clicked.connect(self.accept)
            buttonLayout.addWidget(ok)
            layout.addLayout(buttonLayout)
            self.setLayout(layout)
            self.violations = {}
            return

        self.satisfied_message = 'This constraint is fully satisfied.\n("{}")'
        self.violations = {'config1hand1': {n:set() for n in range(35)}, 'config2hand1': {n:set() for n in range(35)},
                           'config1hand2': {n:set() for n in range(35)}, 'config2hand2': {n:set() for n in range(35)}}

        layout = QVBoxLayout()

        self.pageSelection = QComboBox()
        self.pageSelection.addItem('Transcription constraints')
        self.pageSelection.addItem('Simple constraints')
        self.pageSelection.addItem('Conditional constraints')
        layout.addWidget(self.pageSelection)

        self.pages = QStackedWidget()
        self.transcriptionsConstraintsTab = QTabWidget()
        self.transcriptionsConstraintsTab.currentChanged.connect(self.changedTab)
        self.pages.addWidget(self.transcriptionsConstraintsTab)
        self.simpleConstraintsTab = QTabWidget()
        self.simpleConstraintsTab.currentChanged.connect(self.changedTab)
        self.pages.addWidget(self.simpleConstraintsTab)
        self.conditionalConstraintsTab = QTabWidget()
        self.conditionalConstraintsTab.currentChanged.connect(self.changedTab)
        self.pages.addWidget(self.conditionalConstraintsTab)
        self.pageSelection.currentIndexChanged.connect(self.pages.setCurrentIndex)
        self.selected_page = 0
        self.selected_tab = 0
        self.page_maximum = self.pages.count()
        self.pages.currentChanged.connect(self.changedPage)

        #first, add all of the selected constraints to the stacked widgets
        # selected_constraints = list()
        # for c in MasterConstraintList:
        #     alert_text = list()
        #     constraint_text = list()
        #     if constraints[c[0]]:
        #         selected_constraints.append(c)
        #         tab = ConstraintTab()
        #         if c[1].constraint_type == 'transcription':
        #             self.transcriptionsConstraintsTab.addTab(tab, c[1].name)
        #         elif c[1].constraint_type == 'simple':
        #             self.simpleConstraintsTab.addTab(tab, c[1].name)
        #         elif c[1].constraint_type == 'conditional':
        #             self.conditionalConstraintsTab.addTab(tab, c[1].name)
        #             no_problems = True
        #then check to see if any constraints are actually violated
        #if they are, then add them to the self.violations set

        problems = dict()
        for constraint_name, constraint in MasterConstraintList:
            if not constraints[constraint_name]:
                continue
            if constraint in UnsupportedConstraints:
                problems[constraint_name] = [(('The constraint "{}" is not supported '
                                            'in the current version of SLPAnnotator'.format(constraint_name)), constraint)]
                continue
            for j in [1,2]:
                for k in [0,1]:
                    transcription = 'hand{}Transcription'.format(j)
                    transcription = getattr(configTabs.widget(k), transcription)
                    result = constraint.check(transcription.slots)
                    if result:
                        handconfig = 'config{}hand{}'.format(k+1, j)
                        for slot in result.split(', '):
                            self.violations[handconfig][int(slot)].add(constraint.name)
                    else:
                        result = 'This constraint is fully satisfied.'
                    text = 'Config {}, Hand {}: {}'.format(k+1, j, result)
                    info = (text, constraint)
                    try:
                        problems[constraint_name].append(info)
                    except (KeyError, AttributeError):
                        problems[constraint_name] = [info]

        for name,details in problems.items():
            tab = ConstraintTab()
            constraint_type = details[-1][-1].constraint_type
            labeltext = '\n'.join([d[0] for d in details])
            tab.layout.addWidget(QLabel(labeltext))
            if constraint_type == 'transcription':
                self.transcriptionsConstraintsTab.addTab(tab, name)
            elif constraint_type == 'simple':
                self.simpleConstraintsTab.addTab(tab, name)
            elif constraint_type == 'conditional':
                self.conditionalConstraintsTab.addTab(tab, name)

        if not problems:
            layout.addWidget(QLabel('All constraints are satisfied!'))
        else:
            layout.addWidget(self.pages)


        self.tab_maximum = {page_number:self.pages.widget(page_number).count()-1
                                     for page_number in range(self.page_maximum)}
        buttonLayout = QHBoxLayout()
        ok = QPushButton('OK')
        ok.clicked.connect(self.accept)
        buttonLayout.addWidget(ok)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def keyPressEvent(self, e):
        key = e.key()
        if key == 0x01000012: #Left key
            self.selected_tab -= 1
            if self.selected_tab < 0:
                self.selected_tab = self.tab_maximum[self.selected_page]
            self.pages.widget(self.selected_page).setCurrentIndex(self.selected_tab)
        elif key == 0x01000014: #Right key
            self.selected_tab += 1
            if self.selected_tab > self.tab_maximum[self.selected_page]:
                self.selected_tab = 0
            self.pages.widget(self.selected_page).setCurrentIndex(self.selected_tab)

    def changedPage(self, new_page):
        self.selected_page = new_page

    def changedTab(self, new_tab):
        self.selected_tab = new_tab