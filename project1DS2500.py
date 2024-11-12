#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 15:15:56 2022

@author: ashvikaboopathy
"""
'''
    Ashvika Boopathy 
    DS 2500
    Project #1 
    March 11, 2022
    
    Question: Did air pollution decrease due to covid in 2020? 
               Which country experienced the most change in air pollution in 2020? 
               
               
    Air Pollution CSV- https://www.kaggle.com/sumandey/daily-air-quality-dataset-india
    US Covid Cases CSV - https://github.com/nytimes/covid-19-data/blob/master/us.csv

'''

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

def City_List(airquality_df): 
    '''
    Parameters
    ----------
    airquality_df : TYPE
        DESCRIPTION.
        
    Function: Print a List of all the Cities in airquality_df

    Returns
    -------
    city_list :  List of all Cities in airquality_df.

    '''
    # Create empty list 
    city_list = []
    
    # Iteratre through City column and add city to city list if it is not in there 
    for i in airquality_df["CITY"]: 
        if i not in city_list: 
            city_list.append(i)
            
        else: 
            pass 
        
    return city_list

def time_stamp(df):
    '''
    Function: Add Month and Year columns to dataframes
    
    Parameters
    ----------
    df : Either dataframes, airquality_df or us_cases_df.

    Returns
    -------
    df : year and month added to the dataframe as separate columns.

    '''
    #Add new column year to dataframes
    df['year'] = pd.DatetimeIndex(df['DATE']).year
    
    # Add new column month to dataframes
    df['month'] = pd.DatetimeIndex(df['DATE']).month
    df.head()
    
    return df

def year_country(airquality_ts_df): 
    '''
    Function: Group air pollution data by country, year, and month
    
    Parameters
    ----------
    airquality_ts_df : Dataframe Containing Date, Country, City, Value of Air 
                    Pollution.

    Returns
    -------
    aq_month_df : Dataframe that groups the data by the country, year, and month.

    '''
    # Use groupby function to group by country, year, and month
    aq_month_df = airquality_ts_df.groupby(by = ["COUNTRY","year", "month"]).agg("mean")
    
    # Adds Index to data
    aq_month_df = aq_month_df.reset_index()
    
    return aq_month_df

def cases_by_yearmonth(us_cases_timestamp): 
    '''
    Function: Group Covid Cases by Year and month

    Parameters
    ----------
    us_cases_timestamp : Dataframe that contains Date, Cases, Deaths, Month, 
                        and Year of Covid Cases

    Returns
    -------
    us_cases_mean : Dataframe grouped by the Year and Month with the mean cases.

    '''
    # Use Groupby to group by year and month
    us_cases_mean = us_cases_timestamp.groupby(by = ["year", "month"]).agg("mean") 
    
    # Adds index to data
    us_cases_mean = us_cases_mean.reset_index()
    
    return us_cases_mean


def main(): 
    
    # Read in Data 
    airquality_df = pd.read_csv("air_quality_index.csv")   
    
    us_cases_df = pd.read_csv("us_cases.csv")
    
    # Print List of Cities in the airpollution dataframe
    city_lst = City_List(airquality_df)
    print("These are the cities from which air pollution data was collected " 
          "from 2019-2021:",'\n', city_lst)
          
    airquality_ts_df = time_stamp(airquality_df)
    #print(airquality_ts_df)

    # Renamed date column to use the time_stamp function 
    us_cases_df.rename(columns = {'date':'DATE'}, inplace = True)
    #print(us_cases_df)
    
    # US Covid Cases with Month and Year added Dataframe
    us_cases_timestamp = time_stamp(us_cases_df)

    # Grouped Air pollution data by country, year, and month 
    year_country_data = year_country(airquality_ts_df)

    # Retrieving data specifically from 2020 and the US from air pollution data
    twenty = year_country_data[year_country_data["year"] == 2020]
    us_twenty = twenty[twenty["COUNTRY"] == "US"]
    
    # Creating lineplot of airpollution for US and India in 2020
    sns.lineplot(x='month', y='VALUE', data=twenty,hue= "COUNTRY", marker="o")
    # Add title
    plt.title('Air Pollution Levels in US and India (2020)')
    plt.show()

    # Covid Cases in the US grouped by year and month
    us_year_month_cases = cases_by_yearmonth(us_cases_timestamp)
    #print(us_year_month_cases)
    
    # Create Moving average and Barplot using Seaborn
    
    #Retrieve data from 2020
    us_year_month_cases_twenty = us_year_month_cases[us_year_month_cases["year"] == 2020]
    # Create Moving Average
    us_year_month_cases_twenty["Moving Average"] = us_year_month_cases_twenty["cases"].rolling(window = 2).mean()
    
    fig, ax1 = plt.subplots()
    
    # Barplot & Lineplot
    sns.barplot(x = "month", y = "VALUE", data = us_twenty, ax = ax1)
    ax2 = ax1.twinx()
    sns.lineplot(data = us_year_month_cases_twenty, x = "month", y = "cases", ax = ax2)

    plt.title("Monthly Cases and Moving Average in the US (2020)")

    plt.show()
main()

