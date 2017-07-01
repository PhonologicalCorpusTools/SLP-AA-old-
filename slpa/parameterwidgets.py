from imports import *
from collections import defaultdict
import parameters
import anytree

class ParameterTreeWidget(QTreeWidget):
    itemChecked = Signal(object, int)

    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog
        self.buttonGroups = defaultdict(list)
        self.itemClicked.connect(self.handleItemChanged)
        self.currentItemChanged.connect(self.handleItemChanged)
        self.currentItemChanged.connect(self.dialog.updateDisplayTree)

    def resetChecks(self):
        treeItem = self.invisibleRootItem()
        self._resetChecks(treeItem)

    def clearChecks(self):
        treeItem = self.invisibleRootItem()
        self._resetChecks(treeItem, checkStrategy='reset')

    def loadChecks(self):
        treeItem = self.invisibleRootItem()
        self._resetChecks(treeItem, checkStrategy='load')

    def _resetChecks(self, treeItem, checkStrategy='defaults'):
        for n in range(treeItem.childCount()):
            child = treeItem.child(n)
            if child.flags() & Qt.ItemIsUserCheckable:
                if checkStrategy == 'reset':
                    child.setCheckState(0, Qt.Unchecked)
                elif checkStrategy == 'load':
                    if child.is_checked:
                        child.setCheckState(0, Qt.Checked)
                    else:
                        child.setCheckState(0, Qt.Unchecked)
                elif checkStrategy == 'defaults':
                    if child.parameter.is_default:
                        child.setCheckState(0, Qt.Checked)
                    else:
                        child.setCheckState(0, Qt.Unchecked)
            if child.childCount() > 0:
                self._resetChecks(child, checkStrategy=checkStrategy)

    def getChildren(self, node):
        if not node.childCount():
            yield node
        else:
            for n in range(node.childCount()):
                child = node.child(n)
                yield child
                self.getChildren(child)

    def topDownIter(self):
        topNode = self.invisibleRootItem()
        for node in range(topNode.childCount()):
            child = topNode.child(node)
            self.getChildren(child)

    def handleItemChanged(self, item, column):
        if item is None or item.parent() is None:
            return
        addToTree = False
        for button in self.buttonGroups[item.parent().text(0)]:
            if button.text(0) == item.text(0):
                button.setCheckState(0, Qt.Checked)
                addToTree = True
            else:
                button.setCheckState(0, Qt.Unchecked)
        self.dialog.updateDisplayTree(addToTree)

    def findTopParent(self, item):
        parent = item.parent()
        while True:
            if parent.parent() is None:
                break
            else:
                parent = parent.parent()
        return parent


class ParameterSelectionsLayout(QHBoxLayout):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.values = list()
        self.addWidget(QLabel(self.name))

    def addLabel(self, text):
        setattr(self, text+'Label', QLabel(text))
        self.values.append(text+'Label')
        self.addWidget(getattr(self, text+'Label'))

    def changeText(self, labelName, newText):
        widgetName = labelName+'Label'
        for value in self.values:
            if value == widgetName:
                getattr(self, widgetName).setText(' : '.join([labelName, newText]))
                break

