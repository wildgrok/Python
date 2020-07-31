__author__ = 'python'
#version in desktop
#last modified
#7/30/2020 fixed pk issue in insert (in if exists)
# 7/6/2020 works with short table data_usa2
# 6/17/2020
#copied from mysql version 7/24/2020
#version for sql server

import csv
import os
from dblib3_ado import *


#not used
# def get_date_from_csv(csvfile):
#     f = open(csvfile, 'r')
#     f.readline()
#     #get second line only
#     line = f.readline()
#     a = line.split(',')[2]  #get the date
#     b = a[0:10]             #yyyy-mm-dd only
#     return b

# not used
def get_list_of_dates():
    cursor = mydb.cursor()
    s = 'select distinct replace(left(Last_Update, 11),"' + chr(39) + '","' + '") as Last_Update from data_usa'
    #s = 'select distinct replace(left(Last_Update, 11),"' + chr(39) + '","' + '") as Last_Update from data_usa2'
    cursor.execute(s)
    return cursor.fetchall()

def get_col_position(colnames, col):
    cnt = 0
    for x in colnames:
        if x == col:
            return cnt
        cnt = cnt + 1


def load_csv_file(csvfile):
    filecsv = open(csvfile)
    cursor = mydb.cursor
    csv_data = csv.reader(filecsv, delimiter=',', quotechar='"')
    reader = csv.DictReader(filecsv, delimiter=',')
    colnames = reader.fieldnames
    # print(colnames)
    # pos_Province_State =  get_col_position(colnames, 'Province_State')
    # pos_Country_Region =  get_col_position(colnames, 'Country_Region')
    # pos_Last_Update    =  get_col_position(colnames, 'Last_Update')
    # pos_Deaths         =  get_col_position(colnames, 'Deaths')
    cnt = 0
    # `Province_State` varchar(100) NOT NULL,
    # `Country_Region` varchar(100) NOT NULL,
    # `Last_Update` varchar(100) NOT NULL,
    # `Deaths` varchar(100) DEFAULT NULL,
    #truncate table before
    # s = 'truncate table data_usa2;'
    # cursor.execute(s)
    for row in csv_data:
        #            Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,FIPS,Incident_Rate,People_Tested,People_Hospitalized,Mortality_Rate,UID,ISO3,Testing_Rate,Hospitalization_Rate
        #FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key,Incidence_Rate,Case-Fatality_Ratio
        # s = 'INSERT IGNORE INTO data_usa(Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,FIPS,Incident_Rate,People_Tested,People_Hospitalized,Mortality_Rate,UID,ISO3,Testing_Rate,Hospitalization_Rate) '
        # # # s = s + 'VALUES("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s") '
        # s = s + 'VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s) '

        if str(row[0]) + str(row[1]) == '':
            Province_State = str(row[2])
            Country_Region = str(row[3])
            Last_Update    = str(row[4])
            Deaths         = str(row[8])
        else:
            Province_State = str(row[0])
            Country_Region = str(row[1])
            Last_Update    = str(row[2])
            Deaths         = str(row[6])


        if Country_Region == 'US':
            s = 'if not exists (select 1 from [dbo].[data_usa2] where Last_Update = ' + chr(39) + Last_Update + chr(39)
            s = s + ' and Province_State = ' +chr(39) + Province_State + chr(39)
            s = s + ' and Country_Region = ' +chr(39) + Country_Region + chr(39) + ') '
            s = s + 'INSERT INTO data_usa2(Province_State,Country_Region,Last_Update,Deaths) '
            s = s + 'VALUES (' + chr(39) + Province_State + chr(39) + ',' + chr(39) + Country_Region + chr(39) + ',' + chr(39) + Last_Update + chr(39) + ',' + chr(39) + Deaths + chr(39) + '); '
            #print(s)
            #print(row)
            cursor.execute(s)
            # try:
            #     cursor.execute(s, row)
            # #except TypeError:
            # finally:
            #     pass
            cnt = cnt + 1
    #close the connection to the database.
    mydb.commit()
    # cursor.close()
    mydb.close()
    print("Processed " + str(cnt) + ' records from ' + csvfile)

def load_all_csv_files(csvfolder):
    #list of all files in csv files
    files = os.listdir(csvfolder)
    for x in files:
        if len(x) == 14:
            csvfile = csvfolder + x
            load_csv_file(csvfile)
            print('Processed ' + csvfile)

#===================PROGRAM START============================================


if __name__ == '__main__':
    csvfolder = 'C:/Users/python/PycharmProjects/coronavirus/csv/'
    mydb = Connection('WORKSTATION\SQLEXPRESS', db='coronavirus')
    print("Connection string: " + mydb.constr)
    if mydb.connected == 1:
        print("Connected OK")
        load_all_csv_files(csvfolder)