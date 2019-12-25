import re
from constants import RE_SYMBOLS
from pprint import pprint


def match_flag(sign_list, search_list):
    search = list()
    for flag in search_list:
        if flag == 1:  #True
            search.append({True})
        elif flag == -1:  # False
            search.append({False})
        else:  # Either
            search.append({True, False})

    for sign_flag, search_flags in zip(sign_list, search):
        if sign_flag not in search_flags:
            return False
    else:
        return True


def check_estimate_flag(sign, config1, config2):
    # word.flags['config1hand1'][0][0] is isUncertain
    # word.flags['config1hand1'][0][1] is isEstimate
    c1h1 = config1[0]  # a tuple of dictionary
    c1h2 = config1[1]
    c2h1 = config2[0]
    c2h2 = config2[1]

    sign_c1h1_estimate = [sign.flags['config1hand1'][i][1] for i in range(1, 34)]
    sign_c1h2_estimate = [sign.flags['config1hand2'][i][1] for i in range(1, 34)]
    sign_c2h1_estimate = [sign.flags['config2hand1'][i][1] for i in range(1, 34)]
    sign_c2h2_estimate = [sign.flags['config2hand2'][i][1] for i in range(1, 34)]

    search_c1h1_estimate = [slot['flag_estimate'] for slot in c1h1]
    search_c1h2_estimate = [slot['flag_estimate'] for slot in c1h2]
    search_c2h1_estimate = [slot['flag_estimate'] for slot in c2h1]
    search_c2h2_estimate = [slot['flag_estimate'] for slot in c2h2]

    return all([match_flag(sign_c1h1_estimate, search_c1h1_estimate),
                match_flag(sign_c1h2_estimate, search_c1h2_estimate),
                match_flag(sign_c2h1_estimate, search_c2h1_estimate),
                match_flag(sign_c2h2_estimate, search_c2h2_estimate)])


def check_uncertain_flag(sign, config1, config2):
    # word.flags['config1hand1'][0][0] is isUncertain
    # word.flags['config1hand1'][0][1] is isEstimate
    c1h1 = config1[0]  # a tuple of dictionary
    c1h2 = config1[1]
    c2h1 = config2[0]
    c2h2 = config2[1]

    sign_c1h1_estimate = [sign.flags['config1hand1'][i][0] for i in range(1, 34)]
    sign_c1h2_estimate = [sign.flags['config1hand2'][i][0] for i in range(1, 34)]
    sign_c2h1_estimate = [sign.flags['config2hand1'][i][0] for i in range(1, 34)]
    sign_c2h2_estimate = [sign.flags['config2hand2'][i][0] for i in range(1, 34)]

    search_c1h1_estimate = [slot['flag_uncertain'] for slot in c1h1]
    search_c1h2_estimate = [slot['flag_uncertain'] for slot in c1h2]
    search_c2h1_estimate = [slot['flag_uncertain'] for slot in c2h1]
    search_c2h2_estimate = [slot['flag_uncertain'] for slot in c2h2]

    return all([match_flag(sign_c1h1_estimate, search_c1h1_estimate),
                match_flag(sign_c1h2_estimate, search_c1h2_estimate),
                match_flag(sign_c2h1_estimate, search_c2h1_estimate),
                match_flag(sign_c2h2_estimate, search_c2h2_estimate)])


def check_config_type(sign, config):
    typ = find_config_type(sign)
    if config == 'Either':
        return True
    else:
        return typ == config


def find_config_type(sign):
    c1h1 = ''.join([slot if slot else '_' for slot in sign.config1hand1])
    c1h2 = ''.join([slot if slot else '_' for slot in sign.config1hand2])
    c2h1 = ''.join([slot if slot else '_' for slot in sign.config2hand1])
    c2h2 = ''.join([slot if slot else '_' for slot in sign.config2hand2])

    if (c1h1 == '_______∅/______1____2____3____4___' and c1h2 == '_______∅/______1____2____3____4___') \
            or (c2h1 == '_______∅/______1____2____3____4___' and c2h2 == '_______∅/______1____2____3____4___'):
        typ = 'One-config signs'
    else:
        typ = 'Two-config signs'

    return typ


def check_hand_type(sign, hand):
    typ = find_hand_type(sign)
    if hand == 'Either':
        return True
    else:
        return typ == hand


