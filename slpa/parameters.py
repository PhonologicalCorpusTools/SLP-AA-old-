from imports import *
from collections import defaultdict

class ListViewParameters(QDialog):

    def __init__(self, parameters, max_list = 4):
        super().__init__()
        self.parameters = parameters
        layout = QHBoxLayout()
        topList = QListWidget()
        layout.addWidget(topList)
        for n in max_list:
            setattr(self, 'list{}'.format(n), QListWidget())
            layout.addWidget(getattr(self, 'list{}'.format(n)))

        for p in parameters:
            topList.addItem(p.name)
        topList.currentItemChanged.connect(self.nextList)

    def nextList(self, item):
        for p in self.parameters:
            if p.name == item:

                break

class MenuViewParameters(QDialog):

    def __init__(self, parameters):
        super().__init__()
        self.setWindowTitle('Select Parameters')
        self.layout = QGridLayout()
        row = 0
        for p in parameters:
            parameterButton = QPushButton(p.name)
            parameterMenu = QMenu(p.name)
            self.addChildren(parameterMenu, p)
            parameterButton.setMenu(parameterMenu)
            self.layout.addWidget(parameterButton, row, 0)
            row += 1
        self.setLayout(self.layout)

    def addChildren(self, parentMenu, parentParameter):
        for c in parentParameter.children:
            if isinstance(c, Parameter):
                childMenu = parentMenu.addMenu(c.name)
                #if it's a parameter, then it's a non-terminal node
                self.addChildren(childMenu, c)
            else:
                #it's a string, and therefore a terminal node
                action = QAction(c, self, checkable = True)
                parentMenu.addAction(action)

class ParameterTreeWidget(QTreeWidget):
    itemChecked = Signal(object, int)

    def __init__(self):
        super().__init__()

def handleItemChecked(self, item, column):
    print('ItemChecked', int(item.checkState(column)))

class TreeViewParameters(QDialog):

    def __init__(self, parameters):
        super().__init__()
        self.setWindowTitle('Select Parameters')
        layout = QVBoxLayout()
        self.tree = ParameterTreeWidget()
        self.tree.currentItemChanged.connect(self.itemChanged)
        self.buttonGroups = dict()
        for p in parameters:
            parent = ParameterTreeWidgetItem(self.tree)
            parent.setText(0, p.name)
            self.addChildren(parent, p)
        layout.addWidget(self.tree)
        self.setLayout(layout)
        self.selectionLayout = QGridLayout()
        row = 0
        for p in parameters:
            self.selectionLayout.addWidget(QLabel(p.name), row, 0)
            self.selectionLayout.addWidget(QLabel('No value selected'), row, 1)
            row += 1
        layout.addLayout(self.selectionLayout)

    def addChildren(self, parentWidget, parentParameter):
        buttonGroup = list()
        appendGroup = False
        for c in parentParameter.children:
            child = ParameterTreeWidgetItem(parentWidget)
            if isinstance(c, Parameter):
                #if it's a parameter, then it's a non-terminal node
                child.setText(0, c.name)
                self.addChildren(child, c)
            else:
                #it's a string, and therefore a terminal node
                child.setText(0, c)
                child.setFlags(Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)#(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0, Qt.Unchecked)
                buttonGroup.append(child)
                appendGroup = True
        if appendGroup:
            self.buttonGroups[parentParameter.name] = buttonGroup

    def itemChanged(self, item, column):
        if item.parent() is None:
            return
        if item.parent().text(0) not in self.buttonGroups.keys():
            return
        for button in self.buttonGroups[item.parent().text(0)]:
            if button.text(0) == item.text(0):
                button.setCheckState(0, Qt.Checked)
            else:
                button.setCheckState(0, Qt.Unchecked)

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
        return p.name

    def len(self):
        return len(self.children)


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


# MajorLocation = Parameter('Major', ['', 'Head', 'Arm', 'Trunk', 'Non-dominant', 'Neutral'])
# OneHandMovement = Parameter('One hand movement', ['','Arc', 'Circular','Straight','Back and forth', 'Multiple', 'Hold'])
# TwoHandMovement = Parameter('Two hand movement', ['', 'N/A', 'Hold', 'Alternating', 'Simaultaneous'])
# Orientation = Parameter('Orientation', ['','Front', 'Back', 'Side', 'Up', 'Down'])
# Dislocation = Parameter('Dislocation', ['', 'None', 'Right', 'Left'])


