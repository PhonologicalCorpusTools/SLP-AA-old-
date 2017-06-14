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

        for button in self.buttonGroups[item.parent().text(0)]:
            if button.text(0) == item.text(0):
                button.setCheckState(0, Qt.Checked)
                self.dialog.updateDisplayTree(addToTree=True)
            else:
                button.setCheckState(0, Qt.Unchecked)
                #self.dialog.updateDisplayTree(button.text(0), item.parent().text(0), addToTree=False)

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
            parent = ParameterTreeWidgetItem(self.tree)
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

        buttonLayout = QHBoxLayout()
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')
        resetButton = QPushButton('Reset to default values')
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addWidget(resetButton)
        okButton.clicked.connect(self.accept)
        cancelButton.clicked.connect(self.reject)
        resetButton.clicked.connect(self.reset)

        layout.addLayout(parameterLayout)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.resize(self.adjustedHeight, self.adjustedWidth)
        self.move(self.adjustedPos)

    def reset(self):
        self.displayTreeWidget.clear()
        self.tree = ParameterTreeWidget(self)
        self.terminalNodesLabel.setText('')
        self.specialButtons = list()
        for p in self.model.tree.children:
            displayNode = anytree.Node(p.name, parent=self.displayTree)
            parent = ParameterTreeWidgetItem(self.tree)
            parent.setFlags(Qt.ItemIsSelectable | parent.flags() ^ Qt.ItemIsUserCheckable)
            parent.setText(0, p.name)
            self.addChildren(parent, p, p.name, displayNode, checkDefaults=True)
        self.tree.buttonGroups['Major Location'].extend(self.specialButtons)
        self.updateDisplayTree(True)

    def addChildren(self, parentWidget, parentParameter, top_parameter, displayNode, checkDefaults=False):
        buttonGroup = list()
        appendGroup = False

        for c in parentParameter.children:
            child = ParameterTreeWidgetItem(parentWidget)
            if c.is_leaf:
                child.setText(0, c.name)
                child.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                if checkDefaults and c.parameter.is_default:
                    child.setCheckState(0, Qt.Checked)
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
                    self.specialButtons.append(child)
                else:
                    child.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable^child.flags())
                self.addChildren(child, c, top_parameter, newDisplayNode, checkDefaults)

        if appendGroup:
            self.tree.buttonGroups[parentParameter.name].extend(buttonGroup)

    def closeEvent(self, e):
        self.reject()

    def accept(self):
        self.updateAfterClosing.emit(True, self.displayTree)
        self.adjustedHeight = self.frameGeometry().height()
        self.adjustedWidth = self.frameGeometry().width()
        self.adjustedPos = self.pos()
        self.hide()

    def reject(self):
        self.updateAfterClosing.emit(False, self.displayTree)
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
        if addToTree is None:
            return #in this case user clicked text, not a checkbox

        if addToTree:
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

    def __init__(self, parent):
        super().__init__(parent)

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

    def __init__(self, parameter, parent=None):
        super().__init__(parameter.name, parent=parent)
        self.name = parameter.name
        self.parameter = parameter
        if isinstance(self.parameter, parameters.TerminalParameter):
           self.default = None
        else:
            self.default = self.parameter.default