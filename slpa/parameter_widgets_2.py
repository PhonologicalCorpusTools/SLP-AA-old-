import parameters
import sys
import anytree
import binary
from collections import defaultdict
from imports import (QApplication, Qt, QDialog, QTreeView, QStandardItemModel, QStandardItem, QVBoxLayout, QHBoxLayout,
                     QTextEdit, QPushButton, QGridLayout, QMessageBox)


class ParameterDialog(QDialog):

    def __init__(self, model):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Select Parameters')
        self.adjustedHeight = self.frameGeometry().height()
        self.adjustedWidth = self.frameGeometry().width()
        self.adjustedPos = self.pos()

        self.model = model
        self.model.itemChanged.connect(self.updateDisplayTree)

        self.treeView = ParameterTreeView()
        self.treeView.setModel(self.model)
        self.treeView.clicked.connect(self.updateDisplayTree)

        self.displayTree = anytree.Node('Selected Parameters', parent=None)
        self.displayTreeWidget = QTextEdit()

        layout = QVBoxLayout()
        self.selectionLayout = QVBoxLayout()
        self.parameterLayout = QHBoxLayout()
        self.selectionLayout.addWidget(self.displayTreeWidget)
        self.parameterLayout.addWidget(self.treeView)
        self.parameterLayout.addLayout(self.selectionLayout)

        self.buildDisplayTree(self.model.invisibleRootItem(), self.displayTree)
        self.generateDisplayTreeText()

        terminalNodesLayout = QVBoxLayout()
        self.terminalNodesLabel = QTextEdit('No parameters selected')
        terminalNodesLayout.addWidget(self.terminalNodesLabel)
        self.parameterLayout.addLayout(terminalNodesLayout)
        self.updateTerminalNodes()

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

    def saveParameters(self):
        def traverse(item):
            item.parameter.is_checked = True if item.checkState() else False
            if item.isEditable():
                item.parameter.name = item.text()
            for m in range(item.rowCount()):
                newItem = item.child(m)
                traverse(newItem)
        output = list()
        for j in range(self.model.invisibleRootItem().rowCount()):
            item = self.model.item(j)
            traverse(item)
            output.append(self.model.item(j).parameter)

        binary.save_binary(output, r'C:\Users\Scott\Documents\GitHub\SLP-Annotator\slpa\test_parameter_output.params')
        return output


    def buildDisplayTree(self, modelItem, displayNode):
        canBeChecked = modelItem.isCheckable()
        if (not canBeChecked) or (canBeChecked and modelItem.checkState()):
            #display anything that cannot be checked (e.g. parent items like Quality or Location)
            #or display anything that could be checked and actually is
            newDisplayNode = anytree.Node(modelItem.text(), parent=displayNode)
            for n in range(modelItem.rowCount()):
                child = modelItem.child(n)
                self.buildDisplayTree(child, newDisplayNode)

    def generateDisplayTreeText(self):
        self.displayTreeWidget.clear()
        treeText = list()
        for pre, fill, node in anytree.RenderTree(self.displayTree):
            treeText.append("{}{}".format(pre, node.name))
        treeText = '\n'.join(treeText)
        self.displayTreeWidget.setText(treeText)

    def clear(self):
        continue_ = self.showWarning()
        if continue_:
            self.displayTreeWidget.clearChecks()
            self.updateDisplayTree()

    def showWarning(self):
        alert = QMessageBox()
        alert.setWindowFlags(Qt.WindowStaysOnTopHint)
        alert.setWindowTitle('Warning')
        alert.setText('This will erase your currently selected parameters. This action cannot be undone. Continue?')
        alert.addButton('OK', QMessageBox.AcceptRole)
        alert.addButton('Cancel', QMessageBox.RejectRole)
        alert.exec_()
        role = alert.buttonRole(alert.clickedButton())
        if role == QMessageBox.AcceptRole:
            return True
        else:
            return False

    def closeEvent(self, e):
        self.close()

    def reset(self):
        continue_ = self.showWarning()
        if continue_:
            self.treeWidget.resetChecks()
            self.updateDisplayTree(True)

    def accept(self):
        self.saveParameters()
        self.adjustedHeight = self.frameGeometry().height()
        self.adjustedWidth = self.frameGeometry().width()
        self.adjustedPos = self.pos()
        self.hide()

    def reject(self):
        self.adjustedHeight = self.frameGeometry().height()
        self.adjustedWidth = self.frameGeometry().width()
        self.adjustedPos = self.pos()
        self.hide()

    def updateDisplayTree(self):
        self.displayTree = anytree.Node('Selected Parameters', parent=None)
        self.buildDisplayTree(self.model.invisibleRootItem(), self.displayTree)
        self.generateDisplayTreeText()
        self.updateTerminalNodes()

    def updateTerminalNodes(self):
        text = list()
        for pre, fill, node in anytree.RenderTree(self.displayTree):
            if node.is_leaf:
                text.append(' : '.join([node.parent.name, node.name]))
        text = '\n'.join(text)
        self.terminalNodesLabel.setText(text)


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
                item.parameter.is_checked = True
            else:
                button.setCheckState(False)
                item.parameter.is_checked = False

    def addItem(self, parameter, parent):
        newItem = ParameterTreeItem(parameter, parent=parent)

        if parameter.children:
            parent.appendRow(newItem)
            for child in parameter.children:
                self.addItem(child, newItem)
        else: #it's a terminal node, which is checkable
            newItem.setCheckable(True)
            if parameter.is_checked:
                newItem.setCheckState(True)
            if parameter.is_editable:
                newItem.setEditable(True)
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

    def __str__(self):
        return self.parameter.name

    def __repr__(self):
        return self.__str__()

app = QApplication(sys.argv)


params = binary.load_binary(r'C:\Users\Scott\Documents\GitHub\SLP-Annotator\slpa\test_parameter_output.params')
model = ParameterTreeModel(params)
#model = ParameterTreeModel(parameters.defaultParameters)
dialog = ParameterDialog(model)

dialog.exec_()