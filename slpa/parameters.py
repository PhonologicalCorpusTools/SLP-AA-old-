from imports import *
from collections import defaultdict
import anytree

class ParameterTreeWidget(QTreeWidget):
    itemChecked = Signal(object, int)

    def __init__(self, dialog):
        super().__init__()
        self.itemClicked.connect(self.handleItemChanged)
        self.currentItemChanged.connect(self.handleItemChanged)
        self.dialog = dialog
        self.buttonGroups = defaultdict(list)

    def handleItemChanged(self, item, column):
        if item.parent() is None:
            return

        parent = self.findTopParent(item)
        selectionLayout = getattr(self.dialog, parent.text(0)+'Layout')
        selectionLayout.changeText(item.parent().text(0), item.text(0))

        for button in self.buttonGroups[item.parent().text(0)]:
            if button.text(0) == item.text(0):
                button.setCheckState(0, Qt.Checked)
            else:
                button.setCheckState(0, Qt.Unchecked)

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

class TreeViewDialog(QDialog):

    def __init__(self, parameters):
        super().__init__()
        self.setWindowTitle('Select Parameters')
        layout = QHBoxLayout()
        self.tree = ParameterTreeWidget(self)
        self.selectionLayout = QVBoxLayout()
        for p in parameters:
            setattr(self, p.name + 'Layout', ParameterSelectionsLayout(p.name))
            self.selectionLayout.addLayout(getattr(self, p.name + 'Layout'))
            parent = ParameterTreeWidgetItem(self.tree)
            parent.setText(0, p.name)
            self.addChildren(parent, p, p.name, getattr(self, p.name + 'Layout'))
        layout.addWidget(self.tree)
        layout.addLayout(self.selectionLayout)

        # for p in parameters:
        #     setattr(self, p.name+'Layout', ParameterSelectionsLayout(p.name))
        #     self.selectionLayout.addLayout(getattr(self, p.name+'Layout'))
        #     # setattr(self, p.name+'Label', QLabel('Nothing selected'))
        #     # self.selectionLayout.addWidget(getattr(self, p.name+'Label'), row, 0)
        #     # self.selectionLayout.addWidget(getattr(self, p.name+'Label'), row, 1)
        #     # self.selectionlayout.addLayout(ParameterSelectionsLayout(), row, 1)


        self.setLayout(layout)

    def addChildren(self, parentWidget, parentParameter, top_parameter, selectionLayout):
        buttonGroup = list()
        appendGroup = False
        for c in parentParameter.children:
            child = ParameterTreeWidgetItem(parentWidget)
            if isinstance(c, Parameter):
                #if it's a parameter, then it's a non-terminal node
                child.setText(0, c.name)
                self.addChildren(child, c, top_parameter, selectionLayout)
            else:
                #it's a string, and therefore a terminal node
                child.setText(0, c)
                child.setFlags(Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
                child.setCheckState(0, Qt.Unchecked)
                buttonGroup.append(child)
                appendGroup = True

        if appendGroup:
            self.tree.buttonGroups[parentParameter.name].extend(buttonGroup)
            selectionLayout.addLabel(buttonGroup[0].parent().text(0))
            #every member of the buttonGroup has the same parent, so just grab an arbitrary one and use that information


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

class Parameter(object):

    def __init__(self, name, children):
        self.name = name
        self.parent = None
        self.children = children

    def addChildren(self, children):
        for c in children:
            self.children.append(c)
        self.children.sort()

    def __str__(self):
        return self.name

    def len(self):
        return len(self.children)


class ParameterTreeModel():

    def __init__(self, parameters):
        self.tree = anytree.Node('Root', parent=None)
        for p in parameters:
            parameterNode = anytree.Node(p.name, parent=self.tree)
            setattr(self, p.name, parameterNode)
            for child in p.children:
                self.addNode(child, parameterNode)


    def addNode(self, parameter, parentNode):
        if hasattr(parameter, 'children'):
            newNode = anytree.Node(parameter.name, parent=parentNode)
            for c in parameter.children:
                self.addNode(c, newNode)
        else:
            newNode = anytree.Node(parameter, parent=parentNode)

Temporal = Parameter(name='Temporal', children = ['None', 'Prolonged', 'Shortened', 'Accelerating'])
NonTemporal = Parameter(name='Non-temporal', children = ['None', 'Tensed', 'Reduced', 'Enlarged'])
Contact = Parameter(name='Contact', children=['None', 'Contacting'])
Quality = Parameter(name='Quality', children=[Temporal, NonTemporal, Contact])

ContourMovement = Parameter(name='Contour of movement', children = ['Hold', 'Straight', 'Arc', 'Circle', 'Seven'])
ContourPlane = Parameter(name='Contour planes', children = ['Hold', 'Horizontal', 'Vertical', 'Surface', 'Midline', 'Oblique'])
Repetition = Parameter(name='Repetition',children=['None', 'Once', 'Twice', 'Multiple'])
Direction = Parameter(name = 'Direction', children = ['None', 'Forward', 'Backward'])
MajorMovement = Parameter(name='Major movement', children=[ContourMovement, ContourPlane, Repetition, Direction])

BodyLocation = Parameter(name='Body location', children=['Back of head', 'Top of head', 'Forehead', 'Side of head'])
ForwardDistance = Parameter(name='Degrees of forward distance', children=['Unspecified', 'Proximal', 'Medial', 'Distal'])
SideToSide = Parameter(name='Side-to-side dimension', children=['No offset', 'In line with breast', 'In line with shoulder'])
Height = Parameter(name='Height', children=['Top of head', 'Forehead', 'Nose', 'Mouth', 'Chin'])
Vector = Parameter(name='Vector', children=['L3', 'L2', 'L1', '0', 'R1', 'R2', 'R3'])
SignSpaceLocation = Parameter(name='Signing space location', children=[ForwardDistance, SideToSide, Height, Vector])
HandPart = Parameter(name='Hand part location', children = ['Hand', 'Fingers', 'Thumb', 'Index', 'Middle', 'Pinky'])
Zone = Parameter(name='Zone', children = ['Inside', 'Pad', 'Back', 'Radial', 'Ulnar'])
NonDominantLocation = Parameter(name='Non-dominant hand location', children=[HandPart, Zone])
MajorLocation = Parameter(name='Major Location', children=[BodyLocation, SignSpaceLocation, NonDominantLocation])

# treeModel = ParameterTreeModel([Quality, MajorMovement, MajorLocation])
# for pre, fill, node in anytree.RenderTree(treeModel.tree):
#     print("{}{}".format(pre, node.name))
#
# import pickle
# import os
# from binary import load_binary, save_binary
# save_binary(treeModel, os.path.join(os.getcwd(),'tree.tree'))
# treeModel = load_binary(os.path.join(os.getcwd(), 'tree.tree'))
# for pre, fill, node in anytree.RenderTree(treeModel.tree):
#     print("{}{}".format(pre, node.name))
# treeModel.addNode('Spam', treeModel.tree)
# # tree.addNode('Vikings', tree.)
# save_binary(treeModel, os.path.join(os.getcwd(),'tree.tree'))
# tree = load_binary(os.path.join(os.getcwd(), 'tree.tree'))
# for pre, fill, node in anytree.RenderTree(treeModel.tree):
#     print("{}{}".format(pre, node.name))
#
# MajorLocation = Parameter('Major', ['', 'Head', 'Arm', 'Trunk', 'Non-dominant', 'Neutral'])
# OneHandMovement = Parameter('One hand movement', ['','Arc', 'Circular','Straight','Back and forth', 'Multiple', 'Hold'])
# TwoHandMovement = Parameter('Two hand movement', ['', 'N/A', 'Hold', 'Alternating', 'Simaultaneous'])
# Orientation = Parameter('Orientation', ['','Front', 'Back', 'Side', 'Up', 'Down'])
# Dislocation = Parameter('Dislocation', ['', 'None', 'Right', 'Left'])


