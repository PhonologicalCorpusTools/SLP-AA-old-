from enum import Enum
import itertools

class Fingers(Enum):

    global_ = (1, None)
    thumb = (2, '[LUO][{<=][HEefF]{2}')
    thumbAndFinger = (3, '[ftbru][tdpM][fbru][tdmpM][1\s][2\s][3\s][4\s]')
    index = (4, '[EFHi]{3}')
    middle = (5, '[EFHi]{3}')
    ring = (6, '[EFHi]{3}')
    pinky = (7, '[EFHi]{3}')
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

class Sign():

    sign_attributes = {'major': None, 'minor': None,
                    'movement': None, 'orientation': None,
                    'config1hand1': None, 'config1hand2': None,
                    'config2hand1': None, 'config2hand2': None,
                    'gloss': None}

    def __init__(self, data):
        self.attributes = list()
        for key,value in data.items():
            self.attributes.append(key)
            setattr(self, key, value)

    def __eq__(self, other):
        if not isinstance(other, Sign):
            return False
        else:
            return self.gloss == other.gloss

    def __str__(self):
        return self.gloss

    def __repr__(self):
        return self.__str__()

    def getConfigInfo(self, config_num, hand_num):
        pass
