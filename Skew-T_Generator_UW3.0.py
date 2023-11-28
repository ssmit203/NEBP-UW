# -*- coding: utf-8 -*-
"""
Author: Alex Chambers / Phil Bergmaier
Date Created: 4/9/2021   
Last Edited: 8/22/2023  1:32 am

ISGC

This program generates Skew-T plots from Grawmet Radiosonde Profile Data

"""
##################################IMPORT ALL MODULES/PACKAGES#######################################
import time
import sys                                            # Used to control entire program (ie. stop run)
import numpy as np                                    # Numbers (like pi) and math
import matplotlib.pyplot as plt                       # Easy plotting
from numpy.core.defchararray import lower             # For some reason I had to import this separately
import os                                             # File reading and input
#import tkinter as tk                                  # Used to create Window Explorer
from tkinter import filedialog, Tk                    # Used to create Window Explorer
from matplotlib.ticker import MultipleLocator
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units
import readGrawProfile_alg_skewt as rgp
import readWyomingProfile_alg_skewt as wyo

readWyoming = False     #if true, program instead reads sounding data downloaded from the U of Wyoming Sounding Archive
windFreq = 75           #frequency with which to plot the wind barbs (e.g., 5 = plot every 5th wind barb)
plot_height = True     #if true, program plots heights (every 1000 m AGL) next to the temperature profile

start_time = time.time()
plt.close("all")


#########FUNCTIONS THE PROGRAM WILL CALL#####
def getUserInputFile(prompt):
    print(prompt)
    main = Tk()    
    userInput = filedialog.askopenfilenames()  # Asks user to choose one or multiple GRAW files to convert
    main.destroy()
    if userInput == "":  # If user cancels or does not select, exit the program
        sys.exit()
    return userInput  # Return the file directory user chos

def getUserInputTF(prompt):
    print(prompt+" (Y/N)")  # Prompts user for a Yes or No
    userInput = ""
    while not userInput:
        userInput = input()
        if lower(userInput) != "y" and lower(userInput) != "n":
            userInput = "Please enter a 'Y' or 'N'"
    if lower(userInput) == "y":
        return True
    else:
        return 
    
def getUserInputFig(prompt):
    print(prompt+"(Y/N)")
    userInput = ""
    while not userInput:
        userInput = input()
        if lower(userInput) != "y" and lower(userInput) != "n":
            userInput = "Please enter a 'Y' or 'N'"
    if lower(userInput) == "y":
            return True
    else:
        return

def SkewTGenerator(data,saveName):
    #Pull specific columns of data relavent to the SkewT
    T = data['T'].values*units.degC                         #make dataframe column with units
    P = data['P'].values*units.hPa
    Td = data['Dewp.'].values*units.degC
    P_wind = P[::windFreq]                                      #use every 400th wind datapoint (gets really cluttered)
    wind_speed = data['Ws'][::windFreq].values*units.knots
    wind_dir = data['Wd'][::windFreq].values*units.degrees
    alt = data['Alt'].values
    u,v = mpcalc.wind_components(wind_speed,wind_dir)
    
    ###Set up Skew T generator
    fig = plt.figure(figsize=(15,15))                       #build figure workspace
    skew = SkewT(fig,rotation=45)                           #call SkewT from the package

    ###Plot the sounding data
    skew.plot(P,T,'r',linewidth=2)                          #plot environmental temperature
    skew.plot(P,Td,'blue',linewidth=2)                      #plot environmental dewpoint
    skew.plot_barbs(P_wind,u,v,y_clip_radius=0,
                    x_clip_radius=0.04,xloc=1.05)           #plot environmental wind barbs
    
    ###Format the x- anx y-axes
    skew.ax.grid(color='black',alpha=0.5)                   #changes the color of the isobars and isotherms    
    skew.ax.set_ylim(1050,100)                              #set y-limits
    skew.ax.yaxis.set_major_locator(MultipleLocator(50))    #show isobars every 50 mb
    for label in skew.ax.yaxis.get_ticklabels()[::2]:       #label every other isobar
        label.set_visible(False)
    skew.ax.set_xlim(-40,50)                                #set x-limits
    skew.ax.set_ylabel('Pressure (mb)')                     #rename the y-axis
    skew.ax.set_xlabel('Temperature (°C)')                  #rename the x-axis
    #skew.ax.grid(axis='both',linestyle='')                 #uncomment to determine which axes are shown
    
    ###Format thedry adiabats, moist adiabats, and mixing ratio lines
    skew.plot_dry_adiabats(units.K * np.arange(223.15,473.15,10),linestyle='solid',linewidth=1)
    #skew.plot_dry_adiabats(units.K * np.arange(223.15,473.15,1),linestyle='solid',linewidth=0.5,alpha=0.25)  
    skew.plot_moist_adiabats(units.Quantity(np.arange(-45, 55, 5), 'degC'),colors='g',linestyle='solid',linewidth=1)
    #skew.plot_moist_adiabats(units.Quantity(np.arange(-42, 52, 2), 'degC'),colors='g',linestyle='solid',linewidth=1)
    skew.plot_mixing_lines(mixing_ratio=np.array([0.0001,0.0002,0.0004,0.001,0.002,0.004,0.007,0.01,0.016,0.024,0.032,0.044,0.06]),
                           pressure=units.Quantity(np.linspace(400,max(skew.ax.get_ylim())),'mbar'),colors='b',linewidth=0.7,linestyle=(0,(5,5)))
    
    
    ######THIS IS TO ADD ALTITUDE [M] SO YOU CAN START TO GET A CORRELATION######
    if plot_height:
        alt_agl=alt-alt[0]
        alt2plot = np.array([1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000,12000,13000,14000,15000,16000,17000,18000,19000,20000])
        skew.ax.text(T[0]+1.5*units.delta_degC,P[0],'0 m AGL')
        for alt_ind in alt2plot:
            diff = np.absolute(alt_agl-alt_ind) 
            index = diff.argmin()
            if P[index]>=100*units.hPa and diff[index]<10:
                skew.ax.text(T[index]+1.5*units.delta_degC,P[index],str(alt_ind)+' m')       
    
    plt.title(saveName,fontsize=20)         #add a title to the plot

    return

