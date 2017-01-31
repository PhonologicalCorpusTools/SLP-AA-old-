#from slpa import __version__ as currentSLPAversion

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

    def __iter__(self):
        for item in self.wordlist.values():
            yield item

    def addWord(self, hs):
        self.wordlist[hs.gloss] = hs

    def __str__(self):
        return 'Corpus object called "{}"'.format(self.name)

