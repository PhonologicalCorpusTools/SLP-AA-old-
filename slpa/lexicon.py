#from slpa import __version__ as currentSLPAversion
from collections import OrderedDict
from random import choice
from parameters import defaultParameterTree, defaultParameters
from parameterwidgets import ParameterTreeModel

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
                setattr(self, attr, default_value)
        self.basic_attributes = Corpus.basic_attributes[:]

    @property
    def notes(self):
        return self.corpusNotes

    def __len__(self):
        return len(self.wordlist)

    def __contains__(self, item):
        if hasattr(item, 'gloss'):
            return item.gloss in self.wordlist
        else:
            return item in self.wordlist

    def __getitem__(self, key):
        return self.wordlist[key]

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
                       'flags': {'config1hand1':[False for n in range(34)], 'config1hand2':[False for n in range(34)],
                                 'config2hand1':[False for n in range(34)], 'config2hand2':[False for n in range(34)]},
                       'signNotes': str(),
                       'forearmInvolved': False,
                       'partialObscurity': False,
                       'uncertainCoding': False,
                       'incompleteCoding': False
                       }

    sorted_attributes = ['gloss', 'config1', 'config2', 'parameters', 'flags', 'notes']

    headers = ['gloss',
                'config1hand1', 'config1hand2',
                'config2hand1', 'config2hand2',
                'parameters']

    for config_num in [1, 2]:
        for hand_num in [1, 2]:
            for slot_num in range(1, 35):
                headers.append('config{}hand{}slot{}'.format(config_num,hand_num, slot_num))
    headers = ','.join(headers)

    def __init__(self, kwargs):
        for attribute, default_value in Sign.sign_attributes.items():
            try:
                setattr(self, attribute, kwargs[attribute])
            except KeyError:
                setattr(self, attribute, default_value)

        self.config1hand1, self.config1hand2 = self.config1
        self.config2hand1, self.config2hand2 = self.config2

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

    def data(self):
        return OrderedDict([(key,getattr(self, key)) for key in Sign.sorted_attributes])

    def export(self, include_fields=True, blank_space = '_', x_in_box=X_IN_BOX, null=NULL):
        output = list()
        for key,value in self.data().items():

            if 'config' in key:
                for hand in value:
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
                continue

            if key == 'major':
                value = 'None' if not value else value
            elif key == 'minor':
                value = 'None' if not value else value
            elif key  == 'oneHandMovement':
                value = 'None' if not value else value
            elif key == 'twoHandMovement':
                value = 'None' if not value else value
            elif key == 'dislocation':
                value = 'None' if not value else value
            elif key == 'orientation':
                value = 'None' if not value else value
            output.append(value)

        for config_num in [1,2]:
            for hand_num in [0,1]:
                slot_list = getattr(self, 'config{}'.format(config_num))[hand_num]
                for slot_num in range(34):
                    symbol = slot_list[slot_num]
                    if symbol == X_IN_BOX:
                        symbol = x_in_box
                    if symbol == NULL:
                        symbol = null
                    output.append(symbol)
        output = ','.join(output)

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