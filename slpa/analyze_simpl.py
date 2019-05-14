import csv
import os
import numpy as np
import xlwt

parts_list = ["All","Forearm","Thumb","Thumb / Finger Contact","Index Finger","Middle Finger","Ring Finger","Pinky Finger","Thumb / Finger Surfaces","Finger Contact","Extensions","Finger 1 Extensions","Finger 2 Extensions","Finger 3 Extensions","Finger 4 Extensions","Finger / Finger Contact","Proximal Joints","Medial Joints","Distal Joints"]
conf_list = ["Config-1 Hand-1","Config-1 Hand-2","Config-2 Hand-1","Config-2 Hand-2"]
choice_list =["Compare all files in folder to a base file (Save and show in excel sheet)","Combine all files to base file to be able to plug into R"]


def delete_last_two(arr):
    # delete last two items of the items from the list of configs on the very end
    return arr[:int(len(arr)-2)]
    
def split_arr_fourths(arr):
    # split the array into the 4 separate configurations 
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


def readMyFile(filename):

    word_config_dict = dict()

    #read each row of the excel file 
    with open(filename,encoding='ISO-8859-1') as csvDataFile:
        csvReader = csv.reader(csvDataFile, skipinitialspace=True,delimiter=',', quoting=csv.QUOTE_NONE)
        next(csvReader)

        rows_not_included = 0
        
        for row in csvReader:
            #if row length is 155, remove the front and back extra data
            if len(row) == 155:
                both_removed = row[5:len(row)-7]
                both_removed = split_arr_fourths(both_removed)
                word_config_dict[row[0].upper()] = both_removed

            #if row length is not 155, skip the row
            elif len(row) != 155:
                rows_not_included += 1
                continue
        #print number of rows that are not properly included 
        if rows_not_included != 0:
            print(str(rows_not_included)+" rows not included")

    return word_config_dict


    

def initializeReadMultiple():
    #Adds the metadata sheet in the excel file
    ws1 = wb.add_sheet("METADATA")

    #Stores the filepath's inside list_of_folders
    list_of_folders = (next(os.walk('Sample'))[1])


    #Prints out all the files inside a folder
    folder_counter = 0
    concat_list1 = ""
    for folder in list_of_folders[:-1]:
        folder_counter += 1
        concat_list1 += str(folder_counter) + '.' + folder + "\n"
    folder_counter += 1
    concat_list1 += str(folder_counter) + '.' + folder
    print(concat_list1)


    #Goes into a certain folder
    folderbaseindex = input("Please choose a folder of excel files you'd like to compare: ")
    folderbaseindex = int(folderbaseindex)-1
    folder_name = list_of_folders[folderbaseindex]

    
    #Filter's out the non-xls files
    list_of_files = os.listdir("Sample/"+folder_name)
    list_of_files=list(filter(lambda a: a[0] != '.', list_of_files))
    list_of_files=list(filter(lambda a: a[-4:] != '.xls', list_of_files))

    
    file_counter = 0
    concat_list = ""
    for file in list_of_files[:-1]:

        file_counter += 1
        concat_list += str(file_counter) + '.' + file + "\n"
    file_counter += 1
    concat_list += str(file_counter) + '.' + file


    print(concat_list)
    filebaseindex = input("Please choose a base file to compare to: ")
    filebaseindex = int(filebaseindex)-1

    filebasepath = "Sample/"+folder_name+"/"+list_of_files[filebaseindex]


    #Adding metadata on to the first page on the sheet
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

#Print out all the choices from the choice
def print_choices():
    choice_ind = 0
    
    print("Would you like to:")
    for choice in choice_list:
        choice_ind += 1
        print(str(choice_ind)+". "+choice)
        

def valid_choice_getter(inte):
    placeh_val = 0

    while(placeh_val not in range(1,inte+1)):
        try:
            placeh_val = int(input("Choose a number from "+"1-"+str(inte)+": "))
        except ValueError:
            print("That wasn't a valid input.")
        
    return placeh_val

def mutate_constants(arr):
    print(arr)
    presetlist = [8,9,16,21,26,31]
    presetlist[:] = [x - 1 for x in presetlist]
    for indexn in presetlist:
        arr[indexn] = "@"
    return arr



def reliability_analysis_diff(basedict, compareddict,word,column,pathname):
    ex_row1 = 0
    for config in range(0,len(conf_list)):
        ws.write(ex_row1,column,pathname)
        mutated_arr1 = ["@"] + mutate_constants(basedict[word][config])
        mutated_arr2 = ["@"] + mutate_constants(compareddict[word][config])
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
        
#Print all the choices and put them in a list form
print_choices()

#Gets a valid choice from the user input
get_choice = valid_choice_getter(len(choice_list))


#Gets the data in a human-readable format
#This means that each tab is a word
# And each tab shows the 4 configs and their reliability analysis
if get_choice == 1:

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
                ex_row += 1
                ws.write(ex_row,ex_col,part)
            ex_row += 2
        ex_col += 1
        ex_row = 0
        
        for path in filearray:
            compared_dict = readMyFile(path)
            alt_path = path
            alt_path = alt_path.split('/')
            #Changed to -1 instead of 2
            alt_path = alt_path[-1].split('.')
            alt_path = alt_path[0]
            reliability_analysis_diff(base_dict, compared_dict,word,ex_col,alt_path)
            ex_col +=1

    save_filename = input("What would you like to call this file?: ")
    wb.save(folderpath+save_filename + '.xls')

#Gets the data in a file and put it in an R compatible format
elif get_choice == 2:

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
    while collapse_val != "done":
        collapse_val = input("Please enter the values you would like to collapse. \nSeparate the values you want to collpase with a / \nAn example would be \"e/E\" \nEnter here(or type \'done\'):")
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
