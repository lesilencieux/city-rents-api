import requests
from bs4 import BeautifulSoup
import re


def get_cities_notes():
    # cities rates website
    cities_rates_website='https://www.bien-dans-ma-ville.fr/classement-ville-global/'

    # call get method to request the page
    page=requests.get(cities_rates_website)

    # with the help of BeautifulSoup
    # method and html parser created soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # With the help of find_all
    # method perform searching in parser tree
    data = []
    for i in range(1,26):        
        # check all link which is contain
        # "www.geeksforgeeks.org" string
        base_url="https://www.bien-dans-ma-ville.fr/classement-ville-global/"
        sufix= "?page="
        if i==1:
            next_url=base_url
        else:
            next_url=f"{base_url}{sufix}{i}"
        print(next_url)
        # call get method to request next url
        nextpage = requests.get(next_url)
            
        # create soup for next url
        nextsoup = BeautifulSoup(nextpage.content, 'html.parser')
            
        # we can scrap any thing of the
        # next page here we are scraping title of
        # nexturl page string
        
        table = nextsoup.find('table', class_="ville")
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
    print(data)

if __name__ == '__main__':
    get_cities_notes()
