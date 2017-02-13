from enum import Enum
import itertools

class Fingers(Enum):

    global_ = (1, None)
    thumb = (2, '[LUO][{<=][HEefF]{2}')
    #thumbAndFinger = (3, '[ftbru][tdpM][fbru][tdmpM]\u2205/[-1\s][-2\s][-3\s][-4\s]')
    thumbAndFinger = (3, '[ftbru][tdpM][fbru][tdmpM]\u2205[-1\s][-2\s][-3\s][-4\s]')
    index = (4, '1[EFHi]{3}')
    middle = (5, '[EFHi]2[EFHi]{2}')
    ring = (6, '[EFHi]{2}3[EFHi]')
    pinky = (7, '[EFHi]{3}4')
    contact = (8,'[{<=]')

    def __init__(self, num, symbols):
        self.num = num
        self.symbols = symbols

    @property
    def features(self):
        if self.symbols is None:
            return None
        triples = [triple for triple in itertools.product(self.symbols, repeat=3)]
        marked = list()
        for n in range(len(triples)):
            # Constraint - no medial joint can be 'H'
            if triples[n][1] == 'H':
                marked.append(n)
            # Constraint - distal joint must match medial join in flexion
            # distal = triples[n][2]
            # medial = triples[n][1]
            # if (distal == 'f' and medial=='F') or (distal =='F' and medial == 'f'):
            #     marked.append(n)
        triples = [triples[n] for n in range(len(triples)) if not n in marked]
        return triples

class Locations(Enum):

    Head = ['CheekNose', 'Chin', 'Eye', 'Forehead', 'HeadTop', 'Mouth', 'UnderChin', 'UpperLip', 'Other']
    Arm = ['ElbowBack', 'ElbowFront', 'ForearmBack', 'ForearmFront', 'ForearmUlnar', 'UpperArm',
           'WristBack', 'WristFront', 'Other']
    Trunk = ['Clavicle', 'Hips', 'Neck', 'Neutral', 'Shoulder', 'TorsoBottom', 'TorsoMid', 'TorsoTop', 'Waist', 'Other']
    NonDominant = ['FingerBack', 'FingerFront', 'FingerRadial', 'FingerUlnar', 'Heel', 'Palm', 'PalmBack', 'Other']
    Neutral = ['FingerRadial', 'Neutral', 'Palm', 'Other']
    Other = []

class Movements(Enum):

    Arc = 1
    Circular = 2
    Straight = 3
    BackAndForth = 4
    Other = 5
    NoMove = 6
    Multiple = 7