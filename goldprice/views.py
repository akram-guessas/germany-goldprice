from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.http import HttpResponse
from blog.models import Post

# Import libs
from deep_translator import GoogleTranslator
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd 
import numpy as np
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your views here.
# make soup function
def make_soup(url):
    r = req.get(url)
    soup = bs(r.content, 'html.parser')
    return soup

def convert_date(n):
    if n == '01':
        month = 'يناير'
        x = '01'
    elif n == '02':
        month = 'فبراير'
        x = '02'
    elif n == '03':
        month = 'مارس'
        x = '03'
    elif n == '04':
        month = 'ابريل'
        x = '04'
    elif n == '05':
        month = 'مايو'
        x = '05'
    elif n == '06':
        month = 'يونيو'
        x = '06'
    elif n == '07':
        month = 'يوليو'
        x = '07'
    elif n == '08':
        month = 'أغسطس'
        x = '08'
    elif n == '09':
        month = 'سبتمبر'
        x = '09'
    elif n == '10':
        month = 'أكتوبر'
        x = '10'
    elif n == '11':
        month = 'نوفمبر'
        x = '11'
    else :
        month = 'ديسمبر'
        x = '12'
    return month , x

def convert_days_ar(day):
    if day == 'Mon':
        day_ar = 'الاثنين'
    elif day == 'Tue':
        day_ar = 'الثلاثاء'
    elif day == 'Wed':
        day_ar = 'الأربعاء'
    elif day == 'Thu':
        day_ar = 'الخميس'
    elif day == 'Sun':
        day_ar = 'الأحد'
    elif day == 'Sat':
        day_ar = 'السبت'
    elif day == 'Today':
        day_ar = 'اليوم'
    elif day == 'Yesterday':
        day_ar = 'البارحة'
    else:
        day_ar = 'الجمعة'
    return day_ar

def convert_date_str(n):
    if n == 'Jan':
        month = 'يناير'
        x = '01'
    elif n == 'Feb':
        month = 'فبراير'
        x = '02'
    elif n == 'Mar':
        month = 'مارس'
        x = '03'
    elif n == 'Apr':
        month = 'ابريل'
        x = '04'
    elif n == 'May':
        month = 'مايو'
        x = '05'
    elif n == 'Jun':
        month = 'يونيو'
        x = '06'
    elif n == 'Jul':
        month = 'يوليو'
        x = '07'
    elif n == 'Aug':
        month = 'أغسطس'
        x = '08'
    elif n == 'Sep':
        month = 'سبتمبر'
        x = '09'
    elif n == 'Oct':
        month = 'أكتوبر'
        x = '10'
    elif n == 'Nov':
        month = 'نوفمبر'
        x = '11'
    else :
        month = 'ديسمبر'
        x = '12'
    return month , x

# Chart function
def make_chart(df,x,y,title,html_file_name,marker):
    # fig = px.line(df.head(n_of_days).loc[::-1], x=x, y=y, markers=False, title=title) 
    x = df[x].loc[::-1]
    y = df[y].loc[::-1]
    fig = go.Figure(data = go.Scatter(x=x, y=y, mode='lines+markers'))
    
    # fig = px.line(df.loc[::-1], x=x, y=y, markers=marker, title=title) 
    fig.update_layout(title=title,)
    fig.update_layout(modebar_bgcolor="yellowgreen")
    fig.update_layout(title_font_color="#333")
    fig.update_layout(title_font_size=18)
    fig.update_layout(title_x=0.5)  
    fig.write_html(html_file_name)

def make_chart_3years(df,x,y,title,html_file_name):
    fig = px.line(df.loc[::-1], x=x, y=y, markers=False, title=title) 
    # fig.show()
    # fig.update_xaxes(rangeslider_visible=True)
    fig.write_html(html_file_name)

# History of 24k Gold Price per Ounce
def history_of_ounce():
    url = 'http://goldpricez.com/eu/ounce'
    soup = make_soup(url)
    table = soup.find('table',{'id':'historymain_table_gold1'})
    trs = table.find_all('tr')
    trs.pop(0)
    data_ounce = []
    for tr in trs:
        d = {}
        pattern = r"[0-9]+"
        import re
        tds = tr.find_all('td')
        # print(tds[0].get_text().split())
        day_num = ''
        month = ''
        if len(tds[0].get_text().split()) > 1:
            day_num = re.search(pattern, tds[0].get_text().split()[1]).group(0)
            month , x = convert_date_str(tds[0].get_text().split()[1])
        date = convert_days_ar(tds[0].get_text().split()[0].split(',')[0]) + ' ' + day_num + ' ' + month
        d['date'] = date
        price = tds[1].get_text().split()[0].replace('€','')
        # print(price)
        d['price'] = price
        data_ounce.append(d)
        
    pd.DataFrame(data_ounce).to_csv('./static/goldprice/csv/history_of_ounce.csv', index=False)
  
