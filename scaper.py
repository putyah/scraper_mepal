mport pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

#List Amazon
df = pd.read_csv('links/pricing_links.csv')
#df_urls =  df.loc[(df['Website'] == 'amazon.de') | (df['Website'] == 'shop.vtwonen.nl') ]

df_urls = df['Clean_Url']
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
        if 'amazon.de' in url:
            #Amazon request
            price = data.find(class_='a-offscreen')
            data_set(price, url, name, 'Amazon')
        if 'bol.com' in url:
            #Bol request
            price = data.find(class_='product-prices__bol-price')
            data_set(price, url, name, 'Bol.com')
        if 'vtwonen.nl' in url:
            #vtwonen request
            price = data.find(class_='pdp-price')
            data_set(price, url, name, 'vtwonen')
        if 'kozoil-shop.de' in url:
            #kozoil request
            price = data.find(class_='price--amount', itemprop='price')
            data_set(price, url, name, 'kozoil')
        if 'locklock.nl' in url: 
            #locklock request
            price = data.find(class_='price')
            data_set(price, url, name, 'locklock')
        if 'rotho-shop.com' in url: 
            price = data.find(class_='price h1')
            data_set(price, url, name, 'rotho')
        if 'oxo-good-grips.nl' in url: 
            price = data.find(class_='price')
            data_set(price, url, name, 'xo-good-grips')
        if 'shop.dopper.com' in url: 
            price = data.find(class_='price')
            data_set(price, url, name, 'dopper')
        if 'sigg.nl' in url: 
            price = data.find(itemprop='price')
            data_set(price, url, name, 'sigg')             
        if 'chicmic.de' in url: 
            price = data.find(class_='money')
            data_set(price, url, name, 'chicmic')
        if 'laessig-fashion.de' in url: 
            price = data.find(class_='price--content')
            data_set(price, url, name, 'laessig-fashion')
        if 'lurch.de' in url: 
            price = data.find(class_='price--content')
            data_set(price, url, name, 'lurch') 
        if 'sunware.com' in url: 
            price = data.find(class_='lbl-price')
            data_set(price, url, name, 'sunware')
        if 'eu.josephjoseph.com' in url: 
            price = data.find(class_='prd-DetailPrice_Price')
            data_set(price, url, name, 'josephjoseph')
        if 'black-blum.eu' in url: 
            price = data.find(class_='current_price')
            data_set(price, url, name, 'black-blum')
        if 'berghoffworldwide.com' in url: 
            price = data.find(class_='price-final_price')
            data_set(price, url, name, 'berghoffworldwide') 

def data_set(price, url, name, website):
    price = (price.text.strip())
    f.writerow([today,url,name,price,website])


scraper(urls_clean)

#Creat if function based on url
