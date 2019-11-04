from constants import X_IN_BOX, NULL

ORDER = {'H': 5, 'E': 4, 'e': 3, 'i': 2, 'F': 1, 'f': 0}


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


class Handshape1(object):
    options = [
        ['O'], ['<', '='], ['i', 'f', 'F'], ['i', 'f', 'F'],
        ['t', 'fr'], ['d'], [NULL], ['/'], ['b'], ['m'], ['-'], ['2'], ['-'], ['-'],
        ['1'], ['e', 'E'], ['e', 'E'], ['H'],
        ['='], ['2'], ['i', 'f'], ['i', 'f'], ['i', 'f'],
        ['='], ['3'], ['f', 'F'], ['i', 'f'], ['i', 'f'],
        ['='], ['4'], ['F', 'f'], ['i', 'f'], ['i', 'f']
    ]

    def __init__(self):
        super().__init__()

    # constraint1: no combination of "i" and "F" options[2] and options[3]
    @staticmethod
    def satisfy_const1(sign):
        if (sign[2], sign[3]) in [('i', 'F')]:
            return False
        else:
            return True

    # constraint2: no "e" + "H" for options[15], options[16], and options[17]
    @staticmethod
    def satisfy_const2(sign):
        if (sign[15], sign[17]) == ('e', 'H') or (sign[16], sign[17]) == ('e', 'H'):
            return False
        else:
            return True

    # constraint3: no "i" + "F" for options[25], options[26], and options[27]
    @staticmethod
    def satisfy_const3(sign):
        if (sign[25], sign[26]) == ('F', 'i') or (sign[25], sign[27]) == ('F', 'i'):
            return False
        else:
            return True

    # constraint4: no "i" + "F" for options[30], options[31], and options[32]
    @staticmethod
    def satisfy_const4(sign):
        if (sign[30], sign[31]) == ('F', 'i') or (sign[30], sign[32]) == ('F', 'i'):
            return False
        else:
            return True

    @staticmethod
    def match(sign):
        for symbol, allowed in zip(sign, Handshape1.options):
            if symbol not in allowed:
                return False

        return all([Handshape1.satisfy_const1(sign), Handshape1.satisfy_const2(sign), Handshape1.satisfy_const3(sign),
                    Handshape1.satisfy_const4(sign)])


class HandshapeS(object):
    options = [
        ['O'], ['=', '{'], ['i', 'f', 'e'], ['i', 'f', 'F', 'e'],
        ['u', 'fr'], ['d'], [NULL], ['/'], ['b'], ['m'], ['1', '-'], ['2', '-'], ['3', '-'], ['-'],
        ['1'], ['F', 'f'], ['F'], ['F', 'f'],
        ['='], ['2'], ['F', 'f'], ['F'], ['F', 'f', 'i'],
        ['='], ['3'], ['f', 'F'], ['F'], ['F', 'f', 'i'],
        ['='], ['4'], ['F', 'f'], ['F', 'f'], ['F', 'f', 'i']
    ]

    def __init__(self):
        super().__init__()

    # constraint1: option[1] and option[3]: "{" can happen only if option[3] if "F"
    @staticmethod
    def satisfy_const1(sign):
        if (sign[1], sign[3]) in [('{', 'e'), ('{', 'i')]:
            return False
        else:
            return True

    # constraint2: option[3], option[4], option[10], option[11], option[12]:
    # "u" (option[4]) can happen only if thumb only contacts finger 1 (option[10]), or thumb's DIP is "F" (option[3])
    @staticmethod
    def satisfy_const2(sign):
        if sign[4] == 'u':
            if (sign[10], sign[11], sign[12]) != ('1', '-', '-'):
                return False

            if sign[3] != 'F':
                return False

            return True
        else:
            return True

    # constraint3: option[10], option[11], option[12]:
    # Minimum contact of one finger, Maximum 2, but they have to be adjacent to each other (e.g., [12--], not [1-3-])
    @staticmethod
    def satisfy_const3(sign):
        # Minimum contact of one finger
        if (sign[10], sign[11], sign[12]) == ('-', '-', '-'):
            return False
        # Maximum 2, but they have to be adjacent to each other (e.g., [12--], not [1-3-])
        elif (sign[10], sign[11], sign[12]) in [('1', '2', '3'), ('1', '-', '3')]:
            return False
        else:
            return True

    # constraint4: option[15], option[20], option[25], option[30]: they have to have all the same flexion value (e.g., f, f, f, f),
    # or from finger 1 to finger 4 have an increasing flexion value (e.g., f,f,F,F) or increasing-decreasing (e.g.: f,F,F,f),
    # but not decreasing flexion (e.g.: F, f,f,f), decreasing-increasing (e.g.: F,f,f,F) or f, F, f, F.
    @staticmethod
    def satisfy_const4(sign):
        def is_decreasing_first(sign):
            values = [ORDER[sign[15]], ORDER[sign[20]], ORDER[sign[25]], ORDER[sign[30]]]
            compare = list()
            for i in range(4-1):
                if values[i] > values[i+1]:
                    compare.append('decrease')
                elif values[i] < values[i+1]:
                    compare.append('increase')

            if not compare:
                return False
            else:
                if compare[0] == 'decrease':
                    return True
                else:
                    return False

        return not is_decreasing_first(sign)

        # constraint5: option[17], option[22], option[27], option[32]: they have to have all the same flexion value (e.g., f,f,f,f),
        # or from thumb to finger 4 have an increasing flexion value (e.g., f, f, F, F, but not the other way around (e.g., F, f, f, i,),
        # or F, f, F, i.
    @staticmethod
    def satisfy_const5(sign):
        def has_decreasing(sign):
            values = [ORDER[sign[17]], ORDER[sign[22]], ORDER[sign[27]], ORDER[sign[32]]]
            compare = list()
            for i in range(4 - 1):
                if values[i] > values[i + 1]:
                    compare.append('decrease')
                elif values[i] < values[i + 1]:
                    compare.append('increase')

            if not compare:
                return False
            else:
                return 'decrease' in compare

        return not has_decreasing(sign)

    @staticmethod
    def match(sign):
        for symbol, allowed in zip(sign, HandshapeS.options):
            if symbol not in allowed:
                return False

        # Constraint 4 and 5 are relaxed
        return all([HandshapeS.satisfy_const1(sign), HandshapeS.satisfy_const2(sign), HandshapeS.satisfy_const3(sign)])

        #return all([HandshapeS.satisfy_const1(sign), HandshapeS.satisfy_const2(sign), HandshapeS.satisfy_const3(sign),
        #            HandshapeS.satisfy_const4(sign), HandshapeS.satisfy_const5(sign)])