def find_hand_type(sign):
    c1h1 = ''.join([slot if slot else '_' for slot in sign.config1hand1])
    c1h2 = ''.join([slot if slot else '_' for slot in sign.config1hand2])
    c2h1 = ''.join([slot if slot else '_' for slot in sign.config2hand1])
    c2h2 = ''.join([slot if slot else '_' for slot in sign.config2hand2])

    if (c1h1 == '_______∅/______1____2____3____4___' and c2h1 == '_______∅/______1____2____3____4___')\
            or (c1h2 == '_______∅/______1____2____3____4___' and c2h2 == '_______∅/______1____2____3____4___'):
        typ = 'One-hand signs'
    else:
        typ = 'Two-hand signs'

    return typ


def check_global_options(sign, options):
    sign_specifications = [sign.forearm, sign.estimated, sign.uncertain, sign.incomplete]

    option_specifications = list()
    for option in options:
        if option == 'Yes':
            option_specifications.append({True})
        elif option == 'No':
            option_specifications.append({False})
        else:  #'Either'
            option_specifications.append({True, False})

    ret = all([sign_spec in option_spec for sign_spec, option_spec in zip(sign_specifications, option_specifications)])
    return ret


def check_slot_symbol(word, config1, config2):
    c1h1 = config1[0]  # a tuple of dictionary
    c1h2 = config1[1]
    c2h1 = config2[0]
    c2h2 = config2[1]

    c1h1_slots = '.'.join([slot if slot else '_' for slot in word.config1hand1[1:]])
    c1h2_slots = '.'.join([slot if slot else '_' for slot in word.config1hand2[1:]])
    c2h1_slots = '.'.join([slot if slot else '_' for slot in word.config2hand1[1:]])
    c2h2_slots = '.'.join([slot if slot else '_' for slot in word.config2hand2[1:]])

    re_c1h1 = re.compile('^' + generate_hand_re(c1h1) + '$')
    re_c1h2 = re.compile('^' + generate_hand_re(c1h2) + '$')
    re_c2h1 = re.compile('^' + generate_hand_re(c2h1) + '$')
    re_c2h2 = re.compile('^' + generate_hand_re(c2h2) + '$')

    #print('====================')
    #print(c1h1_slots)
    #print(re_c1h1)
    #print('====================')
    #print(c1h2_slots)
    #print(re_c1h2)
    #print('====================')
    #print(c2h1_slots)
    #print(re_c2h1)
    #print('====================')
    #print(c2h2_slots)
    #print(re_c2h2)
    #print('====================')

    return all([bool(re_c1h1.match(c1h1_slots)),
                bool(re_c1h2.match(c1h2_slots)),
                bool(re_c2h1.match(c2h1_slots)),
                bool(re_c2h2.match(c2h2_slots))])


def generate_slot_re(allowed_set):
    pattern = '(?:' + '|'.join([RE_SYMBOLS[s] if s in RE_SYMBOLS else s for s in allowed_set]) + ')'
    return pattern


def generate_hand_re(hand_slots):
    pattern = r'\.'.join([generate_slot_re(slot['allowed']) for slot in hand_slots])
    return pattern


def check_coder(sign, coders):
    return sign.coder in coders


def check_lastUpdated(sign, lastUpdateds):
    return sign.lastUpdated in lastUpdateds


def transcription_search(corpus, forearm, estimated, uncertain, incomplete, configuration, hand,
                         frequency_range, config1, config2, coders, lastUpdateds):
    '''
    :param corpus: the loaded corpus
    :param forearm: Yes, No, Either
    :param estimated: Yes, No, Either
    :param uncertain: Yes, No, Either
    :param incomplete: Yes, No ,Either
    :param configuration: One-config signs, Two-config signs, Either
    :param hand: One-hand signs, Two-hand signs, Either
    :param config1: a dictionary of information
    :param config2: a dictionary of information
    :return: a list of signs matching the criteria
    '''

    ret = list()
    for word in corpus:
        #print(word)
        if word.frequency not in frequency_range:
            continue

        if not check_global_options(word, (forearm, estimated, uncertain, incomplete)):
            #print('global')
            continue

        if not check_config_type(word, configuration):
            #print('config')
            continue

        if not check_hand_type(word, hand):
            #print('hand')
            continue

        if not check_estimate_flag(word, config1, config2):
            #print('estimate')
            continue

        if not check_uncertain_flag(word, config1, config2):
            #print('uncertain')
            continue

        if not check_slot_symbol(word, config1, config2):
            #print('slot')
            #print(word)
            continue

        if not check_coder(word, coders):
            continue

        if not check_lastUpdated(word, lastUpdateds):
            continue

        ret.append(word)

    #print(ret)
    return ret