# Gold price per karat
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

# Silver price per karat
def silver_price_data():
    links = [('eur',"https://www.livepriceofgold.com/silver-price/germany.html"),('usd',"https://www.livepriceofgold.com/silver-price/usa.html")]
    
    def karat(i):
        for j in range(7):
            if i == 1:
                karat = "سعر جرام الفضة عيار 999"
            elif i == 2:
                karat = "سعر جرام الفضة عيار 958"
            elif i == 3:
                karat = "سعر جرام الفضة عيار 925"
            elif i == 4:
                karat = "سعر جرام الفضة عيار 916"
            elif i == 5:
                karat = "سعر جرام الفضة عيار 875"
            elif i == 6:
                karat = "سعر جرام الفضة عيار 800"
            elif i == 7:
                karat = "سعر جرام الفضة عيار 585"
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
            d['kg'] = tds[0].get_text()
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
            d['tola'] = tds[0].get_text()
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
        
    pd.DataFrame(data_gram).to_csv('./static/goldprice/csv/silver_data_gram.csv', index=False)
    pd.DataFrame(data_onece).to_csv('./static/goldprice/csv/silver_data_ounce.csv', index=False)
    df.to_csv('./static/goldprice/csv/all_silver_unit.csv', index=False)
    
def get_listOf_sixmonth():
    df = pd.read_csv('./static/goldprice/csv/charts_data.csv')
    df_7_days = df.head(7)
    json_records4 = df.head(7).reset_index().to_json(orient ='records')
    historic_data = []
    historic_data = json.loads(json_records4)
    
    data = df.head(180)
    data = np.array_split(data, 6)
    list_month = []
    for d in data:
        dic = {}
        r_max, r_min = d.max(), d.min()
        month, x = convert_date(r_max['date'].split('-')[1])
        r_max['date'] = month + ' ' + r_max['date'].split('-')[2]
        # r_max['date'] = r_max['date'].replace(x, month)

        month, x = convert_date(r_min['date'].split('-')[1])
        r_min['date'] = r_min['date'].replace(x, month)
        dic['max_price_date'], dic['max_price'] = r_max['date'], r_max['price']
        dic['الاشهر'], dic['أعلى سعر'] = r_max['date'], r_max['price']
        dic['min_price_date'], dic['min_price'] = r_min['date'], r_min['price']
        list_month.append(dic)  
    return list_month, historic_data ,df_7_days

def get_listOf_oneyear():
    df = pd.read_csv('./static/goldprice/csv/charts_data.csv')
    data = df.head(365)
    data = np.array_split(data, 12)
    list_year = []
    for d in data:
        dic = {}
        r_max, r_min = d.max(), d.min()
        month, x = convert_date(r_max['date'].split('-')[1])
        r_max['date'] = month + ' ' + r_max['date'].split('-')[2]
        # r_max['date'] = r_max['date'].replace(x, month)

        month, x = convert_date(r_min['date'].split('-')[1])
        r_min['date'] = r_min['date'].replace(x, month)
        dic['max_price_date'], dic['max_price'] = r_max['date'], r_max['price']
        dic['الاشهر'], dic['أعلى سعر'] = r_max['date'], r_max['price']
        dic['min_price_date'], dic['min_price'] = r_min['date'], r_min['price']
        list_year.append(dic)  
    return list_year

# Historical Gold Price Chart in EUR
def gold_price_charts_data():
    url = "http://goldpricez.com/gold/history/eur/years-3"
    trs = make_soup(url).find_all('table')[1].find_all('tr')
    trs.pop(0)
    def data_list(data, data_days, number):
        for d in data:
            if number != 0:
                data_days.append(d)
            else:
                break
            number = number - 1
        return data_days
    data = []
    data_30 = []
    for tr in trs:
        tds = tr.find_all('td')
        date = tds[0].get_text()
        price = tds[1].get_text().split()[0]
        data.append({'date': date,"price":price})

    df_30 = pd.DataFrame(data_list(data, data_30, 30))
    make_chart(df_30,"date","price"," مخطط سعر الذهب خلال 30 أيام الماضية","./templates/goldprice/chart_30.html" ,marker=True)
   
    list_month, historic_data, df_7_days = get_listOf_sixmonth()
    df_six_month = pd.DataFrame(list_month)
    make_chart(df_7_days,"date","price","مخطط سعر الذهب خلال 7 أيام الماضية","./templates/goldprice/chart_7_days.html", marker=True)
    
    make_chart(df_six_month,"الاشهر","أعلى سعر","مخطط سعر الذهب خلال 6 أشهر الماضية","./templates/goldprice/chart_six_month.html", marker=True)
    
    list_oneyear = get_listOf_oneyear()
    df_oneyear = pd.DataFrame(list_oneyear)
    make_chart(df_oneyear,"الاشهر","أعلى سعر","مخطط سعر الذهب خلال السنة الماضية","./templates/goldprice/chart_oneyear.html", marker=True)
    
    # ounce chart for 15 days 
    df_oneyear = pd.read_csv("./static/goldprice/csv/history_of_ounce.csv")
    make_chart(df_oneyear,"date","price","سعر أونصة الذهب في الايام السابقة","./templates/goldprice/chart_ounce_15days.html", marker=True)
    
    df = pd.read_csv('./static/goldprice/csv/silver_chart_data.csv')
    make_chart(df,"date","gram","سعر غرام الفضة في الايام 90 السابقة","./templates/goldprice/chart_silver_gram.html", marker=True)

    
