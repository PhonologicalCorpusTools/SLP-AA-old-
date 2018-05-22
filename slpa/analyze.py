import csv
import numpy as np
def delete_last_two(arr):
    return arr[:int(len(arr)-2)]
    
def split_arr_fourths(arr):
    config1hand1 = []
    config1hand2 = []
    config2hand1 = []
    config2hand2 = []

    config1hand1 = arr[0:int(len(arr)/4)]
    config1hand2 = arr[int(len(arr)/4):int(2*len(arr)/4)]
    config2hand1 = arr[int(2*len(arr)/4):int(3*len(arr)/4)]
    config2hand2 = arr[int(3*len(arr)/4):int(len(arr))]

    config1hand1 = delete_last_two(config1hand1)
    config1hand2 = delete_last_two(config1hand2)
    config2hand1 = delete_last_two(config2hand1)
    config2hand2 = delete_last_two(config2hand2)
    
    return [config1hand1,config1hand2,config2hand1,config2hand2]

#returns a dictionary with word and a list of 4 elements with all configs and hands
def readMyFile(filename):
    word_dict = dict()
    with open(filename,encoding='utf-8') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        next(csvReader)
        
        for row in csvReader:
            front_removed = row[5:]
            both_removed = front_removed[:len(front_removed)-7]
            both_removed = split_arr_fourths(both_removed)
            word_dict[row[0]]=both_removed
    return word_dict

def mutate_constants(arr):
    presetlist = [8,9,16,21,26,31]
    presetlist[:] = [x - 1 for x in presetlist]
    for indexn in presetlist:
        arr[indexn] = "*"
    return arr

def weird_function(rangestr):

    range_arr = rangestr.split("-")
    proto_val = 0
    while int(range_arr[0]) > proto_val or int(range_arr[1]) < proto_val:
        try:
            proto_val = int(input("Choose a number from"+" "+rangestr+":"+" "))
        except ValueError:
            print("That wasn't a valid input")

    return proto_val

def print_options_get_val():
    print("Type in a value from 1-19 for the reliability statistic you'd like to view")
    parts_list = ["All","Forearm","Thumb","Thumb / Finger Contact","Index Finger","Middle Finger","Ring Finger","Pinky Finger","Thumb / Finger Surfaces","Finger Contact","Extensions","Finger 1 Extensions","Finger 2 Extensions","Finger 3 Extensions","Finger 4 Extensions","Finger / Finger Contact","Proximal Joints","Medial Joints","Distal Joints"]
    numb = 0
    for elem in parts_list:
        numb +=1
        print(numb, ".", elem)
    part_val = weird_function("1-19")
    print("\n")

    print("Choose from 4 types of combinations below")
    conf_list = ["Config-1 Hand-1","Config-1 Hand-2","Config-2 Hand-1","Config-2 Hand-2"]
    numb0 = 0
    for elem in conf_list:
        numb0 += 1
        print(numb0, ".", elem)
    config_val = weird_function("1-4")
    print("\n")

    word_val = input

    return part_val

def get_range(numb):
    switcher = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
        13: [],
        14: [],
        15: [],
        16: [],
        17: [],
        18: [],
        19: [],
        
    }
    return switcher.get(argument, "nothing")


# word is word
# config index = [0 for config1hand1] [1 for config1hand2] [2 for config2hand1] [3 for config2hand2]
def reliability_analysis(word,configindex,dict1,dict2):
    mutated_arr1 = mutate_constants(dict1[word][configindex])
    mutated_arr2 = mutate_constants(dict2[word][configindex])
    user_choice = print_options_get_val()

    
    

first_dict = readMyFile('export_ASL.csv')
second_dict = readMyFile('export_ASL copy.csv')
reliability_analysis("1_DOLLAR",0,first_dict,second_dict)

#print(np.mean(np.array(first_dict["1_DOLLAR"][0]) != np.array(second_dict["1_DOLLAR"][0])))
#print(split_arr_fourths(second_dict["1_DOLLAR"]))



