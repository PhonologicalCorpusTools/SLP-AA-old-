import os
import sys

path = r'C:\Users\Scott\Documents\GitHub\SLP-Annotator\media'
files = [f for f in os.listdir(path) if f.endswith('.png')]

with open(r'c:\users\scott\documents\github\slp-annotator\slpa.qrc', mode='w') as f:
    print('<!DOCTYPE RCC><RCC version="1.0">\n<qresource>', file=f)
    for file in files:
        line = ''.join(['<file>', 'media/', file, '</file>'])
        print(line, file=f)
    print('</qresource>\n</RCC>', file=f)
    
