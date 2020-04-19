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


class HandshapeG:
    canonical = ('_', 'O', '<', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
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

class HandshapeF:
    canonical = ('_', 'O', '{', 'E', 'E',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeI:
    canonical = ('_', 'O', '=', 'E', 'E',
                 'fr', 'd', NULL, '/', 'b', 'm', '1', '-', '-', '-',
                 '1', 'F', 'F', 'F',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'E', 'E', 'E')

class HandshapeClawedSpreadC:
    canonical = ('_', 'O', '{', 'E', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'E', 'F', 'F',
                 '{', '4', 'E', 'F', 'F')

class HandshapeClawedW:
    canonical = ('_', 'O', '{', 'E', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '-', '-', '4',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'E', 'F', 'F',
                 '{', '4', 'i', 'i', 'i')

class HandshapeClosedW:
    canonical = ('_', 'O', '=', 'E', 'E',
                 't', 'd', NULL, '/', 't', 'd', '-', '-', '-', '4',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'F', 'F', 'F')


class HandshapeBentI:
    canonical = ('_', 'O', '=', 'E', 'F',
                 '?', 'd', NULL, '/', 'b', 'd', '-', '2', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'E', 'E')


class HandshapeMiddleFinger:
    canonical = ('_', 'O', '{', 'E', 'i',
                 't', 'd', NULL, '/', 'b', 'd', '-', '-', '3', '-',
                 '1', 'E', 'E', 'F',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'F',
                 '=', '4', 'E', 'E', 'F')


class HandshapeOIndex:
    canonical = ('_', 'U', '{', 'E', 'E',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeOpenF:
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '<', '2', 'E', 'E', 'E',
                 '<', '3', 'E', 'E', 'E',
                 '<', '4', 'E', 'E', 'E')


class HandshapeClawedExtendedV:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '<', '2', 'E', 'F', 'F',
                 '<', '3', 'F', 'i', 'i',
                 '=', '4', 'F', 'i', 'i')


class HandshapeDoubleCIndex:
    canonical = ('_', 'U', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'E',
                 '<', '2', 'i', 'i', 'E',
                 '{', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeFlatC:
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')


class HandshapeBentThumbL:
    canonical = ('_', 'U', '{', 'i', 'i',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'E', 'E',
                 '=', '4', 'F', 'E', 'E')


class HandshapeBentV:
    canonical = ('_', 'O', '{', 'E', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'F', 'E', 'E',
                 '{', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class Handshape8:
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'b', 'd', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'F', 'i', 'i',
                 '=', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeClawedI:
    canonical = ('_', 'O', '=', 'F', 'i',
                 'u', 'p', NULL, '/', 'b', 'm', '1', '2', '3', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '<', '4', 'E', 'F', 'F')

class HandshapeClosedDoubleModifiedG:
    canonical = ('_', 'O', '<', 'E', 'E',
                 'fr', 'M', NULL, '/', '-', 'd', '-', '2', '3', '4',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'E', 'E', 'E',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeDoubleModifiedG:
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeCovered8:
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'b', 'd', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'F', 'i', 'i',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')

class HandshapeSlantedB:
    canonical = ('_', 'U', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'i', 'E', 'E',
                 '=', '3', 'i', 'E', 'E',
                 '=', '4', 'i', 'E', 'E')

class HandshapeClawed1:
    canonical = ('_', 'O', '{', 'E', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'E', 'F', 'i',
                 '<', '2', 'i', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeExtendedC:
    canonical = ('_', 'U', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'i',
                 '=', '2', 'E', 'i', 'i',
                 '=', '3', 'E', 'i', 'i',
                 '=', '4', 'E', 'E', 'i')

class HandshapeClosedModifiedG:
    canonical = ('_', 'U', '=', 'E', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'd', '1', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'i', 'i', 'E',
                 '=', '4', 'i', 'i', 'E')

class HandshapeFlatCombinedIPlusOne:
    canonical = ('_', 'O', '=', 'E', 'i',
                 'fr', 'd', NULL, '/', 'b', 'd', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')

class Handshape3:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '=', '3', 'F', 'F', 'i',
                 '=', '4', 'F', 'F', 'i')

class HandshapeExtendedB:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')

class Handshape4:
    canonical = ('_', 'O', '=', 'F', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'M', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'E', 'E', 'E',
                 '<', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')

class HandshapeOpen8:
    canonical = ('_', 'O', '{', 'H', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'F', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeU:
    canonical = ('_', 'O', '=', 'F', 'E',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeClawed3:
    canonical = ('_', 'L', '{', 'E', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '<', '3', 'F', 'F', 'i',
                 '=', '4', 'F', 'F', 'i')

class HandshapeExtendedA:
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'F', 'F',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeR:
    canonical = ('_', 'O', '=', 'E', 'E',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 'x', '2', 'E', 'i', 'i',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeV:
    canonical = ('_', 'O', '{', 'E', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')
