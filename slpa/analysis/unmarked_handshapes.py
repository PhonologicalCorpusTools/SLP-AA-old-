from constants import X_IN_BOX, NULL


class HandshapeEmpty(object):
    options = [
        ['_'], ['_'], ['_'], ['_'],
        ['_'], ['_'], [NULL], ['/'], ['_'], ['_'], ['_'], ['_'], ['_'], ['_'],
        ['1'], ['_'], ['_'], ['_'],
        ['_'], ['2'], ['_'], ['_'], ['_'],
        ['_'], ['3'], ['_'], ['_'], ['_'],
        ['_'], ['4'], ['_'], ['_'], ['_']
    ]

    def __init__(self):
        super().__init__()

    @staticmethod
    def match(sign):
        for symbol, allowed in zip(sign, HandshapeEmpty.options):
            if symbol not in allowed:
                return False
        return True


class HandshapeAny(object):
    options = [
        ['L', 'U', 'O', '?', '_'], ['{', '<', '=', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'],
        ['-', 't', 'fr', 'b', 'r', 'u', '?', '_'], ['-', 'd', 'p', 'M', '?', '_'], [NULL], ['/'], ['-', 't', 'fr', 'b', 'r', 'u', '?', '_'], ['-', 'd', 'm', 'p', 'M', '?', '_'], ['-', '1', '?', '_'], ['-', '2', '?', '_'], ['-', '3', '?', '_'], ['-', '4', '?', '_'],
        ['1'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'],
        ['{', '<', '=', 'x-', 'x', 'x+', X_IN_BOX, '?', '_'], ['2'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'],
        ['{', '<', '=', 'x-', 'x', 'x+', X_IN_BOX, '?', '_'], ['3'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'],
        ['{', '<', '=', 'x-', 'x', 'x+', X_IN_BOX, '?', '_'], ['4'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_'], ['H', 'E', 'e', 'i', 'F', 'f', '?', '_']
    ]

    def __init__(self):
        super().__init__()

    @staticmethod
    def match(sign):
        for symbol, allowed in zip(sign, HandshapeAny.options):
            if symbol not in allowed:
                return False
        return True


class HandshapeC(object):
    options = [
        ['O'], ['<'], ['E', 'e', 'i'], ['E', 'e', 'i'],
        ['-'], ['-'], [NULL], ['/'], ['-'], ['-'], ['-'], ['-'], ['-'], ['-'],
        ['1'], ['e', 'i', 'f'], ['e', 'i', 'f'], ['E', 'e', 'i', 'f'],
        ['=', 'x-'], ['2'], ['e', 'i', 'f'], ['e', 'i', 'f'], ['E', 'e', 'i', 'f'],
        ['=', 'x-'], ['3'], ['e', 'i', 'f'], ['e', 'i', 'f'], ['E', 'e', 'i', 'f'],
        ['=', 'x-'], ['4'], ['E', 'e', 'i', 'f'], ['E', 'e', 'i', 'f'], ['E', 'e', 'i', 'f']
    ]

    def __init__(self):
        super().__init__()

    # constraint1: options[2] and options[3] can't be more than one value apart from each other
    @staticmethod
    def satisfy_const1(sign):
        # not okay: (E, i), (i, E)
        if (sign[2], sign[3]) in [('E', 'i'), ('i', 'E')]:
            return False
        else:
            return True

    # constraint2: options[15], options[20], and options[25] must exactly match each other
    @staticmethod
    def satisfy_const2(sign):
        if sign[15] != sign[20] or sign[15] != sign[25] or sign[20] != sign[25]:
            return False
        else:
            return True

    # constraint3: options[16], options[21], and options[26] can't be more than one-value apart from each other
    @staticmethod
    def satisfy_const3(sign):
        # not okay: e, f together
        if 'e' in [sign[16], sign[21], sign[26]] and 'f' in [sign[16], sign[21], sign[26]]:
            return False
        else:
            return True

    # constraint4: options[17], options[22], and options[27] can't be more than one-value apart from each other
    @staticmethod
    def satisfy_const4(sign):
        # E, e, i, f
        # not okay: (E, i), (E, f), (e, f)
        if ('E' in [sign[17], sign[22], sign[27]] and 'i' in [sign[17], sign[22], sign[27]]) \
                or ('E' in [sign[17], sign[22], sign[27]] and 'f' in [sign[17], sign[22], sign[27]]) \
                or ('e' in [sign[17], sign[22], sign[27]] and 'f' in [sign[17], sign[22], sign[27]]):
            return False
        else:
            return True

    # constraint5: options[30] can't be more than one value apart from options[15], options[20], options[25]
    @staticmethod
    def satisfy_const5(sign):
        # [15, 20, 25]: e, i, f
        # [30]: E, e, i, f
        if sign[30] == 'E':
            if 'i' in [sign[15], sign[20], sign[25]] or 'f' in [sign[15], sign[20], sign[25]]:
                return False
            else:
                return True
        elif sign[30] == 'e':
            if 'f' in [sign[15], sign[20], sign[25]]:
                return False
            else:
                return True
        elif sign[30] == 'i':
            return True
        else:  # sign[30] == 'f':
            if 'e' in [sign[15], sign[20], sign[25]]:
                return False
            else:
                return True

    # constraint6: options[31] can't be more than two values apart from options[16], options[21], options[26]
    @staticmethod
    def satisfy_const6(sign):
        # [16, 21, 26]: e, i, f
        # [31]: E, e, i, f
        if sign[31] == 'E':
            if 'f' in [sign[16], sign[21], sign[26]]:
                return False
            else:
                return True
        elif sign[31] == 'e':
            return True
        elif sign[31] == 'i':
            return True
        else:  # sign[30] == 'f':
            return True

    @staticmethod
    def match(sign):
        for symbol, allowed in zip(sign, HandshapeC.options):
            if symbol not in allowed:
                return False

        return all([HandshapeC.satisfy_const1(sign), HandshapeC.satisfy_const2(sign), HandshapeC.satisfy_const3(sign),
                    HandshapeC.satisfy_const4(sign), HandshapeC.satisfy_const5(sign), HandshapeC.satisfy_const6(sign)])



