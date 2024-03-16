import httpx
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup 
import requests
import pandas


result = []

def get_data(Store , Url , Tag_Price , Selector ,Tag_Name,Product_name_classe):
    global result
    response = requests.get(url=Url,headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 "
                  "Safari/537.36"})
    
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    prices = soup.find_all(Tag_Price,class_=Selector)
    Product_names = soup.find_all(Tag_Name,class_=Product_name_classe)
    for price in prices :
        for product in Product_names:
            try:
                Pname = product.find('span').text
            except AttributeError:
                Pname = product.text
            result.append({'store':Store,'Product':Pname,'price':price.text})


get_data('Ebay','https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=Rtx+4070&_sacat=0','span',"s-item__price",'div','s-item__title')
get_data('Aliexpress','https://fr.aliexpress.com/w/wholesale-rtx-4070.html?spm=a2g0o.home.history.1.1a6a7065roQwvV','div','multi--price-sale--U-S0jtj','h3','multi--titleText--nXeOvyr')
Dframe = pandas.DataFrame(result)
Dframe.dropna()
df = Dframe[Dframe.apply(lambda row: not any('#' in value for value in row), axis=1)]
df.to_csv('DATA-Scraped.csv',index=False)