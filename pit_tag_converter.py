#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 06:19:35 2020

@author: rikeem
"""

import pandas as pd
import csv
import os

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
    csv_path = "/home/rikeem/Desktop/PIT_Tag_script_output.txt"
    df.to_csv(csv_path, header=None, index=None, sep=' ', mode='a')
    
    #open csv to add footer
    data_final = open(csv_path, "a")
    line1 = "\n    FILE CLOSED                    : 25 SEPTEMBER 2018 AT 09:54"
    data_final.writelines([line1])
    data_final.close()
    
    
    return csv_path

def prepend_multiple_lines(file_name, list_of_lines):
    """Insert given list of strings as a new lines at the beginning of a file"""

    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    # open given original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Iterate over the given list of strings and write them to dummy file as lines
        for line in list_of_lines:
            write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
 
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

def main():
    #data_converter()
    
    data_converter_returns = data_converter()
    csv_path = data_converter_returns
    
    Line1 = "    FILE TYPE                      : INTERROGATION"
    Line2 = "    FILE TITLE                     : CAL18213.ALL"
    Line3 = "    FILE CREATED                   : 07 NOVEMBER 2019 AT 13:55"
    Line4 = "    PROGRAM VERSION                : MINIMON V.1.7.0"
    Line5 = "\n! The following data were compiled by Rikeem Sholes, USFWS."
    Line6 = "! This file includes data from 07 APRIL 2019 AT 10:48 to 25 SEPTEMBER 2018 AT 09:54.\n"
    
    list_of_lines = [Line1, Line2, Line3, Line4, Line5, Line6]
    
    prepend_multiple_lines(csv_path, list_of_lines)
    
if __name__ == '__main__':
    main()


