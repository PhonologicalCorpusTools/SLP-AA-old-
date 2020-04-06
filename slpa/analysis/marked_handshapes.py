from constants import X_IN_BOX, NULL


class HandshapeExtendedU:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '<', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeCIndex:
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeD:
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'i', 'i', 'i',
                 '=', '3', 'i', 'i', 'i',
                 '=', '4', 'i', 'i', 'i')


class HandshapeModifiedG:
    canonical = ('_', 'O', '<', 'E', 'E',
                 'fr', 'M', NULL, '/', '-', 'd', '-', '2', '3', '4',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeCombinedLY:
    canonical = ('_', 'U', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'F', 'i',
                 '<', '3', 'F', 'F', 'i',
                 '<', '4', 'E', 'E', 'E')


class HandshapeK:
    canonical = ('_', 'O', '=', 'E', 'E',
                 'fr', 'd', NULL, '/', 'r', 'p', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeL:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'F')


class HandshapeExtended8:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'E', 'F', 'E',
                 '<', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')


class HandshapeW:
    canonical = ('_', 'O', '<', 'E', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '-', '-', '4',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'F', 'i', 'i')


class HandshapeY:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeClawedF:
    canonical = ('_', 'O', '{', 'E', 'i',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'E', 'F', 'F',
                 '<', '3', 'E', 'F', 'F',
                 '<', '4', 'E', 'F', 'F')

class HandshapeClawedL:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeClawedV:
    canonical = ('_', 'O', '=', 'E', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '<', '3', 'F', 'F', 'F',
                 '<', '4', 'F', 'F', 'F')

class HandshapeCombinedIPlusOne:
    canonical = ('_', 'O', '=', 'E', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '3', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '<', '4', 'E', 'E', 'E')