# Historical Silver Price Chart in EUR
def silver_chart_data():
    url = "https://www.bullion-rates.com/silver/EUR-history.htm"
    soup = make_soup(url)
    table = soup.find('table',{'id':'dtDGrid'})
    trs = table.find_all('tr')
    trs.pop(0)
    list = []
    
    for tr in trs:
        d = {}
        try:
            tds = tr.find_all('td')
            date = tds[0].get_text().split('-')[1]
            day = tds[0].get_text().split('-')[0]
            month, x = convert_date(date)
            date = day + ' ' + month
            d['date'] = date
            d['gram'] = tds[2].get_text()
            d['ounce'] = tds[1].get_text()
            list.append(d)
        except:
            pass
    df = pd.DataFrame(list)
    df.head(7).to_csv('./static/goldprice/csv/silver_chart_data.csv', index=False)
    make_chart(df.head(7),"date","gram","سعر غرام الفضة في الايام 7 السابقة","./templates/goldprice/chart_silvergrm_7days.html", marker=True)
    make_chart(df.head(7),"date","ounce","سعر أونصة الفضة في الايام 7 السابقة","./templates/goldprice/chart_silverounce_7days.html", marker=True)


def chart_data_ounce():
    url = "http://goldpricez.com/gold/history/eur/year-1"
    
    trs = make_soup(url).find_all('table')[1].find_all('tr')
    trs.pop(0)
    data = []
    for tr in trs:
        tds = tr.find_all('td')
        date = tds[0].get_text()
        price = tds[1].get_text().split()[0]
        data.append({'date': date,"price":price})
    
def index(request):
    now = datetime.now().strftime("%d %B %Y")
    time = datetime.now().strftime("%H:%M")
    month = now.split()[1]
    translated = GoogleTranslator(source='auto', target='ar').translate(month)
    date_now = now.replace(month,translated) 
    df = pd.read_csv('./static/goldprice/csv/data_gram.csv')
    data_eur = df.loc[df['currency'] == 'eur']
    data_usd = df.loc[df['currency'] == 'usd']
    
    json_records1 = data_eur.reset_index().to_json(orient ='records')
    data1 = []
    data1 = json.loads(json_records1)
    
    json_records2 = data_usd.reset_index().to_json(orient ='records')
    data2 = []
    data2 = json.loads(json_records2)
    
    df1 = pd.read_csv('./static/goldprice/csv/all_gold_unit.csv')
    data_eur1 = df1.loc[df1['currency'] == 'eur']
    data_usd1 = df1.loc[df1['currency'] == 'usd']
    
    json_records3 = data_eur1.reset_index().to_json(orient ='records')
    data3 = []
    data3 = json.loads(json_records3)
    
    json_records4 = data_usd1.reset_index().to_json(orient ='records')
    data4 = []
    data4 = json.loads(json_records4)
    
    
    
    list_month, historic_data, df_7_days= get_listOf_sixmonth()

    gram = data_eur['price'][0]
    #data_price = [data_eur['price'][0],data_eur['price'][1],data_eur['price'][2],data_eur['price'][3],data_eur['price'][4],data_eur['price'][5],data_eur['price'][6]]
    karat_22,karat_21,karat_18,karat_14,karat_10,karat_6 = data_eur['price'][1],data_eur['price'][2],data_eur['price'][3],data_eur['price'][4],data_eur['price'][5],data_eur['price'][6]
    
    posts = Post.objects.all()
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
        
    context = {
        'title': 'الصفحة الرئيسية',
        'date': date_now,
        'time': time,
        'data_eur_grm': data1,
        'data_usd_grm': data2,
        'data_eur_unit': data3,
        'data_usd_unit': data4,
        'historic_data': historic_data,
        'list_month': list_month,
        'gram': gram,
        'karat_22':karat_22,'karat_21':karat_21,'karat_18':karat_18,'karat_14':karat_14,'karat_10':karat_10,'karat_6':karat_6,
        'posts': posts,
    }
    return render(request, 'goldprice/index.html', context)


