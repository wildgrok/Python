__author__ = 'python'
#version in desktop
#last modified 6/17/2020

import csv
import MySQLdb
import os

#filecsv = 'C:/Users/python/PycharmProjects/04-25-2020.csv'
#filecsv = open('04-26-2020.csv')
csvfolder = 'C:/Users/python/PycharmProjects/coronavirus/csv/'

#mydb = MySQLdb.connect(host='localhost',
mydb = MySQLdb.connect(host='localhost', user='root', passwd='Camello2183', db='coronavirus')

#not used
# def get_date_from_csv(csvfile):
#     f = open(csvfile, 'r')
#     f.readline()
#     #get second line only
#     line = f.readline()
#     a = line.split(',')[2]  #get the date
#     b = a[0:10]             #yyyy-mm-dd only
#     return b

def get_list_of_dates():
    cursor = mydb.cursor()
    #s = 'select distinct replace(left(Last_Update, 11),"' + chr(39) + '","' + '") as Last_Update from data_usa'
    s = 'select distinct replace(left(Last_Update, 11),"' + chr(39) + '","' + '") as Last_Update from data_usa2'

    cursor.execute(s)
    return cursor.fetchall()


def load_csv_file(csvfile):
    filecsv = open(csvfile)
    cursor = mydb.cursor()
    csv_data = csv.reader(filecsv, delimiter=',', quotechar='"')
    next(csv_data) #skip header
    cnt = 0
    # `Province_State` varchar(100) NOT NULL,
    # `Country_Region` varchar(100) NOT NULL,
    # `Last_Update` varchar(100) NOT NULL,
    # `Deaths` varchar(100) DEFAULT NULL,
    for row in csv_data:
        # print(row)
        #            Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,FIPS,Incident_Rate,People_Tested,People_Hospitalized,Mortality_Rate,UID,ISO3,Testing_Rate,Hospitalization_Rate
        #FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key,Incidence_Rate,Case-Fatality_Ratio



        # s = 'INSERT IGNORE INTO data_usa(Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,FIPS,Incident_Rate,People_Tested,People_Hospitalized,Mortality_Rate,UID,ISO3,Testing_Rate,Hospitalization_Rate) '
        # # s = s + 'VALUES("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s") '
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
            s = 'INSERT IGNORE INTO data_usa2(Province_State,Country_Region,Last_Update,Deaths) '
            # s = s + 'VALUES("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s") '
            s = s + 'VALUES (' + chr(39) + Province_State + chr(39) + ',' + chr(39) + Country_Region + chr(39) + ',' + chr(39) + Last_Update + chr(39) + ',' + chr(39) + Deaths + chr(39) + '); '
            #s = s + 'VALUES("%s", "%s", "%s","%s") '
            print(s)
            cursor.execute(s)

        # try:
        #     cursor.execute(s, row)
        # #except TypeError:
        # finally:
        #     pass
        cnt = cnt + 1
    #close the connection to the database.
    mydb.commit()
    cursor.close()
    # print("Processed " + str(cnt) + ' records from ' + csvfile)

def load_all_csv_files(csvfolder):
    #list of all files in csv files
    files = os.listdir(csvfolder)
    for x in files:
        if len(x) == 14:
            csvfile = csvfolder + x
            load_csv_file(csvfile)
            print('Processed ' + csvfile)






#===========================================================================

#file = '04-27-2020.csv'
# m = get_date_from_csv(file)
# print(m)
#load_csv_file(file)
#lst = get_list_of_dates()
# for x in lst:
#     print(x)
# print('-----')
#
# print(lst[0][0])
# print(lst[1][0])
# print(lst[2][0])
# print(lst[-1][0])
# files = os.listdir(csvfolder)
# print(files)
load_all_csv_files(csvfolder)