import os
from PyQt5.QtCore import QSettings

class Settings(object):

    key_to_ini = {'storage': ('storage/directory',os.path.normpath(os.path.join(
                                            os.path.expanduser('~/Documents'),'SLP-A','Annotator')))}



    def __init__(self):
        self.qs = QSettings("UBC Phonology Tools","Sign Language Phonetic Annotator")
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

    def __getitem__(self, key):

        mapped_key = self.key_to_ini[key]
        if isinstance(mapped_key, list):
            return tuple(type(d)(self.qs.value(k,d)) for k, d in mapped_key)
        else:
            inikey, default = mapped_key
            if key == 'num_cores':
                if self['use_multi']:
                    return type(default)(self.qs.value(inikey,default))
                else:
                    return -1
            else:
                return type(default)(self.qs.value(inikey, default))

    def __setitem__(self, key, value):
        mapped_key = self.key_to_ini[key]
        if isinstance(mapped_key, list):
            if not isinstance(value,list) and not isinstance(value,tuple):
                raise(KeyError)
            if len(mapped_key) != len(value):
                raise(KeyError)
            for i,(k, d) in enumerate(mapped_key):
                self.qs.setValue(k,value[i])
        else:
            inikey, default = mapped_key
            self.qs.setValue(inikey,value)

    def sync(self):
        self.qs.sync()

    def update(self,setting_dict):
        for k,v in setting_dict.items():
            self[k] = v

    def get_storage_settings(self):
        out = {x: self[x] for x in self.storage_setting_keys}
        return out