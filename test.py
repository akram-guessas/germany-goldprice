import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
import json
import numpy as np

import plotly.graph_objects as go
import plotly.express as px


def make_soup(url):
    r = req.get(url)
    soup = bs(r.content, 'html.parser')
    return soup


def get_tableData_karat():
    links = [('eur',"https://www.livepriceofgold.com/germany-gold-price.html"),('usd',"https://www.livepriceofgold.com/us-gold-price.html")]
    
    def karat(i):
        for j in range(7):
            if i == 1:
                karat = "عيار سعر الذهب عيار 24 قيراط"
            elif i == 2:
                karat = "سعر الذهب عيار 22 قيراط"
            elif i == 3:
                karat = "سعر الذهب عيار 21 قيراط"
            elif i == 4:
                karat = "سعر الذهب عيار 18 قيراط"
            elif i == 5:
                karat = "سعر الذهب عيار 14 قيراط"
            elif i == 6:
                karat = "سعر الذهب عيار 10 قيراط"
            elif i == 7:
                karat = "سعر الذهب عيار 6 قيراط"
            else:
                print("Error in data list")
            break
           
        return karat
    
    data_gram = []
    price_list = []
    def get_data_gram(tables):
        trs = tables[0].find_all('tr')
        trs.pop(0)
        i = 1
        for tr in trs:
            d, d1 = {}, {}
            tds = tr.find_all('td')
            tds.pop(0)
            karat1 = karat(i)
            i += 1
            color = tds[3].get("class")[0]
            if color == 'green-font':
                val = True
            else:
                val = False
            d['color'] = val
            d['change'] = tds[3].get_text()
            d['low'] = tds[2].get_text()
            d['high'] = tds[1].get_text()
            d['price'] = tds[0].get_text()
            d['karat'] = karat1
            d1['karat'] = karat1
            d1['gram'] = d['price']
            price_list.append(d1)
            d['currency'] = link[0]
            data_gram.append(d)
            
        return data_gram, price_list

    data_onece = []
    def get_data_onece(tables):
        trs = tables[1].find_all('tr')
        trs.pop(0)
        i = 1
        for tr in trs:
            d, d1 = {}, {}
            tds = tr.find_all('td')
            tds.pop(0)
            karat1 = karat(i)
            i += 1
            color = tds[3].get("class")[0]
            if color == 'green-font':
                val = True
            else:
                val = False
            d['color'] = val
            d['change'] = tds[3].get_text()
            d['low'] = tds[2].get_text()
            d['high'] = tds[1].get_text()
            d['ounce'] = tds[0].get_text()
            d['karat'] = karat1
            d['currency'] = link[0]
            data_onece.append(d)
        return data_onece
    
    data_kg = []
    def get_data_kg(tables):
        trs = tables[2].find_all('tr')
        trs.pop(0)
        i = 1
        for tr in trs:
            d = {}
            tds = tr.find_all('td')
            tds.pop(0)
            karat1 = karat(i)
            i += 1
            if karat1 == "سعر الذهب عيار 21 قيراط":
                if link[0] == "eur":
                    url = "http://goldpricez.com/eu/21k/kg"
                    soup = make_soup(url)
                    kg_eur = soup.find('div',{'class': 'gold_panel'}).find_all('tr')[0].find_all('td')[1].get_text()
                    kg_eur = kg_eur.split()[0]
                    d['kg'] = kg_eur + ".00"
                    d['karat'] = karat1
                    d['currency'] = link[0]
                    p = tds[0].get_text()
                    test = False
                else:
                    url = "http://goldpricez.com/us/21k/kg"
                    soup = make_soup(url)
                    kg_usd = soup.find('div',{'class': 'gold_panel'}).find_all('tr')[0].find_all('td')[1].get_text()
                    kg_usd = kg_usd.split()[0]
                    d['kg'] = kg_usd + ".00"
                    d['karat'] = karat1
                    d['currency'] = link[0]
                    p = tds[0].get_text()
            else:
                try:
                    d['kg'] = p
                    d['karat'] = karat1
                    d['currency'] = link[0]
                    p = tds[0].get_text()
                except:
                    d['kg'] = tds[0].get_text()
                    d['karat'] = karat1
                    d['currency'] = link[0]
                
            data_kg.append(d)
        d = {}
        d['kg'] = p
        d['karat'] = karat1
        d['currency'] = link[0]
        data_kg.append(d)
        return data_kg
        
    data_tola = []
    def get_data_tola(tables):
        trs = tables[3].find_all('tr')
        trs.pop(0)
        i = 1
        for tr in trs:
            d = {}
            tds = tr.find_all('td')
            tds.pop(0)
            karat1 = karat(i)
            i += 1
            if karat1 == "سعر الذهب عيار 21 قيراط":
                if link[0] == "eur":
                    url = "http://goldpricez.com/eu/21k/tola-india"
                    soup = make_soup(url)
                    tola_eur = soup.find('div',{'class': 'gold_panel'}).find_all('tr')[0].find_all('td')[1].get_text()
                    tola_eur = tola_eur.split()[0]
                    d['tola'] = tola_eur
                    d['karat'] = karat1
                    d['currency'] = link[0]
                    p = tds[0].get_text()
                else:
                    url = "http://goldpricez.com/us/21k/tola-india"
                    soup = make_soup(url)
                    tola_usd = soup.find('div',{'class': 'gold_panel'}).find_all('tr')[0].find_all('td')[1].get_text()
                    tola_usd = tola_usd.split()[0]
                    d['tola'] = tola_usd
                    d['karat'] = karat1
                    d['currency'] = link[0]
                    p = tds[0].get_text()
                    
            else:
                try:
                    d['tola'] = p
                    d['karat'] = karat1
                    d['currency'] = link[0]
                    p = tds[0].get_text()
                except:
                    d['tola'] = tds[0].get_text()
                    d['karat'] = karat1
                    d['currency'] = link[0]
                
            data_tola.append(d)
        d = {}
        d['tola'] = p
        d['karat'] = karat1
        d['currency'] = link[0]
        data_tola.append(d)
        return data_tola
    
    for link in links:
        soup = make_soup(link[1])
        tables = soup.find_all('table',{'class':'data-table-price'})
        list_gram, price = get_data_gram(tables)
        df = pd.DataFrame(price)
        df1 = pd.DataFrame(get_data_onece(tables))
        df2 = pd.DataFrame(get_data_kg(tables))
        df3 = pd.DataFrame(get_data_tola(tables))
        df = df.join(df1['ounce']).join(df2['kg']).join(df3['tola']).join(df3['currency'])
   
    pd.DataFrame(data_gram).to_csv('./static/goldprice/csv/data_gram.csv', index=False)
    pd.DataFrame(data_onece).to_csv('./static/goldprice/csv/data_ounce.csv', index=False)
    df.to_csv('./static/goldprice/csv/all_gold_unit.csv', index=False)

     
if __name__ == '__main__':
    '''price_list = []
    data_gram = []
    get_ounce_data()'''
    # silver_price_data()
    get_tableData_karat()
    
    
