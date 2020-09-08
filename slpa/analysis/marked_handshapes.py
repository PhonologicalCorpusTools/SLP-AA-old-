from constants import X_IN_BOX, NULL


class HandshapeExtendedU:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeCIndex:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeD:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'i', 'i', 'i',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeG:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeCombinedILY:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'E', 'E', 'E')


class HandshapeK:  #checked
    canonical = ('_', 'O', '=', 'E', 'E',
                 'fr', 'd', NULL, '/', 'r', 'p', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '<', '4', 'F', 'F', 'E')


class HandshapeL:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeExtended8:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'i', 'i', 'i',
                 '<', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')


class HandshapeW:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'd', '-', '-', '-', '4',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '<', '4', 'i', 'i', 'i')


class HandshapeY:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeClawedF:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'E', 'F', 'F',
                 '{', '4', 'E', 'F', 'F')

class HandshapeClawedL:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeClawedV:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeCombinedIPlusOne:  #checked
    canonical = ('_', 'O', '{', 'i', 'F',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '3', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'F', 'F', 'i',
                 '=', '3', 'F', 'F', 'i',
                 '=', '4', 'E', 'E', 'E')


class HandshapeF:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')


class HandshapeI:  #checked
    canonical = ('_', 'O', '=', 'i', 'F',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'E', 'E', 'E')

class HandshapeClawedSpreadC:  #checked
    canonical = ('_', 'O', '{', 'E', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'E', 'F', 'F',
                 '{', '4', 'E', 'F', 'F')

class HandshapeClawedW:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'd', '-', '-', '-', '4',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'E', 'F', 'F',
                 '<', '4', 'i', 'i', 'i')

class HandshapeClosedV:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'i', 'i', 'F',
                 '=', '2', 'i', 'i', 'F',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeClosedW:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'd', '-', '-', '-', '4',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'i', 'i', 'i')


class HandshapeBentI:  #checked
    canonical = ('_', 'O', '=', 'i', 'F',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'E', 'E')


class HandshapeMiddleFinger:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'F', 'F', 'E',
                 '<', '2', 'E', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeOIndex:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeOpenF:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')


class HandshapeClawedExtendedV:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeDoubleCIndex:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '<', '2', 'i', 'i', 'i',
                 '{', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeFlatC:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'E', 'E',
                 '=', '4', 'F', 'E', 'E')


class HandshapeBentThumbL:  #checked
    canonical = ('_', 'L', '{', 'E', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeBentV:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'F', 'E', 'E',
                 '{', '2', 'F', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class Handshape8:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'i', 'i', 'i',
                 '<', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeClawedI:  #checked
    canonical = ('_', 'O', '=', 'i', 'F',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '<', '4', 'E', 'F', 'F')

class HandshapeClosedDoubleModifiedG:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'd', '1', '2', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeDoubleModifiedG:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeCovered8:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'd', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'i', 'i', 'F',
                 '<', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')


class HandshapeSlantedExtendedB:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'i', 'E', 'E',
                 '=', '3', 'i', 'E', 'E',
                 '=', '4', 'i', 'E', 'E')

class HandshapeX:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'E', 'F', 'i',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeExtendedX:  #checked
    canonical = ('_', 'U', '<', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeExtendedC:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'i', 'E',
                 '=', '2', 'E', 'i', 'E',
                 '=', '3', 'E', 'i', 'E',
                 '=', '4', 'E', 'i', 'E')


class HandshapeClosedG:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'd', '1', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeFlatCombinedIPlusOne:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'd', '-', '2', '3', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'E', 'E',
                 '<', '4', 'E', 'E', 'E')


class Handshape3:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeExtendedB:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')


