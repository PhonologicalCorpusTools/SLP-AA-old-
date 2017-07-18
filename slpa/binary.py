import pickle
import sys
import os

def load_binary(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj

def save_binary(obj, path):
    with open(path,'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

