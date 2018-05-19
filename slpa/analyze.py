import csv
import codecs


word_dict = dict()

def readMyFile(filename):
 
    with open(filename,encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader)
        
        for row in csvReader:

            word_dict[row[0]]=row[5:]
            
 
 
readMyFile('export_ASL.csv')

print(word_dict['1_DOLLAR'])
