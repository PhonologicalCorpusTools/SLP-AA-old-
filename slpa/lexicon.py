#from slpa import __version__ as currentSLPAversion
import os, re
from collections import OrderedDict
from random import choice
from parameters import defaultParameterTree, defaultParameters
from parameterwidgets import ParameterTreeModel
from transcriptions import Flag

X_IN_BOX = '\u2327'
NULL = '\u2205'

class Corpus():
    corpus_attributes = {'name': 'corpus', 'wordlist': dict(), '_discourse': None, 'path': None,
                         'specifier': None, 'inventory': None, 'inventoryModel': None, 'has_frequency': True,
                         'has_spelling': False, 'has_wordtokens': False, 'has_audio': False, 'wav_path': None,
                         '_attributes': list(),
                         'corpusNotes': str(),
                         '_version': 0.1#currentSLPAversion
                         }
    basic_attributes = ['spelling', 'transcription', 'frequency']

    def __init__(self, kwargs):
        for attr, default_value in Corpus.corpus_attributes.items():
            try:
                setattr(self, attr, kwargs[attr])
            except KeyError:
                value = self.copyValue(default_value)
                setattr(self, attr, value)
        self.basic_attributes = Corpus.basic_attributes[:]

    def copyValue(self, value):
        if isinstance(value, dict):
            return value.copy()
        elif isinstance(value, list):
            return value[:]
        else:
            return value

    def regExSearch(self, query):
        expressions = [ [query[0], query[1]], [query[2], query[3]] ]
        match_list = list()
        for word in self:
            for config_num, hand_num in [(1,1), (1,2), (2,1), (2,2)]:
                slots = getattr(word, 'config{}hand{}'.format(config_num, hand_num))
                slots = ''.join([slot if slot else '_' for slot in slots])
                regex = re.compile(expressions[config_num - 1][hand_num - 1])
                if regex.match(slots) is None:
                    break
            else:
                match_list.append(word)

        return match_list

    def getWord(self, text):
        return self[text]

    @property
    def notes(self):
        return self.corpusNotes

    def __len__(self):
        return len(self.wordlist)

    def __contains__(self, item):
        if hasattr(item, 'gloss'):
            return item.gloss in self.wordlist
        else:
            return item.upper() in [w.upper() for w in self.wordlist]

    def __getitem__(self, key):
        try:
            word = self.wordlist[key]
        except KeyError:
            try:
                word = self.wordlist[key.upper()]
            except KeyError:
                word = self.wordlist[key.lower()]
                #if this fails, then a KeyError is raised as usual
        return word

    def __iter__(self):
        wordlist = sorted(self.wordlist.keys())
        for item in wordlist:
            yield self.wordlist[item]

    def __repr__(self):
        return 'Corpus object with name "{}"'.format(self.name)

    def addWord(self, hs):
        self.wordlist[hs.gloss] = hs

    def randomWord(self):
        word = choice(list(self.wordlist.keys()))
        return self.wordlist[word]