class Handshape4:  #checked
    canonical = ('_', 'O', '=', 'i', 'F',
                 'u', 'd', NULL, '/', 'fr', 'M', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')


class HandshapeOpen8:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'F', 'E', 'E',
                 '<', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeU:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeClawed3:  #checked
    canonical = ('_', 'L', '{', 'E', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')


class HandshapeExtendedA:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'F', 'F',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeR:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 'x', '2', 'E', 'i', 'i',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeV:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeClosedAIndex:  #checked
    canonical = ('_', 'U', '=', 'E', 'E',
                 'fr', 'd', NULL, '/', 'r', 'm', '1', '-', '-', '-',
                 '1', 'i', 'i', 'E',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeAdductedF:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '=', '2', 'E', 'E', 'E',
                 '=', '3', 'E', 'E', 'E',
                 '=', '4', 'E', 'E', 'E')

class HandshapeBentExtendedB:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'E', 'E',
                 '=', '4', 'F', 'E', 'E')

class HandshapeClawedC:  #checked
    canonical = ('_', 'O', '{', 'E', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '<', '2', 'E', 'F', 'F',
                 '<', '3', 'E', 'F', 'F',
                 '<', '4', 'E', 'F', 'F')

class HandshapeCoveredF:  #checked
    canonical = ('_', 'O', '{', 'i', 'F',
                 'fr', 'd', NULL, '/', 'b', 'd', '1', '-', '-', '-',
                 '1', 'F', 'F', 'F',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeN:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'r', 'p', '-', '-', '3', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeT:  #checked
    canonical = ('_', 'O', '=', 'i', 'E',
                 'fr', 'd', NULL, '/', 'r', 'p', '-', '2', '-', '-',
                 '1', 'F', 'F', 'E',
                 '<', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeContractedUIndex:  #checked
    canonical = ('_', 'O', '{', 'E', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '-', '3', '4',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '<', '3', 'i', 'i', 'i',
                 '<', '4', 'i', 'i', 'i')

class HandshapeCrookedW:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'd', '-', '-', '-', '4',
                 '1', 'E', 'i', 'i',
                 '{', '2', 'E', 'i', 'i',
                 '{', '3', 'E', 'i', 'i',
                 '<', '4', 'i', 'i', 'i')

class HandshapeSpreadExtendedC:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'i',
                 '{', '2', 'E', 'F', 'i',
                 '{', '3', 'E', 'F', 'i',
                 '{', '4', 'E', 'F', 'i')

class HandshapeClawedExtendedB:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '=', '2', 'E', 'F', 'F',
                 '=', '3', 'E', 'F', 'F',
                 '=', '4', 'E', 'F', 'F')

class HandshapeCombinedYAndMiddle:  #checked
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'F', 'E',
                 '<', '2', 'E', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '<', '4', 'E', 'E', 'E')

class HandshapeContractedC:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'E', 'E',
                 '=', '2', 'i', 'E', 'E',
                 '=', '3', 'i', 'E', 'E',
                 '=', '4', 'i', 'E', 'E')

class HandshapeE:  #checked
    canonical = ('_', 'O', '=', 'F', 'i',
                 'b', 'd', NULL, '/', 't', 'd', '-', '-', '-', '4',
                 '1', 'i', 'F', 'F',
                 '=', '2', 'i', 'F', 'F',
                 '=', '3', 'i', 'F', 'F',
                 '=', '4', 'i', 'F', 'F')

class HandshapeOpenE:  #checked
    canonical = ('_', 'O', '<', 'F', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '=', '2', 'E', 'F', 'F',
                 '=', '3', 'E', 'F', 'F',
                 '=', '4', 'E', 'F', 'F')

class HandshapeM:  #checked
    canonical = ('_', 'O', '=', 'F', 'i',
                 'fr', 'd', NULL, '/', 'r', 'p', '-', '-', '-', '4',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '<', '4', 'F', 'F', 'E')

class HandshapeBent1:  #checked
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'F', 'E', 'E',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeContracted5:  #checked
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'E', 'E',
                 '{', '2', 'i', 'E', 'E',
                 '{', '3', 'i', 'E', 'E',
                 '{', '4', 'i', 'E', 'E')

class HandshapeSlantedF:  #checked
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'E', 'E', 'i',
                 '{', '3', 'i', 'E', 'E',
                 '{', '4', 'i', 'i', 'E')

class HandshapeOpenA:  #new
    canonical = ('_', 'U', '<', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'i', 'i',
                 '=', '2', 'F', 'i', 'i',
                 '=', '3', 'F', 'i', 'i',
                 '=', '4', 'F', 'i', 'i')

class HandshapeModifiedA:  #new
    canonical = ('_', 'U', '=', 'E', 'E',
                 'fr', 'd', NULL, '/', 'r', 'p', '1', '-', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeBentB:  #new
    canonical = ('_', 'O', '=', 'F', 'i',
                 'b', 'd', NULL, '/', 'fr', 'm', '-', '-', '-', '4',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'E', 'E',
                 '=', '4', 'F', 'E', 'E')

class HandshapeContractedB:  #new
    canonical = ('_', 'O', '=', 'E', 'E',
                 't', 'd', NULL, '/', 'fr', 'm', '-', '2', '-', '-',
                 '1', 'i', 'E', 'E',
                 '=', '2', 'i', 'E', 'E',
                 '=', '3', 'i', 'E', 'E',
                 '=', '4', 'i', 'E', 'E')

class HandshapeCrookedExtendedB:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'i', 'i',
                 '=', '2', 'E', 'i', 'i',
                 '=', '3', 'E', 'i', 'i',
                 '=', '4', 'E', 'i', 'i')

