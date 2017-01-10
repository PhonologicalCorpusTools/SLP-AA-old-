from slpa import __version__ as currentSLPAversion
import os


class Corpus():
    corpus_attributes = {'name': 'corpus', 'wordlist': dict(), '_discourse': None,
                         'specifier': None, 'inventory': None, 'inventoryModel': None, 'has_frequency': True,
                         'has_spelling': False, 'has_wordtokens': False, 'has_audio': False, 'wav_path': None,
                         '_attributes': list(),
                         '_version': currentSLPAversion
                         }
    basic_attributes = ['spelling', 'transcription', 'frequency']

    def __init__(self, path):
        self.path = path
        self.name = os.path.split(path)[-1]
        self.wordlist = dict()

    def __len__(self):
        return len(self.wordlist)

    def __contains__(self, item):
        return item.gloss in self.wordlist

    def __iter__(self):
        for item in self.wordlist.values():
            yield item

    def addWord(self, hs):
        self.wordlist[hs.gloss] = hs

