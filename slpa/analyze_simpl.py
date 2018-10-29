import csv
import os
import numpy as np
import xlwt

parts_list = ["All","Forearm","Thumb","Thumb / Finger Contact","Index Finger","Middle Finger","Ring Finger","Pinky Finger","Thumb / Finger Surfaces","Finger Contact","Extensions","Finger 1 Extensions","Finger 2 Extensions","Finger 3 Extensions","Finger 4 Extensions","Finger / Finger Contact","Proximal Joints","Medial Joints","Distal Joints","ALL summary of 1-19"]
conf_list = ["Config-1 Hand-1","Config-1 Hand-2","Config-2 Hand-1","Config-2 Hand-2"]


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
