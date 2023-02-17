import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import json

class Scrapping:

    def get_average_rent_file_url(url):
        response = requests.get('https://www.data.gouv.fr/fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2018/')
        soup = BeautifulSoup ( response.content , "html.parser" )
        average_rent_downlaod_file_url=soup.find('a',class_="fr-btn fr-btn--sm fr-icon-download-line").get('href')
        print(average_rent_downlaod_file_url)
        return average_rent_downlaod_file_url


    def download_file(url):
        req = requests.get(url)
        url_content = req.content
        csv_file = open('average_rent.csv', 'wb')
        csv_file.write(url_content)
        csv_file.close()
        return csv_file


def get_average_rent_cities_by_insee(code_insee):
    data = pd.read_csv("average_rent.csv",encoding='latin-1')

    for index, row in data.iterrows():
        print(row[index])
        pass
        #if row['DEP']==code_insee:
            #print(row['LIBGEO'],row['loypredm2'], row['lwr.IPm2'],row['upr.IPm2'])
 
def csv_to_json(csv_file_path, json_file_path):
    #create a dictionary
    data_dict = {}
 
    #Step 2
    #open a csv file handler
    with open(csv_file_path, encoding = 'latin-1') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
 
        #convert each row into a dictionary
        #and add the converted data to the data_variable
 
        for rows in csv_reader:
 
            #assuming a column named 'No'
            #to be the primary key
            key = rows['Serial Number']
            data_dict[key] = rows
 
    #open a json file handler and use json.dumps
    #method to dump the data
    #Step 3
    with open(json_file_path, 'w', encoding = 'latin-1') as json_file_handler:
        #Step 4
        json_file_handler.write(json.dumps(data_dict, indent = 4))
 

def save_file_content_to_db(average_rent):
    try:
        conn = mysql.connect(host='localhost', database='accommodation', user='root', password='root@123')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute('DROP TABLE IF EXISTS average_rent;')
            print('Creating table....')
            # in the below line please pass the create table statement which you want #to create
            cursor.execute("CREATE TABLE average_rent(lib_geo varchar(255),dep_insee int,loypredm2 double,lwr_IPm2 double,upr_IPm2 double)")
            print("Table is created....")
            #loop through the data frame
            for i,row in average_rent.iterrows():
                #here %S means string values 
                sql = "INSERT INTO accommodation.average_rent VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(sql, tuple(row))
                print("Record inserted")
                # the connection is not auto committed by default, so we must commit to save our changes
                conn.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)

if __name__ == '__main__':
    file_url=get_average_rent_file_url()
    csv_file=download_file(file_url)
    get_average_rent_cities_by_insee(64)
