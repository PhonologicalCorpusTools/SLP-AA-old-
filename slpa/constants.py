GLOBAL_OPTIONS = ['forearm', 'estimated', 'uncertain', 'incomplete', 'reduplicated']

X_IN_BOX = '\u2327'

NULL = '\u2205'

STANDARD_SYMBOLS = ['_', '+', '-', '/', '1', '2', '3', '4', '<', '=', '?', 'E', 'F', 'H', 'L', 'M', 'O', 'U', 'V',
                    'b', 'd', 'e', 'f', 'fr', 'i', 'm', 'p', 'r', 't', 'u', 'x', 'x+', 'x-', '{', NULL, X_IN_BOX]

FINGER_SYMBOLS = ['H', 'E', 'e', 'i', 'F', 'f', '?']

CONTACT_SYMBOLS = ['{', '<', '=', 'x-', 'x', 'x+', X_IN_BOX, '?']

SYMBOL_DESCRIPTIONS = {
    'L': 'lateral',
    'U': 'unopposed',
    'O': 'opposed',
    'x': 'crossed with contact',
    'x+': 'ultracrossed',
    'x-': 'slightly crossed with contact',
    X_IN_BOX: 'crossed without contact',
    '?': 'unestimatable',
    '{': 'full abduction',
    '<': 'neutral',
    '=': 'adducted',
    '-': 'no contact',
    't': 'tip',
    'fr': 'friction surface',
    'b': 'back surface',
    'r': 'radial surface',
    'u': 'ulnar surface',
    'd': 'distal',
    'p': 'proximal',
    'm': 'medial',
    'M': 'meta-carpal',
    '1': 'contact with index finger',
    '2': 'contact with middle finger',
    '3': 'contact with ring finger',
    '4': 'contact with pinky finger',
    'H' : 'hyperextended',
    'E' : 'fully extended',
    'F' : 'fully flexed',
    'i' : 'clearly intermediate',
    'e' : 'somewhat extended',
    'f' : 'somewhat flexed'}