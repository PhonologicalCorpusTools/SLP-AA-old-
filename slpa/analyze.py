import csv
import os
import numpy as np
import xlwt

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

def initializeReadTwoFiles():


    list_of_files = os.listdir("Sample")
    list_of_files=list(filter(lambda a: a[0] != '.', list_of_files))

    print(list_of_files)

    
    file_counter = 0
    concat_list = ""
    for file in list_of_files:
        file_counter += 1
        concat_list += str(file_counter) + '.' + file + "\n"



    print(concat_list)

    fileindex1 = input("Choose a number for your first file: ")
    fileindex2 = input("Choose a number for your second file: ")

    fileindex1 = int(fileindex1)-1
    fileindex2 = int(fileindex2)-1

    filepath1 = "Sample/" + list_of_files[fileindex1]
    filepath2 = "Sample/" + list_of_files[fileindex2]

    return filepath1, filepath2

def initializeReadMultiple():
    ws1 = wb.add_sheet("METADATA")

    list_of_folders = (next(os.walk('Sample'))[1])
    folder_counter = 0
    concat_list1 = ""
    for folder in list_of_folders:
        folder_counter += 1
        concat_list1 += str(folder_counter) + '.' + folder + "\n"
    print(concat_list1)
    folderbaseindex = input("Please choose a folder of excel files you'd like to compare: ")
    folderbaseindex = int(folderbaseindex)-1
    folder_name = list_of_folders[folderbaseindex]

    
    list_of_files = os.listdir("Sample/"+folder_name)
    list_of_files=list(filter(lambda a: a[0] != '.', list_of_files))
    list_of_files=list(filter(lambda a: a[-4:] != '.xls', list_of_files))

    file_counter = 0
    concat_list = ""
    for file in list_of_files:
        file_counter += 1
        concat_list += str(file_counter) + '.' + file + "\n"


    print(concat_list)
    filebaseindex = input("Please choose a base file to compare to: ")
    filebaseindex = int(filebaseindex)-1

    filebasepath = "Sample/"+folder_name+"/"+list_of_files[filebaseindex]
    
    ws1.write(0,0,"Current Folder Selected:")
    ws1.write(1,0,"Base Dictionary File Compared to:")
    ws1.write(3,0,"All Other Files Compared:")

    ws1.write(0,1,folder_name)
    ws1.write(1,1,list_of_files[filebaseindex])
    
    list_of_files.remove(list_of_files[filebaseindex])

    ex_row=2
    for file in list_of_files:
        ex_row +=1
        ws1.write(ex_row,1,file)
        
    
    list_of_files = ["Sample/"+folder_name+"/"+path for path in list_of_files]

    folderpath = "Sample/"+folder_name+"/"

    

    return folderpath, filebasepath, list_of_files
    


