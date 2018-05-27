import csv
import os
import numpy as np

parts_list = ["All","Forearm","Thumb","Thumb / Finger Contact","Index Finger","Middle Finger","Ring Finger","Pinky Finger","Thumb / Finger Surfaces","Finger Contact","Extensions","Finger 1 Extensions","Finger 2 Extensions","Finger 3 Extensions","Finger 4 Extensions","Finger / Finger Contact","Proximal Joints","Medial Joints","Distal Joints","ALL summary of 1-19"]
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
        csvReader = csv.reader(csvDataFile, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
        next(csvReader)
        for row in csvReader:
            front_removed = row[5:]
            both_removed = front_removed
            if len(both_removed) == 151:
                both_removed = both_removed[:len(front_removed)-7]
                both_removed = split_arr_fourths(both_removed)
                word_dict[row[0]]=both_removed
            if len(both_removed) == 150:
                both_removed.append("*")
                both_removed = both_removed[:len(front_removed)-7]
                both_removed = split_arr_fourths(both_removed)
                word_dict[row[0]]=both_removed
            if len(both_removed) > 151:
                both_removed = both_removed[:151]
                both_removed = both_removed[:len(front_removed)-7]
                both_removed = split_arr_fourths(both_removed)
                word_dict[row[0]]=both_removed
            else:
                continue
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
            word_val = input("Type in the word you'd like to compare (Not case-sensitive): ")
            word_val = word_val.upper()
            dict1[word_val]
            dict2[word_val]
            break
        except KeyError:
            print("Word is not located in one or both excel sheets.")
    print("\n")

    print("Choose from 4 types of combinations below")
    numb0 = 0
    combined_list0 = ""
    for elem in conf_list:
        numb0 += 1
        combined_list0 += str(numb0)+". "+elem
        if numb0 != 4:
            combined_list0 += "\n"
    print(combined_list0)
    config_val = weird_function("1-4")
    config_val -=1
    print("\n")
    
    print("Type in a value from 1-20 for the reliability statistic you'd like to view")
    numb = 0
    combined_list = ""
    for elem in parts_list:
        numb +=1
        combined_list += str(numb)+ ". "+ elem
        if numb != 20:
            combined_list += "\n"
            
    print(combined_list)
    part_val = weird_function("1-20")
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

    print("Word: ",word_ch)
    print("Configuration: ",conf_list[config_ch])
    print("\n")
    
    mutated_arr1 = ["*"] + mutate_constants(dict1[word_ch][config_ch])
    mutated_arr2 = ["*"] + mutate_constants(dict2[word_ch][config_ch])

    if part_ch >=1 and part_ch <= 19:
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

        print("Section: ",parts_list[part_ch-1]) 
        print("Reliability = ", (1-np.mean(np.array(dict1_compare_list) != np.array(dict2_compare_list)))*100,"%")
    elif part_ch == 20:
        combined_print = ""
        for part in range(1,len(parts_list)):
            range_list = get_range(part)
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

            combined_print += "Section: "+parts_list[part-1]+"\n"+ "Reliability = "+ str((1-np.mean(np.array(dict1_compare_list) != np.array(dict2_compare_list)))*100)+"%"+"\n"+"\n"
        print(combined_print)
            

    print("\n")
    print("Do you want to search another word?")
    print("1. Yes")
    print("2. No")
    do_exit = weird_function("1-2")

    if do_exit == 1:
        print("\n" * 80)
        reliability_analysis(dict1,dict2)
    elif do_exit == 2:
        exit(0)
    






first_dict = readMyFile('Sample/export_ASL.csv')
second_dict = readMyFile('Sample/export_ASL copy.csv')
reliability_analysis(first_dict,second_dict)




