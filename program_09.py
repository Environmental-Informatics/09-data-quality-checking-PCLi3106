#!/bin/env python
"""
Author: Pin-Ching Li (li3106)
Script adapted from program_09_template.py
Created on 04/19/2020
This script is created for data quality checking

"""
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']
    
    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""
    # define column names
    colNames = ['Precip','Max Temp', 'Min Temp','Wind Speed']
    # Replace the -999 value to Nan
    DataDF = DataDF.replace(-999,np.NaN)
    # get the amount of Nan in every column
    Null_DF = DataDF.isnull().sum()
    # reshape the array so that it could fit the dataframe format
    Null_DF = np.reshape(np.array(Null_DF),(1,4))
    # Create the Relaced Values DataFrame
    ReplacedValuesDF = pd.DataFrame(Null_DF, index=["1. No Data"], columns=colNames)

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
    
    # define column names
    colNames = ['Precip','Max Temp', 'Min Temp','Wind Speed']
    # Conditional change values within dataframe
    DataDF.loc[DataDF['Precip'] < 0, 'Precip'] = np.NaN
    DataDF.loc[DataDF['Precip'] > 25, 'Precip'] = np.NaN
    DataDF.loc[DataDF['Max Temp'] > 35, 'Max Temp'] = np.NaN
    DataDF.loc[DataDF['Max Temp'] < -25, 'Max Temp'] = np.NaN
    DataDF.loc[DataDF['Min Temp'] > 35, 'Min Temp'] = np.NaN
    DataDF.loc[DataDF['Min Temp'] < -25, 'Min Temp'] = np.NaN
    DataDF.loc[DataDF['Wind Speed'] < 0, 'Wind Speed'] = np.NaN
    DataDF.loc[DataDF['Wind Speed'] > 10, 'Wind Speed'] = np.NaN

    # get the amount of Nan in every column
    Null_DF2 = DataDF.isnull().sum()
    # deduct the amount of Nan with amount of missing data
    Null_DF1 = np.array(ReplacedValuesDF.iloc[0])
    Null_DF2 = Null_DF2 - Null_DF1
    # reshape the array so that it could fit the dataframe format
    Null_DF2 = np.reshape(np.array(Null_DF2),(1,4))
    # Append the Relaced Values DataFrame
    ReplacedValuesDF = ReplacedValuesDF.append((pd.DataFrame(Null_DF2, index=["2. Gross Error"], columns=colNames)))

    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    # define column names
    colNames = ['Precip','Max Temp', 'Min Temp','Wind Speed']
    # times max temp is lower than min temp
    times = 0
    for i in range(DataDF.index.size):
        # if max temp < min temp
        if DataDF['Max Temp'][i] < DataDF['Min Temp'][i]:
            # store max temp
            temp_max = DataDF['Max Temp'] [i]
            # swap two values
            DataDF['Max Temp'][i] = DataDF['Min Temp'][i]
            DataDF['Min Temp'][i] = temp_max
            # times of swapping gain one
            times +=1     
    # get the times of swapping
    Null_DF3 = np.reshape(np.array([0, times, times, 0]),(1,4))
    # Append the Relaced Values DataFrame
    ReplacedValuesDF = ReplacedValuesDF.append((pd.DataFrame(Null_DF3, index=["3. Swapped"], columns=colNames)))

    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    # define column names
    colNames = ['Precip','Max Temp', 'Min Temp','Wind Speed']
    # times max temp minus min temp larger than 25
    times2 = 0
    for i in range(DataDF.index.size):
        if (DataDF['Max Temp'][i] - DataDF['Min Temp'][i])>25:
            # make max and min temp as nan when max-min >25 degree
            DataDF['Max Temp'][i] = np.NaN
            DataDF['Min Temp'][i] = np.NaN
            # times of swapping gain one
            times2 +=1     
    # get the times of swapping
    Null_DF4 = np.reshape(np.array([0, times2, times2, 0]),(1,4))
    # Append the Relaced Values DataFrame
    ReplacedValuesDF = ReplacedValuesDF.append((pd.DataFrame(Null_DF4, index=["4. Range Fail"], columns=colNames)))
    
    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    
    print("\nRaw data.....\n", DataDF.describe())
    # keep dataframe before correction
    DataDF_raw = DataDF
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
   
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    # Draw precipitation dataset
    plt.plot(DataDF_raw.index,DataDF_raw['Precip'],label='Before Correction')
    plt.plot(DataDF.index,DataDF['Precip'],label='After Correction')
    plt.xlabel('Time')
    plt.ylabel('Precipitation')
    plt.title('Precipitation Dataset')
    # make graph more clear (ignore the -999 missing value)
    plt.ylim(-50, 300) 
    plt.legend()
    plt.setp(plt.gca().xaxis.get_majorticklabels(),
         'rotation', 90)
    plt.show()
    
    # Draw max temperature dataset
    plt.plot(DataDF_raw.index,DataDF_raw['Max Temp'],label='Before Correction')
    plt.plot(DataDF.index,DataDF['Max Temp'],label='After Correction')
    plt.xlabel('Time')
    plt.ylabel('Maximum Temperature')
    plt.title('Maximum Temperature Dataset')
    # make graph more clear (ignore the -999 missing value)
    plt.ylim(-50, 300) 
    plt.legend()
    plt.setp(plt.gca().xaxis.get_majorticklabels(),
         'rotation', 90)
    plt.show()

    # Draw min temperature dataset
    plt.plot(DataDF_raw.index,DataDF_raw['Min Temp'],label='Before Correction')
    plt.plot(DataDF.index,DataDF['Min Temp'],label='After Correction')
    plt.xlabel('Time')
    plt.ylabel('Minimum Temperature')
    plt.title('Minimum Temperature Dataset')
    # make graph more clear (ignore the -999 missing value)
    plt.ylim(-50, 100) 
    plt.legend()
    plt.setp(plt.gca().xaxis.get_majorticklabels(),
         'rotation', 90)
    plt.show()
    
    # Draw Wind Speed dataset
    plt.plot(DataDF_raw.index,DataDF_raw['Wind Speed'],label='Before Correction')
    plt.plot(DataDF.index,DataDF['Wind Speed'],label='After Correction')
    plt.xlabel('Time')
    plt.ylabel('Wind Speed')
    plt.title('Wind Speed Dataset')
    # make graph more clear (ignore the -999 missing value)
    plt.ylim(-10, 50) 
    plt.legend()
    plt.setp(plt.gca().xaxis.get_majorticklabels(),
         'rotation', 90)
    plt.show()
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']
    
    # drop NaN value within the dataset
    DataDF.dropna()
    # save dataframe to txt file
    DataDF.to_csv("Data_afterchecking.txt", header=None,sep=" ")
    # saave the information on failed check
    ReplacedValuesDF.to_csv("Failedcheck.txt", sep ="\t")