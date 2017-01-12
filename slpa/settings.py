import os
from PyQt5.QtCore import QSettings

class Settings(object):

    key_to_ini = {'storage': ('storage/directory',os.path.normpath(os.path.join(
                                            os.path.expanduser('~/Documents'),'SLP-A','Annotator')))}

    def __init__(self):
        self.qs = QSettings("SLP-A","Sign Language Phonetic Annotator")
        self.check_storage()

    def error_directory(self):
        return os.path.join(self['storage'], 'ERRORS')

    def log_directory(self):
        return os.path.join(self['storage'], 'LOG')

    def feature_directory(self):
            return os.path.join(self['storage'], 'FEATURE')

    def check_storage(self):
        if not os.path.exists(self['storage']):
            os.makedirs(self['storage'])
        LOG_DIR = self.log_directory()
        ERROR_DIR = self.error_directory()
        TMP_DIR = os.path.join(self['storage'],'TMP')
        CORPUS_DIR = os.path.join(self['storage'],'CORPUS')
        FEATURE_DIR = os.path.join(self['storage'],'FEATURE')
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
        if not os.path.exists(ERROR_DIR):
            os.mkdir(ERROR_DIR)
        if not os.path.exists(TMP_DIR):
            os.mkdir(TMP_DIR)
        if not os.path.exists(CORPUS_DIR):
            os.mkdir(CORPUS_DIR)
        if not os.path.exists(FEATURE_DIR):
            os.mkdir(FEATURE_DIR)