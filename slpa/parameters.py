import anytree

class Parameter:

    def __init__(self, name, children=None, parent=None, default=None, is_default=False):
        self.name = name
        self.parent = parent
        self.default = default
        self.is_default = is_default
        self.children = list()
        self.defaultChild = None
        if children is not None:
            for child in children:
                if isinstance(child, str):
                    child = TerminalParameter(child, self)
                if child.name == self.default:
                    child.is_default = True
                    self.defaultChild = child
                else:
                    child.is_default = False
                self.children.append(child)

    def sortChildren(self):
        if self.children is not None:
            sortedList = [child for child in self.children if child.is_default]
            toSort = [child for child in self.children if not child.is_default]
            toSort.sort()
            sortedList.extend(toSort)
            self.children = sortedList

    def getDefaultValue(self):
        for child in self.children:
            if child.name == self.default:
                return child
        else:
            return None

    def addChildren(self, children):
        for c in children:
            self.children.append(c)
        self.children.sort()

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.children)

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name

    def __iter__(self):
        for child in self.children:
            yield child

class TerminalParameter:

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.is_default = True if self.name == parent.default else False
        self.children = tuple()

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.name < other.name

    def __gt__(self, other):
        return self.name > other.name


allParameters = list()

#QUALITY PARAMETERS
Quality = Parameter(name='Quality')
Temporal = Parameter(name='Temporal', children = ['None', 'Prolonged', 'Shortened', 'Accelerating'], default='None', parent=Quality)
NonTemporal = Parameter(name='Non-temporal', children = ['None', 'Tensed', 'Reduced', 'Enlarged'], default='None', parent=Quality)
Contact = Parameter(name='Contact', children=['None', 'Contacting'], default='None', parent=Quality)
Quality.addChildren([Temporal, NonTemporal, Contact])
allParameters.append(Quality)
allParameters.extend(Quality.children)
allParameters.extend(Temporal.children)
allParameters.extend(NonTemporal.children)
allParameters.extend(Contact.children)


#MAJOR MOVEMENT PARAMETERS
MajorMovement = Parameter(name='Major Movement')
ContourMovement = Parameter(name='Contour of movement', children = ['Hold', 'Straight', 'Arc', 'Circle', 'Seven'], default='Hold', parent=MajorMovement)
ContourMovement.sortChildren()
ContourPlane = Parameter(name='Contour planes', children = ['Hold', 'Horizontal', 'Vertical', 'Surface', 'Midline', 'Oblique'], default='Hold', parent=MajorMovement)
ContourPlane.sortChildren()
Repetition = Parameter(name='Repetition',children=['None', 'Once', 'Twice', 'Multiple'], default='None', parent=MajorMovement)
Direction = Parameter(name = 'Direction', children = ['None', 'Forward', 'Backward'], default='None', parent=MajorMovement)
MajorMovement.addChildren([ContourMovement, ContourPlane, Repetition, Direction])
allParameters.append(MajorMovement)
allParameters.append(ContourMovement)
allParameters.extend(ContourMovement.children)
allParameters.append(ContourPlane)
allParameters.extend(ContourPlane.children)
allParameters.append(Repetition)
allParameters.extend(Repetition.children)
allParameters.append(Direction)
allParameters.extend(Direction.children)

#LOCAL MOVEMENT PARAMETERS
LocalMovement = Parameter(name='Local Movement', children=['Hold', 'Wiggling', 'Hooking', 'Flattening', 'Twisting', 'Nodding', 'Releasing', 'Rubbing', 'Circling', 'Shaking'], default='Hold')
LocalMovement.sortChildren()
allParameters.append(LocalMovement)
allParameters.extend(LocalMovement.children)

#MAJOR LOCATION PARAMETERS
MajorLocation = Parameter(name='Major Location')
SignSpaceLocation = Parameter(name='Signing space location',  is_default=True, parent=MajorLocation)
WeakHandLocation = Parameter(name='Non-dominant hand location', parent=MajorLocation)
allParameters.extend([MajorLocation, SignSpaceLocation, WeakHandLocation])

BodyLocation = Parameter(name='Body location', children=['Back of head', 'Top of head', 'Forehead', 'Side of forehead', 'Nose', 'Cheek', 'Ear', 'Mouth', 'Lip', 'Jaw', 'Chin', 'Neck', 'Shoulder', 'Sternum', 'Chest', 'Trunk', 'Upper arm', 'Forearm', 'Abdomen', 'Leg'], default='Trunk', parent=MajorLocation)

ForwardDistance = Parameter(name='Degrees of forward distance', children=['Unspecified', 'Proximal', 'Medial', 'Distal', 'Extended'], default='Unspecified', parent=SignSpaceLocation)
SideToSide = Parameter(name='Side-to-side dimension', children=['No offset', 'In line with breast', 'In line with shoulder'], default='No offset', parent=SignSpaceLocation)
Height = Parameter(name='Height', children=['Top of head', 'Forehead', 'Nose', 'Mouth', 'Chin', 'Neck', 'Sternum', 'Chest', 'Trunk', 'Abdomen'], default='Trunk', parent=SignSpaceLocation)
Vector = Parameter(name='Vector', children=['L3', 'L2', 'L1', '0', 'R1', 'R2', 'R3'], default='0', parent=SignSpaceLocation)
SignSpaceLocation.addChildren([ForwardDistance, Height, SideToSide, Vector])
allParameters.extend([BodyLocation, ForwardDistance, SideToSide, Height, Vector])
allParameters.extend(BodyLocation.children)
allParameters.extend(ForwardDistance.children)
allParameters.extend(SideToSide.children)
allParameters.extend(Height.children)
allParameters.extend(Vector.children)

HandPart = Parameter(name='Hand part location', children = ['Hand', 'Fingers', 'Thumb', 'Index', 'Middle', 'Pinky'], default='Hand', parent=WeakHandLocation)
SigningSpaceZone = Parameter(name='Zone', children = ['Inside', 'Pad', 'Back', 'Radial', 'Ulnar', 'Tips', 'Knuckle', 'Base', 'Heel', 'Web', 'Palm', 'Arm'], default='Palm', parent=WeakHandLocation)
SigningSpaceZone.sortChildren()
WeakHandLocation.addChildren([HandPart, SigningSpaceZone])
allParameters.extend([HandPart, SigningSpaceZone])
allParameters.extend(HandPart.children)
allParameters.extend(SigningSpaceZone.children)

def getAllParameters():
    return allParameters[:]

MajorLocation.addChildren([SignSpaceLocation, BodyLocation, WeakHandLocation])

defaultParameters = [Quality, MajorMovement, LocalMovement, MajorLocation]

def encodeXMLName(name):
    if name == 0 or name == '0':
        name = 'Zero'
    return name.replace(' ', '_')

def decodeXMLName(name):
    if name == 'Zero':
        name = '0'
    return name.replace('_', ' ')

def addChild(parentNode, childParameter):
    node = anytree.Node(childParameter.name, parent=parentNode)
    for child in childParameter.children:
        addChild(node, child)

defaultParameterTree = anytree.Node('Parameters', parent = None)
for parameter in defaultParameters:
    parentNode = anytree.Node(parameter.name, parent = defaultParameterTree)
    for childParameter in parameter.children:
        addChild(parentNode, childParameter)


def getParameterFromXML(element):
    for p in getAllParameters():
        if element.attrib['name'] == p.name:
            parentName = 'Parameters' if p.parent is None else p.parent.name
            if element.attrib['parent'] == parentName:
                return p
    else:
        raise AttributeError('No parameter named {} exists'.format(element.attrib['name']))