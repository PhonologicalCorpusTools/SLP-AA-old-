import csv
import codecs


word_dict = dict()

def readMyFile(filename):
 
    with open(filename,encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader)
        
        for row in csvReader:
            front_removed = row[5:]
            both_removed = front_removed[:len(front_removed)-7]
            word_dict[row[0]]=both_removed

def split_arr_fourths(arr):
    config1hand1 = []
    config1hand2 = []
    config2hand1 = []
    config2hand2 = []

    config1hand1 = arr[0:int(len(arr)/4)]
    config1hand2 = arr[int(len(arr)/4):int(2*len(arr)/4)]
    config2hand1 = arr[int(2*len(arr)/4):int(3*len(arr)/4)]
    config2hand2 = arr[int(3*len(arr)/4):int(len(arr))]

    return [config1hand1,config1hand2,config2hand1,config2hand2]
    


 
readMyFile('export_ASL.csv')


