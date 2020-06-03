#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 06:19:35 2020

@author: rikeem
"""

import pandas as pd
import csv
import datetime

def data_converter(file_path = "/home/rikeem/Desktop/CAL_09232019_143311_raw.txt"):

    data = open(file_path)
    csv_data = csv.reader(data)
    csv_lst = []
    #Removes only the relevant data from the csv (Tag ID) and writes in to a list
    for row in csv_data:
        for word in row:
            if word[0] == "*":
                csv_lst.append(row)
    
    #List comprehension that seperates out each individual piece of the string and imports it into a column of the dataframe
    new = [sub.split() for subl in csv_lst for sub in subl]
    df = pd.DataFrame(new, columns=["F_value_1", "F_value_2", "Tag_ID", "Date", "Time"])
    
    #Rearrange columns into desired configuration
    df = df[['Date', 'Time' , 'Tag_ID', 'F_value_1', 'F_value_2']]
    
   #Removes asterisks from first F value column
    df['F_value_1'] = df['F_value_1'].str.replace(r"*", "")
    
    #Converts date into accepted format
    df["Date"] = pd.to_datetime(df.Date)
    df["Date"] = df["Date"].dt.strftime("%m/%d/%Y")
    
    #Generates a text file
    df.to_csv(r"/home/rikeem/Desktop/PIT_Tag_script_output.txt", header=None, index=None, sep=' ', mode='a')
    print(df)
    return(df)

data_converter()