class ParameterDialog(QDialog):
    updateAfterClosing = Signal(bool, anytree.Node)

    def __init__(self, model):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Select Parameters')
        self.model = model
        self.adjustedHeight = self.frameGeometry().height()
        self.adjustedWidth = self.frameGeometry().width()
        self.adjustedPos = self.pos()
        self.tree = ParameterTreeWidget(self)
        self.displayTree = anytree.Node('Selected Parameters', parent=None)
        self.selectionLayout = QVBoxLayout()
        self.displayTreeWidget = QTextEdit()
        self.specialButtons = list()

        layout = QVBoxLayout()
        parameterLayout = QHBoxLayout()

        for p in model.tree.children:
            displayNode = anytree.Node(p.name, parent=self.displayTree)
            parent = ParameterTreeWidgetItem(self.tree, parameter=p)
            parent.setFlags(Qt.ItemIsSelectable | parent.flags() ^ Qt.ItemIsUserCheckable)
            parent.setText(0, p.name)
            self.addChildren(parent, p, p.name, displayNode)

        self.tree.buttonGroups['Major Location'].extend(self.specialButtons)
        self.generateDisplayTreeText()
        self.selectionLayout.addWidget(self.displayTreeWidget)
        parameterLayout.addWidget(self.tree)
        parameterLayout.addLayout(self.selectionLayout)

        terminalNodesLayout = QVBoxLayout()
        self.terminalNodesLabel = QTextEdit('No parameters selected')
        terminalNodesLayout.addWidget(self.terminalNodesLabel)
        parameterLayout.addLayout(terminalNodesLayout)

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

        layout.addLayout(parameterLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.resize(self.adjustedHeight, self.adjustedWidth)
        self.move(self.adjustedPos)

    def reset(self):
        continue_ = self.showWarning()
        if continue_:
            self.tree.resetChecks()
            self.updateDisplayTree(True)

    def clear(self):
        continue_ = self.showWarning()
        if continue_:
            self.tree.clearChecks()
            self.updateDisplayTree(True)

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


    def addChildren(self, parentWidget, parentParameter, top_parameter, displayNode, checkDefaults=False):
        buttonGroup = list()
        appendGroup = False

        for c in parentParameter.children:
            child = ParameterTreeWidgetItem(parentWidget, parameter=c)
            if c.is_leaf:
                child.setText(0, c.name)
                child.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                if checkDefaults and c.parameter.is_default:
                    child.setCheckState(0, Qt.Checked)
                    c.is_checked = True
                else:
                    child.setCheckState(0, Qt.Unchecked)

                buttonGroup.append(child)
                appendGroup = True
            else:
                #it's a non-terminal node
                newDisplayNode = anytree.Node(c.name, parent=displayNode)
                child.setText(0, c.name)
                if parentParameter.name == 'Major Location':
                    child.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    child.setCheckState(0, Qt.Unchecked)
                    if c.name == 'Body location':
                        child.setCheckState(0, Qt.Checked)
                        c.is_checked = True
                    self.specialButtons.append(child)
                else:
                    child.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable^child.flags())
                self.addChildren(child, c, top_parameter, newDisplayNode, checkDefaults=checkDefaults)

        if appendGroup:
            self.tree.buttonGroups[parentParameter.name].extend(buttonGroup)

    def closeEvent(self, e):
        self.reject()

    def accept(self):
        self.updateAfterClosing.emit(True, self.model.tree)
        self.adjustedHeight = self.frameGeometry().height()
        self.adjustedWidth = self.frameGeometry().width()
        self.adjustedPos = self.pos()
        self.hide()

    def reject(self):
        self.updateAfterClosing.emit(False, self.model.tree)
        self.adjustedHeight = self.frameGeometry().height()
        self.adjustedWidth = self.frameGeometry().width()
        self.adjustedPos = self.pos()
        self.hide()

    def generateDisplayTreeText(self):
        treeText = list()
        for pre, fill, node in anytree.RenderTree(self.displayTree):
            treeText.append("{}{}".format(pre, node.name))
        treeText = '\n'.join(treeText)
        self.displayTreeWidget.setText(treeText)

    def buildTree(self, treeWidgetItem, displayTreeItem):
        canBeChecked = treeWidgetItem.flags() & Qt.ItemIsUserCheckable
        if (not canBeChecked) or (canBeChecked and treeWidgetItem.checkState(0)):
            newDisplayNode = anytree.Node(treeWidgetItem.text(0), parent=displayTreeItem)
            for n in range(treeWidgetItem.childCount()):
                child = treeWidgetItem.child(n)
                self.buildTree(child, newDisplayNode)

    def updateDisplayTree(self, addToTree=None):
        if not addToTree:
            return

        topNode = anytree.Node('Selected Parameters', parent=None)
        root = self.tree.invisibleRootItem()
        self.buildTree(root, topNode)
        self.displayTree = topNode

        treeText = list()
        for pre, fill, node in anytree.RenderTree(self.displayTree):
            treeText.append("{}{}".format(pre, node.name))
        self.displayTreeWidget.clear()
        self.displayTreeWidget.setText('\n'.join(treeText))
        self.updateTerminalNodes()

    def updateTerminalNodes(self):
        text = list()
        true_children = [node.name for pre, fill, node in anytree.RenderTree(self.model.tree) if node.is_leaf]
        for pre, fill, node in anytree.RenderTree(self.displayTree):
            if node.is_leaf and node.name in true_children:
                text.append(' : '.join([node.parent.name, node.name]))
        text = '\n'.join(text)
        self.terminalNodesLabel.setText(text)

class ParameterTreeWidgetItem(QTreeWidgetItem):

    def __init__(self, parent, parameter=None):
        super().__init__(parent)
        self.parameter = parameter

    def setData(self, column, role, value):
        state = self.checkState(column)
        super().setData(column, role, value)
        if (role == Qt.CheckStateRole and
            state != self.checkState(column)):
            treewidget = self.treeWidget()
            if treewidget is not None:
                treewidget.itemChecked.emit(self, column)

class ParameterTreeModel:

    def __init__(self, parameterList):
        self.tree = anytree.Node('Parameters', parent=None)
        for p in parameterList:
            parameterNode = ParameterNode(p, parent=self.tree) #anytree.Node(p.name, parent=self.tree)
            setattr(self, p.name, parameterNode)
            for child in p.children:
                self.addNode(child, parameterNode)

    def addNode(self, parameter, parentNode):
        if hasattr(parameter, 'children'):
            newNode = ParameterNode(parameter, parent=parentNode)#anytree.Node(parameter.name, parent=parentNode)
            for c in parameter.children:
                self.addNode(c, newNode)
        else:
            newNode = ParameterNode(parameters.TerminalParameter(parameter.name, parentNode), parent=parentNode) #anytree.Node(parameter, parent=parentNode)

    def __getitem__(self, item):
        for node in self.tree.children:
            if node.name == item:
                return node
        else:
            return None

    def __iter__(self):
        for node in self.tree.children:
            yield node.name


class ParameterNode(anytree.Node):

    def __init__(self, parameter, parent=None, checked=False):
        super().__init__(parameter.name, parent=parent)
        self.name = parameter.name
        self.parameter = parameter
        self.is_default = self.parameter.is_default
        self.is_checked = checked
        if isinstance(self.parameter, parameters.TerminalParameter):
           self.default = None
        else:
            self.default = self.parameter.default

    def printTree(self):
        treeText = list()
        for pre, fill, node in anytree.RenderTree(self):
            treeText.append("{}{}".format(pre, node.name))
        treeText = '\n'.join(treeText)
        print(treeText)