class HandshapeCrookedC:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'i', 'i',
                 '=', '2', 'E', 'i', 'i',
                 '=', '3', 'E', 'i', 'i',
                 '=', '4', 'E', 'i', 'i')


class HandshapeSpreadC:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'i',
                 '{', '2', 'E', 'F', 'i',
                 '{', '3', 'E', 'F', 'i',
                 '{', '4', 'E', 'F', 'i')


class HandshapePartiallyBentD:  #new
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '2', '-', '-',
                 '1', 'i', 'E', 'E',
                 '<', '2', 'i', 'i', 'i',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')


class HandshapeClosedBentD:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 't', 'd', NULL, '/', 't', 'd', '1', '2', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeModifiedD:  #new
    canonical = ('_', 'O', '{', 'i', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '2', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'i', 'i', 'i',
                 '=', '3', 'i', 'i', 'i',
                 '=', '4', 'i', 'i', 'i')

class HandshapeFlatF:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'd', '1', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeFlatOpenF:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeFlatClawedF:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'd', '1', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'E', 'F', 'F',
                 '{', '4', 'E', 'F', 'F')

class HandshapeOffsetF:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'p', NULL, '/', 'r', 'm', '1', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'i', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeModifiedG:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeBentCombinedIPlusOne:  #new
    canonical = ('_', 'O', '=', 'i', 'F',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'E', 'E')

class HandshapeCombinedIPlusA:  #new
    canonical = ('_', 'U', '=', 'E', 'E',
                 'fr', 'd', NULL, '/', 'r', 'p', '1', '-', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'E', 'E', 'E')

class HandshapeExtendedK:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '<', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '<', '4', 'F', 'F', 'E')

class HandshapeBentL:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeContractedL:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'E', 'E',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeDoubleContractedL:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'E', 'E',
                 '=', '2', 'i', 'E', 'E',
                 '<', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeCrookedL:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'i', 'i',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeFlatM:  #new
    canonical = ('_', 'O', '=', 'F', 'i',
                 'fr', 'd', NULL, '/', 'r', 'p', '-', '-', '-', '4',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'E', 'E',
                 '<', '4', 'F', 'F', 'E')

class HandshapeCoveredO:  #new
    canonical = ('_', 'O', '=', 'i', 'E',
                 'u', 'd', NULL, '/', 't', 'd', '-', '-', '3', '-',
                 '1', 'i', 'i', 'i',
                 '=', '2', 'i', 'i', 'i',
                 '=', '3', 'i', 'i', 'i',
                 '=', '4', 'i', 'i', 'i')

class HandshapeFlatO:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'd', '1', '2', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '=', '3', 'F', 'E', 'E',
                 '=', '4', 'F', 'E', 'E')

class HandshapeModifiedO:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'd', NULL, '/', 'fr', 'd', '1', '2', '-', '-',
                 '1', 'F', 'i', 'i',
                 '=', '2', 'F', 'i', 'i',
                 '=', '3', 'F', 'i', 'i',
                 '=', '4', 'F', 'i', 'i')

class HandshapeOffsetO:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 'fr', 'p', NULL, '/', 'r', 'm', '1', '-', '-', '-',
                 '1', 'F', 'i', 'i',
                 '=', '2', 'F', 'i', 'i',
                 '=', '3', 'F', 'i', 'i',
                 '=', '4', 'F', 'i', 'i')

class HandshapeOpenSpreadO:  #new
    canonical = ('_', 'O', '{', 'i', 'i',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '{', '2', 'i', 'i', 'i',
                 '{', '3', 'i', 'i', 'i',
                 '{', '4', 'i', 'i', 'i')

