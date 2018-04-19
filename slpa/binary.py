import pickle
import anytree

class SLPAUnpickler(pickle._Unpickler):

    def __init__(self, file):
        super().__init__(file)

    def find_class(self, module, name):
        print(module, name)
        if 'anytree' in module:
            print(module, name)
            return getattr(anytree, name)
        else:
            return super().find_class(module, name)

def load_binary(path):
    with open(path, 'rb') as f:
        up = SLPAUnpickler(f)
        #obj = pickle.load(f)
        obj = up.load()
    return obj

def save_binary(obj, path):
    with open(path,'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

