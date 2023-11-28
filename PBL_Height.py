 # -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 14:32:10 2021
Last Updated: 9/19/2023 - 09:15PST


This is the user interface program for the PBL algorithm
that:
    -Reads and parces GRAWMET profiles into the program
    -Analyzses the PBL using methods:
        -VPT
        -RI
        -PT
    -Calculates atmospheric conditions
    -Determines proper PBL method based on conditions
    -Creates analysis reports
        -printed version in console
        -Printed version in text file (easy to read)
        -CSV version to allow easy data transfer to other programs
        
     
NOTE: this programs location MUST be in the same folder as "readGrawProfile_alg" 
and "AlgorithmFunctions"folder to load subprograms properly   
     
This program has been developed for the use of the NASA-ISGC 
for the purposes of the National Eclipse Ballooning Project
author: Chambers,Alex
contact: chambers.alexander00@gmail.com

This program has been updated to remove erroneous row data based on the column
specified by the user. It now creates a new file with suffix of "_Cleaned" to 
indicate the data has been modified by the program. UI has been added to allow 
user to choose which columns they would like cleaned.
Author: Samantha Smith
Contact: sasm3709@gmail.com
"""
# =============================================================================
# Libraries
# =============================================================================
import os
import time
import readGrawProfile_alg as rgp
import AlgorithmFunctions as af
import numpy as np
from tkinter import *
import pandas as pd

# =============================================================================
# Function to save column values chosen by user
# =============================================================================
# def obtain_clean_columns():                                                                 #Not Necessary?
#     for x in range(19):
#         if ButtonLoopVal[x].get():
#             #print(ButtonLoopName[x])
#             boxesChecked[x] = 1;
#     root.destroy();
 
# =============================================================================
# Display UI for user to select columns
# =============================================================================
# root = Tk()                                                                         # Need to Make It Look Pretty!
# root.geometry('500x900')

# boxesChecked = [None]*19;

# w = Label(root, text ='Select columns you want to clean:', font = "50") 
# w.pack()
  
# ButtonLoop = [None] * 19
# ButtonLoopName = ["Time","UTCTime","P","T","Hu","Ws","Long",
#                   "Lat","Alt","Geopot","MRI","RI","Dewp","VirtTemp",
#                   "Rs","Elevation","Azimuth","Range","D"];
# ButtonLoopVal = [None]*19;

# for x in range(19):
#    ButtonLoopVal[x] = IntVar();
#    clean_button = Checkbutton(root, text = ButtonLoopName[x], 
#                           variable = ButtonLoopVal[x],
#                           onvalue = 1,
#                           offvalue = 0,
#                           height = 2,
#                           width = 10,
#                           anchor = 'w')
#    clean_button.pack(anchor = 'w')
   
# finish_button = Button(text = "Clean these columns!",
#                        command = obtain_clean_columns)
# finish_button.pack(side = 'bottom')

# mainloop()


# =============================================================================
# Setup Text File Names if Saving
# =============================================================================
site = input("Enter Site Location: ")

pblTxtName = "PBLMethods_%s" %(site)
algTxtName = "PBL_AlgorithumResults_%s" %(site)

pblCsvName = "PBLMethodsCSV_%s"%(site)
algCsvName = "PBL_AlgorithumCSV_%s"%(site)


# =============================================================================
# Data UI
# =============================================================================
start_time = time.time()
dataSource = rgp.getUserInputFile("Select path to data input directory: ")
saveData   = rgp.getUserInputTF("Do you want to save output data?")

if saveData:
    savePrompt = rgp.getUserInputTF("Save to same directory?")
    if savePrompt: 
        savePath = dataSource
    elif saveData:
        savePath = rgp.getUserInputFile("Enter path to data output directory:")
    else:
        savePath = "NA"
else:
    savePath = "NA"
    
output1 = []
output2 = []
millsOutput = []

# =============================================================================
# Clean Data Based on Column Selection
# =============================================================================
for path, subdirs,files, in os.walk(dataSource):
    for file in os.listdir(path):
        try:
            raw_file = open(path+"/"+file,"r")
            raw_header = "";

            for x in range(19):
                if x == 0:
                    raw_header = raw_header + raw_file.readline().strip();
                else:
                    raw_header = raw_header + "\n" + raw_file.readline().strip();
                    
            raw_footer = "";                                                        # Construct Footer

            for line in (raw_file.readlines() [-10:]):
                raw_footer = raw_footer + line; 
                                
            raw_file = open(path+"/"+file,"r")                                      # Construct Data File from Raw Data File
            raw_data = pd.read_csv(raw_file, sep = '\t', skiprows = 18);
            raw_data.drop(raw_data.tail(10).index,inplace = True);
            
            raw_data.rename(columns={'Time               '     : 'Time',            # Change the names of column headers to something reasonable
                                     'UTC Time                ': 'UTC Time',
                                     'P                      ' : 'P', 
                                     'T                     '  : 'T',
                                     'Hu '                     : 'Hu',
                                     'Ws                 '     : 'Ws',
                                     'Wd '                     : 'Wd',
                                     'Long.        '           : 'Long.',
                                     'Lat.     '               : 'Lat.',
                                     'Alt  '                   : 'Alt',
                                     'Geopot     '             : 'Geopot',
                                     'MRI       '              : 'MRI',
                                     'RI     '                 : 'RI',
                                     'Dewp.         '          : 'Dewp.',
                                     'Virt. Temp '             : 'Virt. Temp',
                                     'Rs   '                   : 'Rs',
                                     'Elevation'               : 'Elevation',
                                     'Azimuth '                : 'Azimuth',
                                     'Range'                   : 'Range',
                                     'D'                       : 'D'},
                            inplace=True);
 
            # p = 1;                                                                  # Filter out relevant columns
            # for x in range(19):
            #      if ButtonLoopVal[x].get() == 1:
            #          p = p and (raw_data[ButtonLoopName[x]].str.contains('- ') == False);
   
            # raw_data2 = raw_data[p];
            
        
           
            raw_data2 = raw_data[
                (raw_data['Ws'].str.contains('- ') == False) &
                (raw_data['Alt'].str.contains('- ') == False) &
                (raw_data['P'].str.contains('- ') == False)
                ];
      
            
            raw_file.close()                                                        # Close file - Reading is Finished

            clean_file = open(path+"/"+file[:-4]+"_Cleaned.txt","w")                # Create New Identifiable Output File For Writing

            np.savetxt(clean_file,raw_data2, header = raw_header,
                       fmt = '%s', comments = '');

            clean_file.writelines(raw_footer)
               
            clean_file.close();
        except:                                                                     # If There is an Error Reading the File
            print("I am a failure")


# =============================================================================
# Calculate Results on Cleaned Files
# =============================================================================
for path, subdirs,files, in os.walk(dataSource):
    for file in os.listdir(path):
        if file.endswith("_Cleaned.txt"):                                           # Only Run Files That Have Been Cleaned
            try:
                profile = rgp.readProfile(dataSource,subdirs,path,file)
                if profile is not None:
                    data = profile[0]
                    saveName = profile[2]
                    datetime = profile[3]
                    RunProgram = af.operations(data,saveName)
                    PBLResults= af.Selection(RunProgram)
                    TotalResults = af.fullOutput(datetime,RunProgram,output1,
                                                 output2,saveName,PBLResults)
                    mills = af.mills700(data,millsOutput,saveName)
                    profile2 = 1
            except:                                                                 
                print("Error Running " +saveName)
                pass  
      

# =============================================================================
# Output to Console If Calculations Worked
# =============================================================================
if profile2 is not None:
    Results = af.printConsole(TotalResults,savePath)
    if saveData:
        fileNames = [pblTxtName,algTxtName,pblCsvName,algCsvName]
        textfiles = af.saveTxt(TotalResults,savePath,fileNames)
        mills = np.array(mills)
        np.savetxt("%s/900millsLR"%(savePath),mills,fmt='%s',delimiter=",",
                   encoding="utf-8")      
        print("Data Saved")

print("\n----- Program operated in %.5s seconds / %.5s minutes -------" 
      %((time.time()-start_time),(time.time()-start_time)/60))
del start_time,output1,output2



    
    
    



    
    
    
    
    
    
    
    
    
    
