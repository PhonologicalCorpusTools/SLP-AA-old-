import regex as re
from pprint import pprint

def run_phonological_search(corpus, query):
    # returned object should be a list: ([words], [matched_part], [token_freq])
    reg_expressions = [[query[0], query[1]],
                       [query[2], query[3]]]

    match_list = tuple()
    for word in corpus:
        for config_num, hand_num in [(1, 1), (1, 2), (2, 1), (2, 2)]:
            slots = getattr(word, 'config{}hand{}'.format(config_num, hand_num))
            slots = ''.join([slot if slot else '_' for slot in slots])
            regex = re.compile(reg_expressions[config_num - 1][hand_num - 1])
            if regex.match(slots) is None:
                break
        else:
            match_list.append(word)

    return match_list


def check_finger_match(word, reg_exps):
    for config_num, hand_num in [(1, 1), (1, 2), (2, 1), (2, 2)]:
        slots = getattr(word, 'config{}hand{}'.format(config_num, hand_num))
        slots = ''.join([slot if slot else '_' for slot in slots])
        for reg_exp in reg_exps:
            reg_exp = re.compile(reg_exp)
            if reg_exp.match(slots):
                return True
    return False


def run_extended_finger_search(corpus, search_mode, relation_logic, finger_config_reg_exps, finger_num_reg_exps):
    finger_config_matches = set()
    finger_num_matches = set()
    for word in corpus:
        match_finger_config = check_finger_match(word, finger_config_reg_exps)
        match_finger_num = check_finger_match(word, finger_num_reg_exps)

        if match_finger_config:
            finger_config_matches.add(word.gloss)

        if match_finger_num:
            finger_num_matches.add(word.gloss)

    if relation_logic == 'Apply both':
        print('=====Apply both=====')
        ret = finger_config_matches & finger_num_matches
        pprint(ret)
    elif relation_logic == 'Apply either':
        print('=====Apply either=====')
        ret = finger_config_matches | finger_num_matches
        pprint(ret)
    elif relation_logic == 'Apply only the finger configuration':
        print('=====Apply only the finger configuration=====')
        pprint(finger_config_matches)
    else:
        print('=====Apply only the number of extended fingers=====')
        pprint(finger_num_matches)


def match_specification(slots, spec):
    finger_config_reg_exps = spec['fingerConfigRegExps']  # a set
    finger_number_reg_exps = spec['fingerNumberRegExps']  # a set
    relation_logic = spec['relationLogic']
    search_mode = spec['searchMode']

    for finger_config_reg_exp in finger_config_reg_exps:
        finger_config_reg_exp = re.compile(finger_config_reg_exp)
        if finger_config_reg_exp.match(slots):
            match_finger_config = True
            break
    else:
        match_finger_config = False

    for finger_number_reg_exp in finger_number_reg_exps:
        finger_number_reg_exp = re.compile(finger_number_reg_exp)
        if finger_number_reg_exp.match(slots):
            match_finger_number = True
            break
    else:
        match_finger_number = False

    if relation_logic == 'Apply both':
        matched = all([match_finger_config, match_finger_number])
    elif relation_logic == 'Apply either':
        matched = any([match_finger_config, match_finger_number])
    elif relation_logic == 'Apply only the finger configuration':
        matched = match_finger_config
    else:  # relation_logic == 'Apply only the number of extended fingers'
        matched = match_finger_number

    if search_mode == 'Positive':
        return matched
    else:
        return not matched


def extended_finger_search(corpus, c1h1, c1h2, c2h1, c2h2, logic):
    # loop through the words in the corpus
    # for each word, find if each hand/configuration matches the specification
    # logic part: if "and", means that all four have to be true
    # if "or", means that only one of them has to be true

    ret = set()
    for word in corpus:
        c1h1_slots = ''.join([slot if slot else '_' for slot in word.config1hand1])
        c1h2_slots = ''.join([slot if slot else '_' for slot in word.config1hand2])
        c2h1_slots = ''.join([slot if slot else '_' for slot in word.config2hand1])
        c2h2_slots = ''.join([slot if slot else '_' for slot in word.config2hand2])

        c1h1_match = match_specification(c1h1_slots, c1h1)
        c1h2_match = match_specification(c1h2_slots, c1h2)
        c2h1_match = match_specification(c2h1_slots, c2h1)
        c2h2_match = match_specification(c2h2_slots, c2h2)

        if logic == 'All four hand/configuration specifications':
            matched = all([c1h1_match, c1h2_match, c2h1_match, c2h2_match])
        else:
            matched = any([c1h1_match, c1h2_match, c2h1_match, c2h2_match])

        if matched:
            ret.add(word.gloss)

    return ret

