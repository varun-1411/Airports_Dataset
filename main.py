# read xls file and write to csv file
import pandas as pd
import openpyxl
import os
import sys
import csv
import datetime


# read xls file
def read_xls_file(file_name):
    df = pd.read_excel(file_name, sheet_name='Sheet1')
    return df


# write to csv file
def write_csv_file(file_name, df):
    df.to_csv(file_name, index=False)


# function to get the time and date from the string

def get_time(x):
    return pd.to_datetime(x, format='%H:%M').time()


def get_date(x, year=2023):
    # Parse the input string with a custom date format and set the desired year
    date_string = f'{x.strip()}, {year}'
    return pd.to_datetime(date_string, format='%d, %b., %Y').date()


def split_time(x):
    return x.split('\xa0')[0]


def split_date(x):
    return x.split('\xa0')[2]


# main function
def main():
    # read xls file
    df_departure_aircrafs = read_xls_file('Aircrafts_departure.xlsx')
    df_arrivals_aircrafs = read_xls_file('ARRIVALS_AIRCRAFTT.xlsx')

    # write to csv file
    write_csv_file('df_departure_aircrafs.csv', df_departure_aircrafs)
    write_csv_file('df_arrivals_aircrafs.csv', df_arrivals_aircrafs)

    # read csv file
    df_departure_terminals = pd.read_csv('dep_blr_7_sep_airport_website.csv')
    df_arrivals_terminals = pd.read_csv('arr_blr_7_sep_airport_website.csv')

    # ---------------------------------------------------------------------------------------- Terminal
    # fillna with T1 for departure terminals and arrival terminals
    df_departure_terminals['Terminal'] = df_departure_terminals['Terminal'].fillna('T1')
    df_arrivals_terminals['Terminal'] = df_arrivals_terminals['Terminal'].fillna('T1')

    df_departure_terminals['Scheduled_Time'] = df_departure_terminals['Scheduled'].apply(split_time)
    df_arrivals_terminals['Scheduled_time'] = df_arrivals_terminals['Scheduled'].apply(split_time)
    df_departure_terminals['Scheduled_date'] = df_departure_terminals['Scheduled'].apply(split_date)
    df_arrivals_terminals['Scheduled_date'] = df_arrivals_terminals['Scheduled'].apply(split_date)

    df_departure_terminals['Estimated_time'] = df_departure_terminals['Estimated time'].apply(split_time)
    df_arrivals_terminals['Estimated_time'] = df_arrivals_terminals['Estimated time'].apply(split_time)
    df_departure_terminals['Estimated_date'] = df_departure_terminals['Estimated time'].apply(split_date)
    df_arrivals_terminals['Estimated_date'] = df_arrivals_terminals['Estimated time'].apply(split_date)

    # convert time string to time format
    df_departure_terminals['Scheduled_Time'] = df_departure_terminals['Scheduled_Time'].apply(get_time)
    df_arrivals_terminals['Scheduled_time'] = df_arrivals_terminals['Scheduled_time'].apply(get_time)
    df_departure_terminals['Estimated_time'] = df_departure_terminals['Estimated_time'].apply(get_time)
    df_arrivals_terminals['Estimated_time'] = df_arrivals_terminals['Estimated_time'].apply(get_time)

    # convert date string to date format
    df_departure_terminals['Scheduled_date'] = df_departure_terminals['Scheduled_date'].apply(get_date)
    df_arrivals_terminals['Scheduled_date'] = df_arrivals_terminals['Scheduled_date'].apply(get_date)
    df_departure_terminals['Estimated_date'] = df_departure_terminals['Estimated_date'].apply(get_date)
    df_arrivals_terminals['Estimated_date'] = df_arrivals_terminals['Estimated_date'].apply(get_date)

    # clean the data
    def split_string(x):
        return x.split('\xa0')[0]

    df_arrivals_terminals['Departure'] = df_arrivals_terminals['Departure'].apply(split_string)
    df_arrivals_terminals['ARR_CODE'] = df_arrivals_terminals['ARR_CODE'].apply(lambda x: 'BLR' if x != '(BLR)' else x)

    df_departure_terminals['Arrival'] = df_departure_terminals['Arrival'].apply(split_string)
    df_departure_terminals['DEP_CODE'] = df_departure_terminals['DEP_CODE'].apply(
        lambda x: 'BLR' if x == '(BLR)' else x)

    # drop the columns
    df_departure_terminals = df_departure_terminals.drop(['Scheduled', 'Estimated time', 'Unnamed: 10', 'Gate'], axis=1)
    df_arrivals_terminals = df_arrivals_terminals.drop(['Scheduled', 'Estimated time'], axis=1)

    # ---------------------------------------------------------------------------------------- Aircrafts
    # Add aircrafts from df_departure_aircrafs to df_departure_terminals and df_arrivals_aircrafs to df_arrivals_terminals
    df_departure_terminals['Aircraft'] = ''
    df_arrivals_terminals['Aircraft'] = ''
    # convert the flight no to string and aircraft to string
    df_departure_terminals['Flight No'] = df_departure_terminals['Flight No'].astype(str)
    df_arrivals_terminals['Flight No'] = df_arrivals_terminals['Flight No'].astype(str)
    df_departure_aircrafs['Flight_no'] = df_departure_aircrafs['Flight_no'].astype(str)
    df_arrivals_aircrafs['Flight_no'] = df_arrivals_aircrafs['Flight_no'].astype(str)

    df_departure_aircrafs['Aircraft'] = df_departure_aircrafs['Aircraft'].astype(str)
    df_arrivals_aircrafs['Aircraft'] = df_arrivals_aircrafs['Aircraft'].astype(str)

    df_departure_aircrafs['Aircraft'] = df_departure_aircrafs['Aircraft'].apply(split_string)
    df_arrivals_aircrafs['Aircraft'] = df_arrivals_aircrafs['Aircraft'].apply(split_string)

    # departure
    for i in range(len(df_departure_terminals)):
        for j in range(len(df_departure_aircrafs)):
            if df_departure_terminals['Flight No'][i] == df_departure_aircrafs['Flight_no'][j]:
                print(df_departure_terminals['Flight No'][i], df_departure_aircrafs['Flight_no'][j])
                df_departure_terminals['Aircraft'][i] = df_departure_aircrafs['Aircraft'][j]
                break
            else:
                df_departure_terminals['Aircraft'][i] = 'NA'

    # check if there are any aircrafts with NA
    for i in range(len(df_departure_terminals)):
        if df_departure_terminals['Aircraft'][i] == 'NA':
            print(df_departure_terminals['Flight No'][i])


    # check the difference between the two sets

    set1 = set(df_departure_aircrafs['Flight_no'])
    set2 = set(df_departure_terminals['Flight No'])
    print(set1.difference(set2))
    print(set2.difference(set1))

    # arrival
    for i in range(len(df_arrivals_terminals)):
        for j in range(len(df_arrivals_aircrafs)):
            if df_arrivals_terminals['Flight No'][i] == df_arrivals_aircrafs['Flight_no'][j]:
                print(df_arrivals_terminals['Flight No'][i], df_arrivals_aircrafs['Flight_no'][j])
                df_arrivals_terminals['Aircraft'][i] = df_arrivals_aircrafs['Aircraft'][j]
                break
            else:
                df_arrivals_terminals['Aircraft'][i] = 'NA'

    # check if there are any aircrafts with NA
    for i in range(len(df_arrivals_terminals)):
        if df_arrivals_terminals['Aircraft'][i] == 'NA':
            print(df_arrivals_terminals['Flight No'][i])

#---------------------------------------------------------------------------------------- save 2 df
    df_departure_terminals.to_csv('df_departures_blr.csv', index=False)
    df_arrivals_terminals.to_csv('df_arrivals_blr.csv', index=False)



