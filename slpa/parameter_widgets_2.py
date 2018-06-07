import parameters
import sys
import anytree
from collections import defaultdict
from imports import (QApplication, Qt, QDialog, QTreeView, QStandardItemModel, QStandardItem, QVBoxLayout, QHBoxLayout,
                     QTextEdit, QPushButton, QGridLayout)


class ParameterDialog(QDialog):

    def __init__(self, model):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Select Parameters')
        self.adjustedHeight = self.frameGeometry().height()
        self.adjustedWidth = self.frameGeometry().width()
        self.adjustedPos = self.pos()
        self.model = model
        self.displayTree = anytree.Node('Selected Parameters', parent=None)
        self.selectionLayout = QVBoxLayout()
        self.displayTreeWidget = QTextEdit()
        self.treeView = ParameterTreeView()
        self.treeView.setModel(self.model)

        layout = QVBoxLayout()
        self.parameterLayout = QHBoxLayout()

        #self.generateDisplayTreeText()
        self.selectionLayout.addWidget(self.displayTreeWidget)
        self.parameterLayout.addWidget(self.treeView)
        self.parameterLayout.addLayout(self.selectionLayout)

        terminalNodesLayout = QVBoxLayout()
        self.terminalNodesLabel = QTextEdit('No parameters selected')
        terminalNodesLayout.addWidget(self.terminalNodesLabel)
        self.parameterLayout.addLayout(terminalNodesLayout)

        buttonLayout = QGridLayout()
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')
        resetButton = QPushButton('Reset to default values')
        clearButton = QPushButton('Clear all check boxes')
        buttonLayout.addWidget(resetButton,0, 0)
        buttonLayout.addWidget(clearButton,0, 1)
        buttonLayout.addWidget(okButton, 1, 0)
        buttonLayout.addWidget(cancelButton, 1, 1)
        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)
        resetButton.clicked.connect(self.reset)
        clearButton.clicked.connect(self.clear)

        layout.addLayout(self.parameterLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.resize(self.adjustedHeight, self.adjustedWidth)
        self.move(self.adjustedPos)

    def clear(self):
        continue_ = self.showWarning()
        if continue_:
            self.treeWidget.clearChecks()
            self.updateDisplayTree(True)

    def reset(self):
        continue_ = self.showWarning()
        if continue_:
            self.treeWidget.resetChecks()
            self.updateDisplayTree(True)

class ParameterTreeModel(QStandardItemModel):
    def __init__(self, parameterList):
        super().__init__()
        self.buttonGroups = defaultdict(list)
        self.specialButtons = list()
        topItem = self.invisibleRootItem()

        for p in parameterList:
            self.addItem(p, topItem)

        self.buttonGroups['Major Location'].extend(self.specialButtons)

    def handleItemChanged(self, item):
        if item.parent is None:
            return

        for button in self.buttonGroups[item.parent.name()]:
            if button.name() == item.name():
                button.setCheckState(True)
                #addToTree = True
            else:
                button.setCheckState(False)

        #self.parent.updateDisplayTree(addToTree)

    def addItem(self, parameter, parent):
        newItem = ParameterTreeItem(parameter, parent=parent)

        if parameter.children:
            parent.appendRow(newItem)
            for child in parameter.children:
                self.addItem(child, newItem)
        else:
            newItem.setCheckable(True)
            parent.appendRow(newItem)
            self.buttonGroups[parameter.parent.name].append(newItem)

        #special handling for Major Location, which has a set of non-terminals that are checkable
        if parameter.parent is not None and parameter.parent.name == 'Major Location':
            newItem.setCheckable(True)
            newItem.setCheckState(False)
            if parameter.name == 'Body location':
                newItem.setCheckState(True)
            self.specialButtons.append(newItem)

class ParameterTreeView(QTreeView):
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.handleClick)

    def handleClick(self, index):
        item = self.model().itemFromIndex(index)
        self.model().handleItemChanged(item)


class ParameterTreeItem(QStandardItem):
    def __init__(self, parameter, parent=None):
        super().__init__()
        self.parameter = parameter
        self.setText(parameter.name)
        self.parent = parent
        self.setEditable(False)
        self.setTristate(False)

    def name(self):
        return self.parameter.name

app = QApplication(sys.argv)

model = ParameterTreeModel(parameters.defaultParameters)
dialog = ParameterDialog(model)

dialog.exec_()