from analysis.unmarked_handshapes import (HandshapeAny, HandshapeEmpty, HandshapeC, Handshape1, HandshapeS, HandshapeA,
                                          HandshapeB2)
from analysis.transcription_search import check_global_options, check_config_type, check_hand_type

handshape_mapping = {'O': HandshapeAny,
                     '1': Handshape1,
                     'B1': HandshapeAny,
                     'A': HandshapeA,
                     'S': HandshapeS,
                     'C': HandshapeC,
                     '5': HandshapeAny,
                     'B2': HandshapeB2,
                     'any': HandshapeAny,
                     'empty': HandshapeEmpty}

def handshape_search(corpus, forearm, estimated, uncertain, incomplete, config, hand, logic, c1h1, c1h2, c2h1, c2h2):
    """
    Run handshape search and return a list of signs in the corpus that match the specifications
    :param corpus: the loaded corpus
    :param forearm: Yes, No, Either
    :param estimated: Yes, No, Either
    :param uncertain: Yes, No, Either
    :param incomplete: Yes, No, Either
    :param config: One-config signs, Two-config signs, Either
    :param hand: One-hand signs, Two-hand signs, Either
    :param logic: Any of the above configurations, All of the above configurations
    :param c1h1: a list of handshape --- O, 1, B, A, S, C, 5, B
    :param c1h2: a list of handshape --- O, 1, B, A, S, C, 5, B
    :param c2h1: a list of handshape --- O, 1, B, A, S, C, 5, B
    :param c2h2: a list of handshapt --- O, 1, B, A, S, C, 5, B
    :return: a list of signs that match the criteria
    """
    ret = list()
    for word in corpus:
        if not check_global_options(word, (forearm, estimated, uncertain, incomplete)):
            continue

        if not check_config_type(word, config):
            continue

        if not check_hand_type(word, hand):
            continue

        if not check_handshape(word, logic, c1h1, c1h2, c2h1, c2h2):
            continue

        ret.append(word)

    return ret


def check_handshape(sign, logic, c1h1, c1h2, c2h1, c2h2):
    sign_c1h1 = [slot if slot else '_' for slot in sign.config1hand1[1:]]
    sign_c1h2 = [slot if slot else '_' for slot in sign.config1hand2[1:]]
    sign_c2h1 = [slot if slot else '_' for slot in sign.config2hand1[1:]]
    sign_c2h2 = [slot if slot else '_' for slot in sign.config2hand2[1:]]

    if logic == 'Any of the above configurations':
        return any([any([handshape_mapping[shape]().match(sign_c1h1) for shape in c1h1]),
                    any([handshape_mapping[shape]().match(sign_c1h2) for shape in c1h2]),
                    any([handshape_mapping[shape]().match(sign_c2h1) for shape in c2h1]),
                    any([handshape_mapping[shape]().match(sign_c2h2) for shape in c2h2])])
    else:  # logic == 'All of the above configurations'
        return all([any([handshape_mapping[shape]().match(sign_c1h1) for shape in c1h1]),
                    any([handshape_mapping[shape]().match(sign_c1h2) for shape in c1h2]),
                    any([handshape_mapping[shape]().match(sign_c2h1) for shape in c2h1]),
                    any([handshape_mapping[shape]().match(sign_c2h2) for shape in c2h2])])
