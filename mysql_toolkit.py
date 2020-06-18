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
    s = 'select distinct replace(left(Last_Update, 11),"' + chr(39) + '","' + '") as Last_Update from data_usa'
    cursor.execute(s)
    return cursor.fetchall()


def load_csv_file(csvfile):
    filecsv = open(csvfile)
    cursor = mydb.cursor()
    csv_data = csv.reader(filecsv, delimiter=',', quotechar='"')
    next(csv_data) #skip header
    cnt = 0
    for row in csv_data:
        #Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,FIPS,Incident_Rate,People_Tested,People_Hospitalized,Mortality_Rate,UID,ISO3,Testing_Rate,Hospitalization_Rate
        s = 'INSERT IGNORE INTO data_usa(Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,FIPS,Incident_Rate,People_Tested,People_Hospitalized,Mortality_Rate,UID,ISO3,Testing_Rate,Hospitalization_Rate) '
        # s = s + 'VALUES("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s") '
        s = s + 'VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s) '

        try:
            cursor.execute(s, row)
        #except TypeError:
        finally:
            pass
        cnt = cnt + 1
    #close the connection to the database.
    mydb.commit()
    cursor.close()
    print("Processed " + str(cnt) + ' records from ' + csvfile)

def load_all_csv_files(csvfolder):
    #list of all files in csv files
    files = os.listdir(csvfolder)
    for x in files:
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