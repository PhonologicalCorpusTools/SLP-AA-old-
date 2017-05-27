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

#QUALITY PARAMETERS
Temporal = Parameter(name='Temporal', children = ['None', 'Prolonged', 'Shortened', 'Accelerating'])
NonTemporal = Parameter(name='Non-temporal', children = ['None', 'Tensed', 'Reduced', 'Enlarged'])
Contact = Parameter(name='Contact', children=['None', 'Contacting'])
Quality = Parameter(name='Quality', children=[Temporal, NonTemporal, Contact])

#MAJOR MOVEMENT PARAMETERS
ContourMovement = Parameter(name='Contour of movement', children = ['Hold', 'Straight', 'Arc', 'Circle', 'Seven'])
ContourPlane = Parameter(name='Contour planes', children = ['Hold', 'Horizontal', 'Vertical', 'Surface', 'Midline', 'Oblique'])
Repetition = Parameter(name='Repetition',children=['None', 'Once', 'Twice', 'Multiple'])
Direction = Parameter(name = 'Direction', children = ['None', 'Forward', 'Backward'])
MajorMovement = Parameter(name='Major movement', children=[ContourMovement, ContourPlane, Repetition, Direction])

#MAJOR LOCATION PARAMETERS
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




