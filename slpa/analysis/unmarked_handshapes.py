from constants import X_IN_BOX, NULL

ORDER = {'H': 5, 'E': 4, 'e': 3, 'i': 2, 'f': 1, 'F': 0}

def increasing_or_equal_flexion(*args):
    """
    return if the specified finger slots are in increased flexion
    :param args: slots in question
    :return: Boolean: true if all slots are in increased flexion
    """
    # latter - former <= 0 for all pairs
    return all([ORDER[args[i+1]] - ORDER[args[i]] <= 0 for i in range(len(args)-1)])


def is_decreasing_flexion_first(*args):
    """
    return if the first comparison is decreasing for flexion
    :param sign:
    :return:
    """
    # decreasing flexion: latter - former > 0

    for i in range(len(args)-1):
        if ORDER[args[i+1]] - ORDER[args[i]] > 0:
            return True
    else:
        return False


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
        return all([symbol in allowed for symbol, allowed in zip(sign, HandshapeEmpty.options)])


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
        return all([symbol in allowed for symbol, allowed in zip(sign, HandshapeAny.options)])


class Handshape1(object):
    canonical = ('_', 'O', '=', 'f', 'f',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'E', 'E', 'H',
                 '=', '2', 'f', 'f', 'f',
                 '=', '3', 'F', 'f', 'f',
                 '=', '4', 'F', 'f', 'f')

    options = [
        ['O'], ['<', '=', '?'], ['i', 'f', 'F', '?'], ['i', 'f', 'F', '?'],
        ['t', 'fr', '?'], ['d', '?'], [NULL], ['/'], ['b'], ['m', '?'], ['-', '?'], ['2', '?'], ['-', '?'], ['-', '?'],
        ['1'], ['E', 'e'], ['E', 'e'], ['H'],
        ['='], ['2'], ['i', 'f'], ['i', 'f', '?'], ['i', 'f', '?'],
        ['='], ['3'], ['f', 'F'], ['i', 'f', '?'], ['i', 'f', '?'],
        ['='], ['4'], ['f', 'F'], ['i', 'f', '?'], ['i', 'f', '?']
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
        return all([symbol in allowed for symbol, allowed in zip(sign, Handshape1.options)]) and \
               all([Handshape1.satisfy_const1(sign), Handshape1.satisfy_const2(sign), Handshape1.satisfy_const3(sign),
                    Handshape1.satisfy_const4(sign)])


class Handshape5(object):
    # note that for canonical we have one extra slot in the very beginning, which is always '_'
    canonical = ('_', 'L', '{', 'f', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'E', 'E', 'E',
                 '<', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')

    options = [
        ['L', 'U'], ['{'], ['E', 'e', 'f'], ['H', 'E', 'e'],
        ['-'], ['-'], [NULL], ['/'], ['-'], ['-'], ['-'], ['-'], ['-'], ['-'],
        ['1'], ['H', 'E', 'e'], ['H', 'E', 'e'], ['H', 'E', 'e'],
        ['{', '<'], ['2'], ['H', 'E', 'e'], ['H', 'E', 'e'], ['H', 'E', 'e'],
        ['{', '<'], ['3'], ['H', 'E', 'e'], ['H', 'E', 'e'], ['H', 'E', 'e'],
        ['{', '<'], ['4'], ['H', 'E', 'e'], ['H', 'E', 'e'], ['H', 'E', 'e']
    ]

    def __init__(self):
        super().__init__()

    # constraint1: option[2], option[3]: no combination of "e" and "H"
    @staticmethod
    def satisfy_const1(sign):
        return (sign[2], sign[3]) != ('e', 'H')

    @staticmethod
    def match(sign):
        for symbol, allowed in zip(sign, Handshape5.options):
            if symbol not in allowed:
                return False

        return Handshape5.satisfy_const1(sign)


class HandshapeA(object):
    canonical = ('_', 'U', '=', 'e', 'e',
                 'fr', 'd', NULL, '/', 'r', 'p', '1', '-', '-', '-',
                 '1', 'F', 'F', 'F',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

    options = [
        ['U'], ['='], ['E', 'e'], ['H', 'E', 'e', 'i'],
        ['fr'], ['-', 'd', 'p'], [NULL], ['/'], ['r'], ['p'], ['1'], ['-'], ['-'], ['-'],
        ['1'], ['f', 'F'], ['F', '?'], ['E', 'e', 'i', 'f', 'F', '?'],
        ['='], ['2'], ['f', 'F'], ['F', '?'], ['E', 'e', 'i', 'f', 'F', '?'],
        ['='], ['3'], ['f', 'F'], ['F', '?'], ['E', 'e', 'i', 'f', 'F', '?'],
        ['='], ['4'], ['f', 'F'], ['f', 'F', '?'], ['E', 'e', 'i', 'f', 'F', '?']
    ]

    # Add H
    # Add question mark for finger joints

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

    # constraint6: option[17], option[22], option[27]: they cannot be more than two values apart with the adjacent finger,
    # except in between option[27] and option[32]
    @staticmethod
    def satisfy_const6(sign):
        def difference(value1, value2):
            value1 = ORDER[value1]
            value2 = ORDER[value2]
            return abs(value1 - value2)

        if any([symbol == '?' for symbol in [sign[17], sign[22], sign[27]]]):
            return True

        return not (difference(sign[17], sign[22]) > 2 or difference(sign[22], sign[27]) > 2)

    # constraint7: option[17], option[22], option[27], option[32]: they have to have all the same flexion or from index to finger4
    # have an increasing flexion value but not the other way around
    @staticmethod
    def satisfy_const7(sign):
        if any([symbol == '?' for symbol in [sign[17], sign[22], sign[27], sign[32]]]):
            return True

        return increasing_or_equal_flexion(sign[17], sign[22], sign[27], sign[32])

    @staticmethod
    def match(sign):
        return all([symbol in allowed for symbol, allowed in zip(sign, HandshapeA.options)]) and \
               all([HandshapeA.satisfy_const1(sign), HandshapeA.satisfy_const2(sign), HandshapeA.satisfy_const3(sign),
                    HandshapeA.satisfy_const4(sign), HandshapeA.satisfy_const5(sign), HandshapeA.satisfy_const6(sign),
                    HandshapeA.satisfy_const7(sign)])


class HandshapeB1(object):  #B1 = Opposed B (Henner et al., 2013)
    canonical = ('_', 'O', '=', 'i', 'e',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')
    options = [
        ['O'], ['{', '<', '=', '?'], ['H', 'E', 'e', 'i', 'f', 'F', '?'], ['H', 'E', 'e', 'i', 'f', 'F', '?'],
        ['-', 'fr', 'u', '?'], ['-', 'd', '?'], [NULL], ['/'], ['-', 'fr', '?'], ['-', 'p', '?'], ['-', '1', '?'], ['-', '2', '?'], ['-', '3', '?'], ['-', '4', '?'],
        ['1'], ['H', 'E', 'e'], ['H', 'E', 'e'], ['H', 'E', 'e'],
        ['<', '='], ['2'], ['H', 'E', 'e'], ['H', 'E', 'e'], ['H', 'E', 'e'],
        ['<', '='], ['3'], ['H', 'E', 'e', 'i'], ['H', 'E', 'e', 'i'], ['H', 'E', 'e', 'i'],
        ['<', '='], ['4'], ['H', 'E', 'e', 'i'], ['H', 'E', 'e', 'i'], ['H', 'E', 'e', 'i']
    ]

    def __init__(self):
        super().__init__()

    # constraint1: Thumb-finger contact will always be [rd0/fp....] but the finger will co-vary with other values as follows:
    # (a) If there is thumb-finger contact (option[10], option[11], option[12], option[13]), thumb is abducted (option[1]) (i.e., {)
    # (b) If there is thumb-finger contact (option[10], option[11], option[12], option[13]), finger extension is 'e' or 'E'
    # (c) If there is contact with finger 1, the thumb extension is 'e' or 'E'
    # (d) If there is contact with finger 2, the thumb extension is 'e' or 'E'
    # (e) If there is contact with finger 3, the thumb extension is 'i', 'e', or 'E'
    # (f) If there is contact with finger 4, the thumb extension is 'i', 'e', or 'E'
    # (g) Unlikely but for simplicity: [O{EE][ud0/fp---4]

    @staticmethod
    def satisfy_const1(sign):
        # (a)
        if sign[10] == '1' or sign[11] == '2' or sign[12] == '3' or sign[13] == '4':
            if sign[1] != '{':
                return False

        # (b)
        if sign[10] == '1' or sign[11] == '2' or sign[12] == '3' or sign[13] == '4':
            for s in [sign[15], sign[16], sign[17],  # index
                      sign[20], sign[21], sign[22],  # middle
                      sign[25], sign[26], sign[27],  # ring
                      sign[30], sign[31], sign[32]]:  # pinky
                if s not in ['e', 'E']:
                    return False

        # (c)
        if sign[10] == '1':
            for s in [sign[2], sign[3]]:
                if s not in ['e', 'E']:
                    return False

        # (d)
        if sign[11] == '2':
            for s in [sign[2], sign[3]]:
                if s not in ['e', 'E']:
                    return False

        # (e)
        if sign[12] == '3':
            for s in [sign[2], sign[3]]:
                if s not in ['i', 'e', 'E']:
                    return False

        # (f)
        if sign[13] == '4':
            for s in [sign[2], sign[3]]:
                if s not in ['i', 'e', 'E']:
                    return False

        return True

    # constraint2: Across fingers, the values must match with all fingers by one value
    # option[15], [20], [25], [30]
    # option[16], [21], [26], [31]
    # option[17], [22], [27], [32]
    @staticmethod
    def satisfy_const2(sign):
        def difference(value1, value2):
            value1 = ORDER[value1]
            value2 = ORDER[value2]
            return abs(value1 - value2)

        if any([symbol == '?' for symbol in [sign[15], sign[16], sign[17],
                                             sign[20], sign[21], sign[22],
                                             sign[25], sign[26], sign[27],
                                             sign[30], sign[31], sign[32]]]):
            return True

        MCPs = [sign[15], sign[20], sign[25], sign[30]]
        PIPs = [sign[16], sign[21], sign[26], sign[31]]
        DIPs = [sign[17], sign[22], sign[27], sign[32]]

        return all([difference(MCPs[i + 1] - MCPs[i]) <= 1 for i in range(3)]) and \
               all([difference(PIPs[i + 1] - PIPs[i]) <= 1 for i in range(3)]) and \
               all([difference(DIPs[i + 1] - DIPs[i]) <= 1 for i in range(3)])

    @staticmethod
    def match(sign):
        return all([symbol in allowed for symbol, allowed in zip(sign, HandshapeB1.options)]) and \
               all([HandshapeB1.satisfy_const1(sign), HandshapeB1.satisfy_const2(sign)])


class HandshapeB2(object):  #B2 = Plain B (Brentari, 2005)
    canonical = ('_', 'L', '<', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')

    options = [
        ['L', 'U'], ['<', '='], ['E', 'e', 'i'], ['E', 'e', 'i'],
        ['-'], ['-'], [NULL], ['/'], ['-'], ['-'], ['-'], ['-'], ['-'], ['-'],
        ['1'], ['E', 'e', 'i'], ['E', 'e', 'i'], ['E', 'e'],
        ['=', 'x-'], ['2'], ['E', 'e', 'i'], ['E', 'e', 'i'], ['E', 'e'],
        ['=', 'x-'], ['3'], ['E', 'e', 'i'], ['E', 'e', 'i'], ['E', 'e', 'i'],
        ['<', '=', 'x-'], ['4'], ['E', 'e', 'i'], ['E', 'e', 'i'], ['E', 'e']
    ]

    def __init__(self):
        super().__init__()

    # constraint1: option[15], option[20], option[25], option[30]: no [E]...[i], order doesn't matter
    @staticmethod
    def satisfy_const1(sign):
        for s1, s2 in [(sign[15], sign[20]), (sign[15], sign[25]), (sign[15], sign[30]),
                       (sign[20], sign[25]), (sign[20], sign[30]),
                       (sign[25], sign[30])]:
            if (s1, s2) in [('E', 'i'), ('i', 'E')]:
                return False
        else:
            return True

    # constraint2: option[16], option[21], option[26], option[31]: no [E]...[i], order doesn't matter
    @staticmethod
    def satisfy_const2(sign):
        for s1, s2 in [(sign[16], sign[21]), (sign[16], sign[26]), (sign[16], sign[31]),
                       (sign[21], sign[26]), (sign[21], sign[31]),
                       (sign[26], sign[31])]:
            if (s1, s2) in [('E', 'i'), ('i', 'E')]:
                return False
        else:
            return True

    # constraint3: 4([15], [16], [17]), 5([20], [21], [22]), 6([25], [26], [27]), 7([30], [31], [32]): no [E]...[i], order doesn't matter
    @staticmethod
    def satisfy_const3(sign):
        for s1, s2 in [(sign[15], sign[16]), (sign[15], sign[17]), (sign[16], sign[17]),
                       (sign[20], sign[21]), (sign[20], sign[22]), (sign[21], sign[22]),
                       (sign[25], sign[26]), (sign[25], sign[27]), (sign[26], sign[27]),
                       (sign[30], sign[31]), (sign[30], sign[32]), (sign[31], sign[32])]:
            if (s1, s2) in [('E', 'i'), ('i', 'E')]:
                return False
        else:
            return True

    @staticmethod
    def match(sign):
        return all([symbol in allowed for symbol, allowed in zip(sign, HandshapeB2.options)]) and \
               all([HandshapeB2.satisfy_const1(sign), HandshapeB2.satisfy_const2(sign), HandshapeB2.satisfy_const3(sign)])


class HandshapeC(object):
    canonical = ('_', 'O', '<', 'e', 'e',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'e',
                 '=', '2', 'i', 'i', 'e',
                 '=', '3', 'i', 'i', 'e',
                 '=', '4', 'e', 'e', 'e')

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
        return all([symbol in allowed for symbol, allowed in zip(sign, HandshapeC.options)]) and \
               all([HandshapeC.satisfy_const1(sign), HandshapeC.satisfy_const2(sign), HandshapeC.satisfy_const3(sign),
                    HandshapeC.satisfy_const4(sign), HandshapeC.satisfy_const5(sign), HandshapeC.satisfy_const6(sign)])


class HandshapeO(object):
    canonical = ('_', 'O', '{', 'e', 'f',
                 'fr', 'd', NULL, '/', 'fr', 'd', '1', '2', '-', '-',
                 '1', 'f', 'i', 'e',
                 '=', '2', 'f', 'i', 'e',
                 '=', '3', 'f', 'i', 'e',
                 '=', '4', 'e', 'i', 'e')

    options = [
        ['O'], ['{'], ['e', 'i'], ['i', 'f', 'F', '?'],
        ['t', 'fr'], ['d'], [NULL], ['/'], ['t', 'fr'], ['d'], ['-', '1'], ['-', '2'], ['-', '3'], ['-'],
        ['1'], ['i', 'f'], ['i', 'f'], ['e', 'i', 'f', '?'],
        ['=', 'x-'], ['2'], ['i', 'f'], ['i', 'f'], ['e', 'i', 'f', '?'],
        ['=', 'x-'], ['3'], ['i', 'f'], ['i', 'f'], ['e', 'i', 'f', '?'],
        ['=', 'x-'], ['4'], ['e', 'i', 'f'], ['e', 'i'], ['E', 'e', 'i', '?']
    ]

    def __init__(self):
        super().__init__()

    # constraint1: option[2], option[3]: can't be more than two values apart from each other
    @staticmethod
    def satisfy_const1(sign):
        return (sign[2], sign[3]) != ('e', 'F')

    # constraint2: option[10], option[11], option[12]: can't all be '-'
    @staticmethod
    def satisfy_const2(sign):
        return (sign[10], sign[11], sign[12]) != ('-', '-', '-')

    @staticmethod
    def match(sign):
        return all([symbol in allowed for symbol, allowed in zip(sign, HandshapeO.options)]) and \
               all([HandshapeO.satisfy_const1(sign), HandshapeO.satisfy_const2(sign)])


class HandshapeS(object):
    canonical = ('_', 'O', '=', 'i', 'f',
                 'fr', 'd', NULL, '/', 'b', 'm', '1', '2', '-', '-',
                 '1', 'F', 'F', 'F',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

    options = [
        ['O'], ['{', '=', '?'], ['e', 'i', 'f', '?'], ['e', 'i', 'f', 'F', '?'],
        ['fr', 'u', '?'], ['d', '?'], [NULL], ['/'], ['b', '?'], ['m', '?'], ['-', '1', '?'], ['-', '2', '?'], ['-', '3', '?'], ['-', '?'],
        ['1'], ['f', 'F'], ['F', '?'], ['f', 'F', '?'],
        ['='], ['2'], ['f', 'F'], ['F', '?'], ['i', 'f', 'F', '?'],
        ['='], ['3'], ['f', 'F'], ['F', '?'], ['i', 'f', 'F', '?'],
        ['='], ['4'], ['f', 'F'], ['f', 'F', '?'], ['i', 'f', 'F', '?']
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
    # but not decreasing flexion (e.g.: F,f,f,f), decreasing-increasing (e.g.: F,f,f,F) or f, F, f, F.
    @staticmethod
    def satisfy_const4(sign):
        if any([symbol == '?' for symbol in [sign[15], sign[20], sign[25], sign[30]]]):
            return True

        return not is_decreasing_flexion_first(sign[15], sign[20], sign[25], sign[30])

    # constraint5: option[17], option[22], option[27], option[32]: they have to have all the same flexion value (e.g., f,f,f,f),
    # or from thumb to finger 4 have an increasing flexion value (e.g., f, f, F, F, but not the other way around (e.g., F, f, f, i,),
    # or F, f, F, i.
    @staticmethod
    def satisfy_const5(sign):
        if any([symbol == '?' for symbol in [sign[17], sign[22], sign[27], sign[32]]]):
            return True

        return increasing_or_equal_flexion(sign[17], sign[22], sign[27], sign[32])

    @staticmethod
    def match(sign):
        return all([symbol in allowed for symbol, allowed in zip(sign, HandshapeS.options)]) and \
               all([HandshapeS.satisfy_const1(sign), HandshapeS.satisfy_const2(sign), HandshapeS.satisfy_const3(sign)])  # Constraint 4 and 5 are relaxed
