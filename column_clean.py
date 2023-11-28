import pandas as pd
import numpy as np
import os

# Construct Header

#os.system("temp.py");
raw_file = open(r"C:\Users\sasm3\OneDrive\Desktop\NEBP GIT Code SRC\Data_In\UWY01_1800_071823_POKE1_Profile.txt","r")

raw_header = "";

for x in range(19):
    if x == 0:
        raw_header = raw_header + raw_file.readline().strip();
    else:
        raw_header = raw_header + "\n" + raw_file.readline().strip();

# Construct Footer
raw_footer = "";

for line in (raw_file.readlines() [-10:]):
    raw_footer = raw_footer + line;
  
# Construct Data File from Raw Data File
raw_file = open(r"C:\Users\sasm3\OneDrive\Desktop\NEBP GIT Code SRC\Data_In\UWY01_1800_071823_POKE1_Profile.txt","r")

raw_data = pd.read_csv(raw_file, sep = '\t', skiprows = 18); 
raw_data.drop(raw_data.tail(10).index,inplace = True);

#Change the names of column headers to something reasonable
raw_data.rename(columns={'Time               '     : 'Time',
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

raw_data2 = raw_data[(raw_data['Ws'].str.contains('- ') == False) & (raw_data['Alt'].str.contains('- ') == False)];               #Make a case switch for UI
#raw_file = open(r"C:\Users\sasm3\OneDrive\Desktop\NEBP GIT Code SRC\Data_In\UWY01_1800_071823_POKE1_Profile.txt","r")
#raw_data2 = raw_data[raw_data["Alt"].str.contains("- ") == False];

raw_file.close()

# Write to Output File
clean_file = open(r"C:/Users/sasm3/OneDrive/Desktop/NEBP GIT Code SRC/Data_In/UWY05_0100_082523_POKE2_Profile_OUT.txt","w")

np.savetxt(clean_file,raw_data2, header = raw_header, fmt = '%s', comments = '');

clean_file.writelines(raw_footer)
   
clean_file.close();


 #raw_data2 = raw_data[(raw_data['Ws'].str.contains('- ') == False) &
 #                     (raw_data['Alt'].str.contains('- ') == False)];
 
 # p = (raw_data['Ws'].str.contains('- ') == False)
 # p = p & (raw_data['Alt'].str.contains('- ') == False)
 # raw_data2 = raw_data[p];
 
     
          #  raw_data2 = raw_data[((raw_data['Ws'].str.contains('- ') == False) & boxesChecked[4]) &
          #                       ((raw_data['Alt'].str.contains('- ') == False)& boxesChecked[8])];
            
           
            
           
            
           
            
            #raw_data2 = raw_data[boxesChecked];