#returns a dictionary with word and a list of 4 elements with all configs and hands
def readMyFile(filename):
    
    word_dict = dict()
    with open(filename,encoding='ISO-8859-1') as csvDataFile:
        csvReader = csv.reader(csvDataFile, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
        next(csvReader)
        for row in csvReader:
            front_removed = row[5:]
            both_removed = front_removed
            if len(both_removed) == 151:
                both_removed = both_removed[:len(front_removed)-7]
                both_removed = split_arr_fourths(both_removed)
                word_dict[row[0].upper()]=both_removed
            if len(both_removed) == 150:
                both_removed.append("*")
                both_removed = both_removed[:len(front_removed)-7]
                both_removed = split_arr_fourths(both_removed)
                word_dict[row[0].upper()]=both_removed
            if len(both_removed) > 151:
                both_removed = both_removed[:151]
                both_removed = both_removed[:len(front_removed)-7]
                both_removed = split_arr_fourths(both_removed)
                word_dict[row[0].upper()]=both_removed
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



def reliability_analysis_diff(basedict, compareddict,word,column,pathname):
    ex_row1 = 0
    for config in range(0,len(conf_list)):
        ws.write(ex_row1,column,pathname)
        mutated_arr1 = ["*"] + mutate_constants(basedict[word][config])
        mutated_arr2 = ["*"] + mutate_constants(compareddict[word][config])
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
            ex_row1 += 1
            ws.write(ex_row1,column,float((1-np.mean(np.array(dict1_compare_list) != np.array(dict2_compare_list)))*100))
        ex_row1 += 2


def reliability_analysis_diff1(basedict, compareddict,word,row,pathname,colist):
    for config in range(0,len(conf_list)):
        mutated_arr1 = ["*"] + mutate_constants(basedict[word][config])
        mutated_arr2 = ["*"] + mutate_constants(compareddict[word][config])
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

            for index in range(len(dict1_compare_list)):
                for pair in colist:
                    if ((dict1_compare_list[index] == pair[0]) & (dict2_compare_list[index] == pair[1])) or ((dict1_compare_list[index] == pair[1]) & (dict2_compare_list[index] == pair[0])):
                        dict1_compare_list[index] == "*"
                        dict2_compare_list[index] == "*"
                        
                

            if '*' in dict1_compare_list and dict2_compare_list:
                dict1_compare_list=list(filter(lambda a: a != "*", dict1_compare_list))
                dict2_compare_list=list(filter(lambda a: a != "*", dict2_compare_list))
            
            ws.write(row,6,float((1-np.mean(np.array(dict1_compare_list) != np.array(dict2_compare_list)))*100))
            row += 1
        row += 0
    return row
        


print("Would you like to: \n1. Compare two values (Print and show in command line) \n2. Compare all files in folder to a base file (Save and show in excel sheet) \n3. Combine all files to base file to be able to plug into R")
get_choice = weird_function("1-3")

if get_choice == 1:
    filepath1,filepath2 = initializeReadTwoFiles()
    first_dict = readMyFile(filepath1)
    second_dict = readMyFile(filepath2)
    reliability_analysis(first_dict,second_dict)
elif get_choice == 2:

    wb = xlwt.Workbook()
    folderpath, filepath, filearray = initializeReadMultiple();
    base_dict = readMyFile(filepath)

    for word in base_dict.keys():
        ex_col = 0
        ex_row = 0

        ws = wb.add_sheet(word)
        
        for config in conf_list:
            ws.write(ex_row,ex_col,config)
            for part in parts_list:
                if part != "ALL summary of 1-19":
                    ex_row += 1
                    ws.write(ex_row,ex_col,part)
            ex_row += 2
        ex_col += 1
        ex_row = 0
        
        for path in filearray:
            compared_dict = readMyFile(path)
            alt_path = path
            alt_path = alt_path.split('/')
            alt_path = alt_path[2].split('.')
            alt_path = alt_path[0]
            reliability_analysis_diff(base_dict, compared_dict,word,ex_col,alt_path)
            ex_col +=1

    save_filename = input("What would you like to call this file?: ")
    wb.save(folderpath+save_filename + '.xls')

elif get_choice == 3:

    wb = xlwt.Workbook()
    folderpath, filepath, filearray = initializeReadMultiple();
    base_dict = readMyFile(filepath)

    ws = wb.add_sheet("ALL DATA")

    header_list = ["Folder","Word","Configuration","Part","Base File","Compared Files","Result"]
    header_col=0
    for word in header_list:
        ws.write(0,header_col, word)
        header_col += 1

    ex_row = 1
    for word in base_dict.keys():
        for path in filearray:
            for config in conf_list:
                for part in parts_list:
                    ex_col = 0
                    if part != "ALL summary of 1-19":
                        ws.write(ex_row,ex_col,folderpath)
                        ex_col += 1
                        ws.write(ex_row,ex_col,word)
                        ex_col += 1
                        ws.write(ex_row,ex_col,config)
                        ex_col += 1
                        ws.write(ex_row,ex_col,part)
                        ex_col += 1
                        ws.write(ex_row,ex_col,filepath)
                        ex_col += 1
                        ws.write(ex_row,ex_col,path)
                        ex_row += 1
                        
    collapse_list = []
    collapse_val =""
    while collapse_val != "quit":
        collapse_val = input("Please enter the values you would like to collapse. \nSeparate the values you want to collpase with a / \nAn example would be \"e/E\" \nEnter here(or type \'quit\'):")
        if (len(collapse_val)==3) & (collapse_val[1]=="/"):
            collapse_list.append(collapse_val.split("/"))
            print("\n")
        else:
            print("Input is in incorrect format, please try again.\n")


    
    rower = 1
    for word in base_dict.keys():
        for path in filearray:
            compared_dict = readMyFile(path)
            alt_path = path
            alt_path = alt_path.split('/')
            alt_path = alt_path[2].split('.')
            alt_path = alt_path[0]


            
            rower = reliability_analysis_diff1(base_dict, compared_dict,word,rower,alt_path,collapse_list)
            

            

        
    save_filename = input("What would you like to call this file?: ")
    wb.save(folderpath+save_filename + '.xls')


        
        
