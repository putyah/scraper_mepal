import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

#List Amazon
df = pd.read_csv('links/pricing_links.csv')
df_urls =  df.loc[(df['Website'] == 'amazon.de') | (df['Website'] == 'bol.com') | (df['Website'] == 'shop.vtwonen.nl') ]

df_urls = df_urls['Clean_Url']
urls_clean = df_urls.values.tolist()


#Date
today = date.today()

#Create headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
}

f = csv.writer(open('data/scrape.csv', 'a'))
f.writerow(['Datum','Url', 'Name', 'Price', 'Website'])

def scraper(urls):
    price = ''
    for url in urls:
        status = requests.get(url, headers = headers)
        print(url)
        print(status.status_code)
        data = BeautifulSoup(status.content, 'html.parser')
        name = data.find('h1')
        name = name.text.strip()
        try:
            #Amazon request
            price = data.find(class_='a-offscreen')
            if price:
                data_set(price, url, name, 'Amazon')
        except TypeError:
            pass
        try:
            #Bol request
            price = data.find(class_='product-prices__bol-price')
            if price:
                data_set(price, url, name, 'Bol.com')
        except TypeError:
            pass
        try:
            #vtwonen request
            price = data.find(class_='pdp-price')
            if price:
                data_set(price, url, name, 'vtwonen')
        except TypeError:
            pass


def data_set(price, url, name, website):
    price = (price.text.strip())
    f.writerow([today,url,name,price,website])


scraper(urls_clean)

