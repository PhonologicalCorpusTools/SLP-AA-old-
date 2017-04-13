#from slpa import __version__ as currentSLPAversion
from collections import OrderedDict
X_IN_BOX = '\u2327'

class Corpus():
    corpus_attributes = {'name': 'corpus', 'wordlist': dict(), '_discourse': None,
                         'specifier': None, 'inventory': None, 'inventoryModel': None, 'has_frequency': True,
                         'has_spelling': False, 'has_wordtokens': False, 'has_audio': False, 'wav_path': None,
                         '_attributes': list(),
                         '_version': 0.1#currentSLPAversion
                         }
    basic_attributes = ['spelling', 'transcription', 'frequency']

    def __init__(self, kwargs):
        self.path = kwargs['path']
        self.name = kwargs['name']
        self.wordlist = dict()

    def __len__(self):
        return len(self.wordlist)

    def __contains__(self, item):
        return item.gloss in self.wordlist

    def __getitem__(self, key):
        return self.wordlist[key]

    def __iter__(self):
        wordlist = sorted(self.wordlist.keys())
        for item in wordlist:
            yield self.wordlist[item]

    def addWord(self, hs):
        self.wordlist[hs.gloss] = hs

    def __str__(self):
        return 'Corpus object called "{}"'.format(self.name)


class Sign():

    sign_attributes = ['gloss', 'config1', 'config2', 'major', 'minor', 'movement', 'orientation']

    headers = ['gloss',
                       'config1hand1', 'config1hand2',
                       'config2hand1', 'config2hand2',
                       'major', 'minor',
                       'movement', 'orientation']
    for config_num in [1, 2]:
        for hand_num in [1, 2]:
            for slot_num in range(1, 35):
                headers.append('config{}hand{}slot{}'.format(config_num,hand_num, slot_num))
    headers = ';'.join(headers)

    def __init__(self, data):
        self.attributes = list()
        for key,value in data.items():
            setattr(self, key, value)
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

    def data(self):
        return OrderedDict([(key,getattr(self, key)) for key in Sign.sign_attributes])

    def export(self, include_fields=True, blank_space = '_', x_in_box=X_IN_BOX):
        output = list()
        for key,value in self.data().items():

            if 'config' in key:
                for hand in value:
                    if hand[0]:
                        hand[0] = 'V'
                    else:
                        hand[0] = blank_space
                    transcription = [x if x else blank_space for x in hand]
                    transcription = [t if not t == X_IN_BOX else x_in_box for t in transcription]
                    if include_fields:
                        transcription = self.add_fields(transcription)
                    output.append(''.join(transcription))
                continue

            if key == 'major':
                value = 'None' if not value else value
            elif key == 'minor':
                value = 'None' if not value else value
            elif key == 'orientation':
                value = 'None' if not value else value
            elif key  == 'movement':
                value = 'None' if not value else value
            output.append(value)

        for config_num in [1,2]:
            for hand_num in [0,1]:
                slot_list = getattr(self, 'config{}'.format(config_num))[hand_num]
                for slot_num in range(34):
                    symbol = slot_list[slot_num]
                    if symbol == X_IN_BOX:
                        symbol = x_in_box
                    output.append(slot_list[slot_num])
        output = ';'.join(output)

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