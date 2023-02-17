#importing requests, BeautifulSoup, pandas, csv
import re
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import csv


#Creating an empty lists of variables
cities = []
notes = []


#command to create a structure of csv file in which we will populate our scraped data
with open('cities_rate.csv', mode='w') as csv_file:
   fieldnames = ['Villes','Notes']
   writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
   writer.writeheader()


#Defining the opencodezscraping function
def scrape_cities(webpage, page_number):
   next_page = webpage + str(page_number)
   response= requests.get(str(next_page))
   soup = BeautifulSoup(response.content,"html.parser")
   table = soup.find('table', class_="ville")
   table_body = table.find('tbody')
   rows = table_body.find_all('tr')
   for row in rows:
            cols = row.find_all('td')
            if len(cols) == 3:
                city = cols[1].find('h3',string=True)
                city = city.text.strip()
                city = re.sub("[0-9]","", city)
                city = city.replace("()","")
                cities.append(city.strip())
                notes.append(cols[2].find(string=True))

   #Generating the next page url
   if page_number < 25:
      page_number = page_number + 1
      scrape_cities(webpage, page_number)
   
   
   #creating the data frame and populating its data into the csv file
   data = {'Villes':cities, 'Notes':notes}
   df = DataFrame(data, columns = ['Villes','Notes'])
   df.to_csv(r'cities_rate.csv')


if __name__ == '__main__':
   # get_cities_notes()
   #calling the function with relevant parameters
   scrape_cities('https://www.bien-dans-ma-ville.fr/classement-ville-global/?page=', 0)