def SkewTGeneratorWyoming(data,saveName):
    #Pull specific columns of data relavent to the SkewT
    T = data['Temp'].values*units.degC                         #make dataframe column with units
    P = data['Pres'].values*units.hPa
    Td = data['Dwpt'].values*units.degC
    P_wind = P[::windFreq]                                        #use every 400th wind datapoint (gets really cluttered)
    wind_speed = data['WindSpd'][::windFreq].values*units.knots
    wind_dir = data['WindDir'][::windFreq].values*units.degrees
    u,v = mpcalc.wind_components(wind_speed,wind_dir)
    
    ###Set up Skew T generator
    fig = plt.figure(figsize=(18,12),dpi=300)                       #build figure workspace   
    skew = SkewT(fig,rotation=45,subplot=(1,1,1))                           #call SkewT from the package

    ###Plot the sounding data
    skew.plot(P,T,'r',linewidth=2)                          #plot environmental temperature
    skew.plot(P,Td,'blue',linewidth=2)                      #plot environmental dewpoint
    skew.plot_barbs(P_wind,u,v,y_clip_radius=0,
                    x_clip_radius=0.04,xloc=1.05)           #plot environmental wind barbs
    
    ###Format the x- anx y-axes
    skew.ax.grid(color='black',alpha=0.5)                   #changes the color of the isobars and isotherms    
    skew.ax.set_ylim(1050,100)                              #set y-limits
    skew.ax.yaxis.set_major_locator(MultipleLocator(50))    #show isobars every 50 mb
    for label in skew.ax.yaxis.get_ticklabels()[::2]:       #label every other isobar
        label.set_visible(False)
    skew.ax.set_xlim(-40,50)                                #set x-limits
    skew.ax.set_ylabel('Pressure (mb)')                     #rename the y-axis
    skew.ax.set_xlabel('Temperature (°C)')                  #rename the x-axis
    #skew.ax.grid(axis='both',linestyle='')                 #uncomment to determine which axes are shown

    skew.plot_dry_adiabats(units.K * np.arange(223.15, 473.15, 10),linestyle='solid',linewidth=1)
    #skew.plot_dry_adiabats(units.K * np.arange(223.15, 473.15, 1),linestyle='solid',linewidth=0.5,alpha=0.25)       
    skew.plot_moist_adiabats(units.Quantity(np.arange(-45, 55, 5), 'degC'),colors='g',linestyle='solid',linewidth=1)
    #skew.plot_moist_adiabats(units.Quantity(np.arange(-42, 52, 2), 'degC'),colors='g',linestyle='solid',linewidth=1)
    skew.plot_mixing_lines(mixing_ratio=np.array([0.0001,0.0002,0.0004,0.001,0.002,0.004,0.007,0.01,0.016,0.024,0.032,0.044,0.06]),
                           pressure=units.Quantity(np.linspace(400,max(skew.ax.get_ylim())),'mbar'),colors='b',linewidth=0.7,linestyle=(0,(5,5)))
    
    return
    
########## FILE RETRIEVAL SECTION ##########
# Need to find all txt files in dataSource directory and iterate over them
dataSource = getUserInputFile(
    "Select path to data input directory: ")  # File directory location
#saveFigFiles = getUserInputFig(
#    "Save Skew-T Plots?")

for file in dataSource:  
    filePath = str(os.path.split(file)[0])
    fileName = str(os.path.split(file)[1])
    if os.path.isfile(file):
        if readWyoming:
            profile = wyo.readProfile(filePath,fileName)
            data = profile[0]                                       #make a dataframe from the retrival subprogram
            saveName = profile[1]                                   #grab the saveName from the retrival subprogram
            makeSkewT = SkewTGeneratorWyoming(data,saveName)               #go to the function to make the skew T
        
        else:
            profile = rgp.readProfile(filePath,fileName)
            data = profile[0]                                       #make a dataframe from the retrival subprogram
            saveName = profile[2]                                   #grab the saveName from the retrival subprogram                          
            if profile is not None:                                     #check to make sure it actually grabbed a REAL profile
                makeSkewT = SkewTGenerator(data,saveName)               #go to the function to make the skew T
                
                
 
print("Finished Analysis of All Files in: %s" % (filePath))
print("\n------ Program operated in %s seconds -------" %(time.time() - start_time))
# 