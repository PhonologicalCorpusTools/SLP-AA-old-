import csv
import os
import numpy as np
import xlwt

parts_list = ["All","Forearm","Thumb","Thumb / Finger Contact","Index Finger","Middle Finger","Ring Finger","Pinky Finger","Thumb / Finger Surfaces","Finger Contact","Extensions","Finger 1 Extensions","Finger 2 Extensions","Finger 3 Extensions","Finger 4 Extensions","Finger / Finger Contact","Proximal Joints","Medial Joints","Distal Joints","ALL summary of 1-19"]
conf_list = ["Config-1 Hand-1","Config-1 Hand-2","Config-2 Hand-1","Config-2 Hand-2"]



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


def reliability_analysis_diff1(basedict, compareddict,word,row,pathname):
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

            if '*' in dict1_compare_list and dict2_compare_list:
                dict1_compare_list=list(filter(lambda a: a != "*", dict1_compare_list))
                dict2_compare_list=list(filter(lambda a: a != "*", dict2_compare_list))
            
            ws.write(row,6,float((1-np.mean(np.array(dict1_compare_list) != np.array(dict2_compare_list)))*100))
            row += 1
        row += 0
    return row




elif get_choice == 1:

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


elif get_choice == 2:

    wb = xlwt.Workbook()
    folderpath, filepath, filearray = initializeReadMultiple();
    base_dict = readMyFile(filepath)

    ws = wb.add_sheet("ALL DATA")
    
    ex_row = 0
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
        ex_row += 0

    rower = 0
    for word in base_dict.keys():
        for path in filearray:
            compared_dict = readMyFile(path)
            alt_path = path
            alt_path = alt_path.split('/')
            alt_path = alt_path[2].split('.')
            alt_path = alt_path[0]
            rower = reliability_analysis_diff1(base_dict, compared_dict,word,rower,alt_path)
            

            

        
save_filename = input("What would you like to call this file?: ")
wb.save(folderpath+save_filename + '.xls')