class Sign():

    sign_attributes = {'gloss': str(), 'config1': None, 'config2': None,
                       'parameters': ParameterTreeModel(defaultParameters),
                       'flags': {'config1hand1':[Flag(False,False) for n in range(34)],
                                 'config1hand2':[Flag(False,False) for n in range(34)],
                                 'config2hand1':[Flag(False,False) for n in range(34)],
                                 'config2hand2':[Flag(False,False) for n in range(34)]},
                       'signNotes': str(),
                       'forearmInvolved': False,
                       'partialObscurity': False,
                       'uncertainCoding': False,
                       'incompleteCoding': False
                       }

    sorted_attributes = ['gloss', 'config1', 'config2',
                         'parameters', 'flags', 'notes']

    headers = ['gloss', 'config1hand1', 'config1hand2', 'config2hand1', 'config2hand2']

    for config_num in [1, 2]:
        for hand_num in [1, 2]:
            for slot_num in range(1, 35):
                headers.append('config{}hand{}slot{}'.format(config_num, hand_num, slot_num))
            headers.append('config{}hand{}uncertain'.format(config_num, hand_num))
            headers.append('config{}hand{}estimated'.format(config_num, hand_num))
    headers.extend(['forearmInvolved','partialObscurity','uncertainCoding', 'incompleteCoding'])
    headers.append('notes')
    headers.append('parameters')
    headers = ','.join(headers)

    def __init__(self, kwargs):
        for attribute, default_value in Sign.sign_attributes.items():
            try:
                setattr(self, attribute, kwargs[attribute])
            except KeyError:
                value = self.copyValue(default_value)
                setattr(self, attribute, value)

        self.config1hand1, self.config1hand2 = self.config1
        self.config2hand1, self.config2hand2 = self.config2

    def copyValue(self, value):
        if isinstance(value, dict):
            return value.copy()
        elif isinstance(value, list):
            return value[:]
        elif isinstance(value, ParameterTreeModel):
            return ParameterTreeModel(defaultParameters)
        else:
            return value

    def __eq__(self, other):
        if not isinstance(other, Sign):
            return False
        else:
            return self.gloss == other.gloss

    def __str__(self):
        return self.gloss

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        return self.__str__()

    @property
    def notes(self):
        return self.signNotes

    def getSlot(self, n):
        return getattr(self, 'slot'+str(n))

    def data(self):
        return OrderedDict([(key, getattr(self, key)) for key in Sign.sorted_attributes])

    def export(self, include_fields=True, blank_space = '_', x_in_box=X_IN_BOX, null=NULL):
        output = list()
        output.append(self.gloss)
        for config_num in [1,2]:
            for hand_num in [1,2]:
                hand = getattr(self, 'config{}hand{}'.format(config_num, hand_num))
                if hand[0] == '_' or not hand[0]:
                    hand[0] = blank_space
                else:
                    hand[0] = 'V'
                transcription = [x if x else blank_space for x in hand]
                transcription[7] = null
                if transcription[19] == X_IN_BOX:
                    transcription[19] = x_in_box
                if transcription[24] == X_IN_BOX:
                    transcription[24] = x_in_box
                if transcription[29] == X_IN_BOX:
                    transcription[29] = x_in_box
                if include_fields:
                    transcription = self.add_fields(transcription)
                output.append(''.join(transcription))
                #continue

        for config_num in [1,2]:
            for hand_num in [1,2]:
                #mini_output = list()
                slot_list = getattr(self, 'config{}hand{}'.format(config_num, hand_num))
                for slot_num in range(34):
                    symbol = slot_list[slot_num]
                    if symbol == X_IN_BOX:
                        symbol = x_in_box
                    if symbol == NULL:
                        symbol = null
                    output.append(symbol)
                # output.append(''.join(mini_output))

                uncertain, estimates = list(), list()
                key_name = 'config{}hand{}'.format(config_num, hand_num)
                for i, flag in enumerate(self.flags[key_name]):
                    if flag.isUncertain:
                        uncertain.append(str(i+1))
                    if flag.isEstimate:
                        estimates.append(str(i+1))
                uncertain = 'None' if not uncertain else '-'.join(uncertain)
                estimates = 'None' if not estimates else '-'.join(estimates)
                output.append(uncertain)
                output.append(estimates)

        output.append('True' if self.forearmInvolved else 'False')
        output.append('True' if self.partialObscurity else 'False')
        output.append('True' if self.uncertainCoding else 'False')
        output.append('True' if self.incompleteCoding else 'False')
        output.append(self.notes)
        parameters = self.parameters.exportXML()
        output.append(parameters)

        output = ','.join(output)

        with open(os.path.join(os.getcwd(), 'output.txt'), mode='w', encoding='utf-8') as f:
            print(output, file=f)

        return output

    def add_fields(self, transcription):
        transcription = '[{}]1[{}]2[{}]3[{}]4[{}]5[{}]6[{}]7'.format(transcription[0],
                                                                     ''.join(transcription[1:5]),
                                                                     ''.join(transcription[5:15]),
                                                                     ''.join(transcription[15:19]),
                                                                     ''.join(transcription[19:24]),
                                                                     ''.join(transcription[24:29]),
                                                                     ''.join(transcription[29:34]))
        return transcription
