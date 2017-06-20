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

class TerminalParameter:

    def __init__(self, name, parent):
        self.name =name
        self.parent = parent
        self.is_default = True if self.name == parent.default else False

    def __str__(self):
        return self.name

#QUALITY PARAMETERS
Quality = Parameter(name='Quality')
Temporal = Parameter(name='Temporal', children = ['None', 'Prolonged', 'Shortened', 'Accelerating'], default='None', parent=Quality)
NonTemporal = Parameter(name='Non-temporal', children = ['None', 'Tensed', 'Reduced', 'Enlarged'], default='None', parent=Quality)
Contact = Parameter(name='Contact', children=['None', 'Contacting'], default='None', parent=Quality)
Quality.addChildren([Temporal, NonTemporal, Contact])


#MAJOR MOVEMENT PARAMETERS
MajorMovement = Parameter(name='Major Movement')
ContourMovement = Parameter(name='Contour of movement', children = ['Hold', 'Straight', 'Arc', 'Circle', 'Seven'], default='Hold', parent=MajorMovement)
ContourPlane = Parameter(name='Contour planes', children = ['Hold', 'Horizontal', 'Vertical', 'Surface', 'Midline', 'Oblique'], default='Hold', parent=MajorMovement)
Repetition = Parameter(name='Repetition',children=['None', 'Once', 'Twice', 'Multiple'], default='None', parent=MajorMovement)
Direction = Parameter(name = 'Direction', children = ['None', 'Forward', 'Backward'], default='None', parent=MajorMovement)
MajorMovement.addChildren([ContourMovement, ContourPlane, Repetition, Direction])

#LOCAL MOVEMENT PARAMETERS
LocalMovement = Parameter(name='Local Movement', children=['Hold', 'Wiggling', 'Hooking', 'Flattening', 'Twisting',
                                                           'Nodding', 'Releasing', 'Rubbing', 'Circling'],
                                                 default='Hold')

#MAJOR LOCATION PARAMETERS
MajorLocation = Parameter(name='Major Location')
WeakHandLocation = Parameter(name='Weak hand location')
SignSpaceLocation = Parameter(name='Signing space location')
NonDominantLocation = Parameter(name='Non-dominant hand location')

HandPart = Parameter(name = 'Hand part', children = ['Hand', 'Fingers', 'Thumb', 'Index', 'Middle', 'Ring', 'Pinky'], parent=WeakHandLocation)
WeakHandZone = Parameter(name = 'Zone', children = ['Inside', 'Pad', 'Back', 'Radial', 'Ulnar', 'Tips', 'Knuckle',
                                                    'Base', 'Heel', 'Web', 'Palm'], parent=WeakHandLocation)
WeakHandLocation.addChildren([HandPart, WeakHandZone])

BodyLocation = Parameter(name='Body location', children=['Back of head', 'Top of head', 'Forehead', 'Side of head'], default='Back of head', parent=WeakHandLocation, is_default=True)
ForwardDistance = Parameter(name='Degrees of forward distance', children=['Unspecified', 'Proximal', 'Medial', 'Distal'], default='Unspecified', parent=WeakHandLocation)
SideToSide = Parameter(name='Side-to-side dimension', children=['No offset', 'In line with breast', 'In line with shoulder'], default='No offset', parent=WeakHandLocation)
Height = Parameter(name='Height', children=['Top of head', 'Forehead', 'Nose', 'Mouth', 'Chin'], default='Chin', parent=WeakHandLocation)
Vector = Parameter(name='Vector', children=['L3', 'L2', 'L1', '0', 'R1', 'R2', 'R3'], default='0', parent=WeakHandLocation)
SignSpaceLocation.addChildren([ForwardDistance, SideToSide, Height, Vector])

HandPart = Parameter(name='Hand part location', children = ['Hand', 'Fingers', 'Thumb', 'Index', 'Middle', 'Pinky'], default='Hand', parent=WeakHandLocation)
SigningSpaceZone = Parameter(name='Zone', children = ['Inside', 'Pad', 'Back', 'Radial', 'Ulnar'], default='Inside', parent=WeakHandLocation)
NonDominantLocation.addChildren([HandPart, SigningSpaceZone])

MajorLocation.addChildren([BodyLocation, SignSpaceLocation, NonDominantLocation])

defaultParameters = [Quality, MajorMovement, LocalMovement, MajorLocation]