class HandshapeOpenOIndex:  #new
    canonical = ('_', 'O', '{', 'i', 'i',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'i',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeBentR:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'F', 'E', 'E',
                 'x', '2', 'F', 'i', 'i',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeExtendedR:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 'x', '2', 'E', 'i', 'i',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeCoveredT:  #new
    canonical = ('_', 'O', '=', 'E', 'E',
                 't', 'd', NULL, '/', 'fr', 'm', '1', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '<', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeBentU:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeBentExtendedU:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '=', '2', 'F', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeClawedU:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'F', 'F',
                 '=', '2', 'E', 'F', 'F',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeCombinedUAndY:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '=', '2', 'E', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeContractedU:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'i', 'E', 'E',
                 '=', '2', 'i', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeCrookedU:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'i', 'i',
                 '=', '2', 'E', 'i', 'i',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeBentExtendedV:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '{', '2', 'F', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeCrookedV:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'i', 'i',
                 '{', '2', 'E', 'i', 'i',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeCrookedExtendedV:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'i', 'i',
                 '{', '2', 'E', 'i', 'i',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeSlantedV:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'i', 'E', 'E',
                 '<', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'F', 'E')

class HandshapeClosedX:  #new
    canonical = ('_', 'O', '=', 'E', 'E',
                 't', 'd', NULL, '/', 't', 'd', '1', '-', '-', '-',
                 '1', 'E', 'F', 'i',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeModifiedY:  #new
    canonical = ('_', 'O', '<', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'F', 'E',
                 '=', '2', 'F', 'F', 'E',
                 '=', '3', 'F', 'F', 'E',
                 '<', '4', 'E', 'E', 'E')

class HandshapeBentOffset1:  #new
    canonical = ('_', 'O', '=', 'E', 'i',
                 'fr', 'd', NULL, '/', 'u', 'm', '1', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeClawed1:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'E', 'F', 'F',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeCrooked1:  #new
    canonical = ('_', 'O', '=', 'i', 'i',
                 'fr', 'd', NULL, '/', 'b', 'm', '-', '2', '-', '-',
                 '1', 'E', 'i', 'i',
                 '<', '2', 'F', 'F', 'F',
                 '=', '3', 'F', 'F', 'F',
                 '=', '4', 'F', 'F', 'F')

class HandshapeContracted3:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'E', 'E',
                 '{', '2', 'i', 'E', 'E',
                 '{', '3', 'F', 'F', 'E',
                 '=', '4', 'F', 'E', 'E')

class HandshapeBent4:  #new
    canonical = ('_', 'O', '=', 'F', 'i',
                 'b', 'd', NULL, '/', 'fr', 'p', '-', '-', '-', '4',
                 '1', 'F', 'E', 'E',
                 '{', '2', 'F', 'E', 'E',
                 '{', '3', 'F', 'E', 'E',
                 '{', '4', 'F', 'E', 'E')

class HandshapeClawed4:  #new
    canonical = ('_', 'O', '=', 'i', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'E', 'F', 'F',
                 '{', '4', 'E', 'F', 'F')

class HandshapeCrooked4:  #new
    canonical = ('_', 'O', '=', 'i', 'F',
                 'u', 'd', NULL, '/', 'fr', 'M', '-', '-', '3', '-',
                 '1', 'E', 'i', 'i',
                 '{', '2', 'E', 'i', 'i',
                 '{', '3', 'E', 'i', 'i',
                 '{', '4', 'E', 'i', 'i')

class HandshapeSlanted4:  #new
    canonical = ('_', 'O', '=', 'i', 'F',
                 'u', 'd', NULL, '/', 'fr', 'M', '-', '-', '3', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'i', 'i',
                 '{', '3', 'i', 'E', 'E',
                 '{', '4', 'F', 'E', 'E')

class HandshapeBent5:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'F', 'E', 'E',
                 '{', '2', 'F', 'E', 'E',
                 '{', '3', 'F', 'E', 'E',
                 '{', '4', 'F', 'E', 'E')

class HandshapeBentMidfinger5:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'F', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeClawed5:  #new
    canonical = ('_', 'L', '{', 'E', 'F',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'F', 'F',
                 '{', '2', 'E', 'F', 'F',
                 '{', '3', 'E', 'F', 'F',
                 '{', '4', 'E', 'F', 'F')

class HandshapeRelaxedContracted5:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'i', 'i', 'E',
                 '<', '2', 'i', 'i', 'E',
                 '<', '3', 'i', 'i', 'E',
                 '<', '4', 'i', 'i', 'E')

class HandshapeCrooked5:  #new
    canonical = ('_', 'L', '{', 'E', 'i',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'i', 'i',
                 '{', '2', 'E', 'i', 'i',
                 '{', '3', 'E', 'i', 'i',
                 '{', '4', 'E', 'i', 'i')

class HandshapeCrookedSlanted5:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'i', 'i',
                 '{', '2', 'i', 'i', 'i',
                 '{', '3', 'F', 'i', 'i',
                 '{', '4', 'F', 'F', 'i')

class HandshapeModified5:  #new
    canonical = ('_', 'O', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '{', '4', 'E', 'E', 'E')

class HandshapeSlanted5:  #new
    canonical = ('_', 'L', '{', 'E', 'E',
                 '-', '-', NULL, '/', '-', '-', '-', '-', '-', '-',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'i', 'i',
                 '{', '3', 'i', 'E', 'E',
                 '{', '4', 'F', 'E', 'E')

class Handshape6:  #new
    canonical = ('_', 'O', '{', 'E', 'i',
                 't', 'd', NULL, '/', 't', 'd', '-', '-', '-', '4',
                 '1', 'E', 'E', 'E',
                 '{', '2', 'E', 'E', 'E',
                 '{', '3', 'E', 'E', 'E',
                 '<', '4', 'i', 'i', 'i')