class HandshapeA(object):
    options = [
        ['U'], ['='], ['e', 'E'], ['H', 'E', 'e', 'i'],
        ['fr'], ['d', 'p', '-'], [NULL], ['/'], ['r'], ['p'], ['1'], ['-'], ['-'], ['-'],
        ['1'], ['F', 'f'], ['F'], ['F', 'f', 'i', 'e', 'E'],
        ['='], ['2'], ['F', 'f'], ['F'], ['F', 'f', 'i', 'e', 'E'],
        ['='], ['3'], ['F', 'f'], ['F'], ['F', 'f', 'i', 'e', 'E'],
        ['='], ['4'], ['F', 'f'], ['F', 'f'], ['F', 'f', 'i', 'e', 'E']
    ]

    def __init__(self):
        super().__init__()

    # constraint1: option[3] and option[5]: option[5] can't be "p" or "-" when option[3] is "i"
    @staticmethod
    def satisfy_const1(sign):
        if (sign[3], sign[5]) in [('i', 'p'), ('i', '-')]:
            return False
        else:
            return True

    # constraint2: option[15] and option[17]: option[17] cannot be "E" or "e" in option[15] is "f"
    @staticmethod
    def satisfy_const2(sign):
        if (sign[15], sign[17]) in [('f', 'E'), ('f', 'e')]:
            return False
        else:
            return True

    # constraint3: option[20] and option[22]: option[22] cannot be "E" or "e" in option[20] is "f"
    @staticmethod
    def satisfy_const3(sign):
        if (sign[20], sign[22]) in [('f', 'E'), ('f', 'e')]:
            return False
        else:
            return True

    # constraint4: option[25] and option[27]: option[27] cannot be "E" or "e" in option[25] is "f"
    @staticmethod
    def satisfy_const4(sign):
        if (sign[25], sign[27]) in [('f', 'E'), ('f', 'e')]:
            return False
        else:
            return True

    # constraint5: option[30] and option[32]: option[32] cannot be "E" or "e" in option[30] is "f"
    @staticmethod
    def satisfy_const5(sign):
        if (sign[30], sign[32]) in [('f', 'E'), ('f', 'e')]:
            return False
        else:
            return True

    @staticmethod
    def match(sign):
        for symbol, allowed in zip(sign, HandshapeA.options):
            if symbol not in allowed:
                return False

        return all([HandshapeA.satisfy_const1(sign), HandshapeA.satisfy_const2(sign), HandshapeA.satisfy_const3(sign),
                    HandshapeA.satisfy_const4(sign), HandshapeA.satisfy_const5(sign)])