def gold_ounce(request):
    now = datetime.now().strftime("%d %B %Y")
    time = datetime.now().strftime("%H:%M")
    month = now.split()[1]
    translated = GoogleTranslator(source='auto', target='ar').translate(month)
    date_now = now.replace(month,translated) 
    
    df = pd.read_csv('./static/goldprice/csv/all_gold_unit.csv')
    data_eur = df.loc[df['currency'] == 'eur']
    data_usd = df.loc[df['currency'] == 'usd']
    json_records1 = data_eur.reset_index().to_json(orient ='records')
    data1 = []
    data1 = json.loads(json_records1)
    
    json_records2 = data_usd.reset_index().to_json(orient ='records')
    data2 = []
    data2 = json.loads(json_records2)
    
    df = pd.read_csv('./static/goldprice/csv/data_ounce.csv')
    data_eur = df.loc[df['currency'] == 'eur']
    data_usd = df.loc[df['currency'] == 'usd']
    
    karat_22,karat_21,karat_18,karat_14,karat_10,karat_6 = data_eur['ounce'][1],data_eur['ounce'][2],data_eur['ounce'][3],data_eur['ounce'][4],data_eur['ounce'][5],data_eur['ounce'][6]
    json_records1 = data_eur.reset_index().to_json(orient ='records')
    data3 = []
    data3 = json.loads(json_records1)
    
    json_records2 = data_usd.reset_index().to_json(orient ='records')
    data4 = []
    data4 = json.loads(json_records2)
    
    df = pd.read_csv('./static/goldprice/csv/history_of_ounce.csv')
    json_records = df.reset_index().to_json(orient ='records')
    data5 = []
    data5 = json.loads(json_records)
    
    posts = Post.objects.all()
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
        
    ounce = data_eur['ounce'][0]
    context = {
        'title': 'سعر اونص الذهب في ألمانيا اليوم',
        'date': date_now,
        'time':time,
        'ounce': ounce,
        'data_eur_unit': data1,
        'data_usd_unit': data2,
        'data_eur_ounce': data3,
        'data_usd_ounce': data4,
        'history_of_ounce': data5,
        'karat_22':karat_22,'karat_21':karat_21,'karat_18':karat_18,'karat_14':karat_14,'karat_10':karat_10,'karat_6':karat_6,
        'posts': posts,

        
    }
    return render(request, 'goldprice/gold_ounce.html', context)


def silver_price(request):
    now = datetime.now().strftime("%d %B %Y")
    time = datetime.now().strftime("%H:%M")
    month = now.split()[1]
    translated = GoogleTranslator(source='auto', target='ar').translate(month)
    date_now = now.replace(month,translated) 
    
    df = pd.read_csv('./static/goldprice/csv/all_silver_unit.csv')
    data_eur1 = df.loc[df['currency'] == 'eur']
    data_usd1 = df.loc[df['currency'] == 'usd']
    
    json_records = data_eur1.reset_index().to_json(orient ='records')
    data1 = []
    data1 = json.loads(json_records)
    
    json_records = data_usd1.reset_index().to_json(orient ='records')
    data2 = []
    data2 = json.loads(json_records)
    gram = data_eur1['gram'][0]
   
    
    df = pd.read_csv('./static/goldprice/csv/silver_data_gram.csv')
    data_eur = df.loc[df['currency'] == 'eur']
    data_usd = df.loc[df['currency'] == 'usd']
    
    karat_22,karat_21,karat_18,karat_14,karat_10,karat_6 = data_eur['price'][1],data_eur['price'][2],data_eur['price'][3],data_eur['price'][4],data_eur['price'][5],data_eur['price'][6]
    json_records1 = data_eur.reset_index().to_json(orient ='records')
    data3 = []
    data3 = json.loads(json_records1)
    
    json_records2 = data_usd.reset_index().to_json(orient ='records')
    data4 = []
    data4 = json.loads(json_records2)
    
    df = pd.read_csv('./static/goldprice/csv/silver_chart_data.csv', engine='python')
    json_records4 = df.reset_index().to_json(orient ='records')
    historic_data = []
    historic_data = json.loads(json_records4)
    
    posts = Post.objects.all()
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
        
    
    context = {
        'title': 'سعر الفضة في ألمانيا',
        'date': date_now,
        'time':time,
        'gram': gram,
        'data_eur_unit': data1,
        'data_usd_unit': data2,
        'data_eur_ounce': data3,
        'data_usd_ounce': data4,
        'karat_22':karat_22,'karat_21':karat_21,'karat_18':karat_18,'karat_14':karat_14,'karat_10':karat_10,'karat_6':karat_6,
        'historic_data':historic_data,
        'posts': posts,
        
    }
    return render(request, 'goldprice/silver_price.html', context)
