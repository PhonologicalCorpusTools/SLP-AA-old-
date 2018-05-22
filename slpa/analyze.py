import csv
import numpy as np

parts_list = ["All","Forearm","Thumb","Thumb / Finger Contact","Index Finger","Middle Finger","Ring Finger","Pinky Finger","Thumb / Finger Surfaces","Finger Contact","Extensions","Finger 1 Extensions","Finger 2 Extensions","Finger 3 Extensions","Finger 4 Extensions","Finger / Finger Contact","Proximal Joints","Medial Joints","Distal Joints"]
conf_list = ["Config-1 Hand-1","Config-1 Hand-2","Config-2 Hand-1","Config-2 Hand-2"]

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

def print_options_get_val(dict1,dict2):

    word_val =""
    while True:
        try:
            word_val = input("Type in the word you'd like to compare: ")
            dict1[word_val]
            dict2[word_val]
            break
        except KeyError:
            print("Word is not located in excel sheet")
    print("\n")

    print("Choose from 4 types of combinations below")
    numb0 = 0
    for elem in conf_list:
        numb0 += 1
        print(numb0, ".", elem)
    config_val = weird_function("1-4")
    config_val -=1
    print("\n")
    
    print("Type in a value from 1-19 for the reliability statistic you'd like to view")
    numb = 0
    for elem in parts_list:
        numb +=1
        print(numb, ".", elem)
    part_val = weird_function("1-19")
    print("\n")

    return word_val, config_val, part_val

def get_range(numb):
    switcher = {
        1: [1,"-",34],
        2: [1],
        3: [2,"-",5],
        4: [6,"-",15],
        5: [17,"-",19],
        6: [20,"-",24],
        7: [25,"-",29],
        8: [30,"-",34],
        9: [6,7,10,11],
        10: [12,"-",15],
        11: [4,5,17,18,19,22,23,24,27,28,29,32,33,34],
        12: [17,18,19],
        13: [22,23,24],
        14: [27,28,29],
        15: [32,33,34],
        16: [20,25,30],
        17: [4,17,22,27,32],
        18: [18,23,28,33],
        19: [5,19,24,29,34]
        
    }
    return switcher[numb]


# word is word
# config index = [0 for config1hand1] [1 for config1hand2] [2 for config2hand1] [3 for config2hand2]
def reliability_analysis(dict1,dict2):
    word_ch, config_ch, part_ch = print_options_get_val(dict1,dict2)
    
    mutated_arr1 = ["*"] + mutate_constants(dict1[word_ch][config_ch])
    mutated_arr2 = ["*"] + mutate_constants(dict2[word_ch][config_ch])


    range_list = get_range(part_ch)
    single_number_list = []

    if (len(range_list) == 3) and ("-" in range_list):
        single_number_list = list(range(range_list[0],range_list[2]+1))
    elif len(range_list) != 0:
        single_number_list = range_list

    dict1_compare_list = []
    dict2_compare_list = []
    for ind in single_number_list:
        dict1_compare_list.append(mutated_arr1[ind])
        dict2_compare_list.append(mutated_arr2[ind])

    if '*' in dict1_compare_list and dict2_compare_list:
        dict1_compare_list=list(filter(lambda a: a != "*", dict1_compare_list))
        dict2_compare_list=list(filter(lambda a: a != "*", dict2_compare_list))
    print("Word: ",word_ch)
    print("Configuration: ",conf_list[config_ch])
    print("Section: ",parts_list[part_ch-1]) 
    print("\n")
    print("Reliability = ", (1-np.mean(np.array(dict1_compare_list) != np.array(dict2_compare_list)))*100,"%")

first_dict = readMyFile('export_ASL.csv')
second_dict = readMyFile('export_ASL copy.csv')
reliability_analysis(first_dict,second_dict)




