from enum import Enum
import itertools
from collections import OrderedDict

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

class Sign():

    sign_attributes = ['gloss', 'config1', 'config2', 'major', 'minor', 'movement', 'orientation']

    headers = ['gloss',
                       'config1hand1', 'config1hand2',
                       'config2hand1', 'config2hand2',
                       'major', 'minor',
                       'movement', 'orientation']
    for config_num in [1, 2]:
        for hand_num in [1, 2]:
            for slot_num in range(1, 35):
                headers.append('config{}hand{}slot{}'.format(config_num,hand_num, slot_num))
    headers = ';'.join(headers)

    def __init__(self, data):
        self.attributes = list()
        for key,value in data:
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

    def data(self):
        return OrderedDict([(key,getattr(self, key)) for key in Sign.sign_attributes])

    def export(self):
        output = list()
        for key,value in self.data().items():

            if 'config' in key:
                for hand in value:
                    if hand[0]:
                        hand[0] = 'Y'
                    else:
                        hand[0] = 'N'
                    output.append(''.join(hand))
                continue

            if key == 'major':
                value = 'None' if not value else value
            elif key == 'minor':
                value = 'None' if not value else value
            elif key == 'orientation':
                value = 'None' if not value else value
            elif key  == 'movement':
                value = 'None' if not value else value
            output.append(value)



        for config_num in [1,2]:
            for hand_num in [0,1]:
                slot_list = getattr(self, 'config{}'.format(config_num))[hand_num]
                for slot_num in range(34):
                    output.append(slot_list[slot_num])
        output = ';'.join(output)

        return output