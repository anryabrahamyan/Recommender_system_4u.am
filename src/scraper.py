"""
File containing the scraping logic for 4u.am
"""

from bs4 import BeautifulSoup
import grequests
import requests
from multiprocessing import Pool
import numpy as np
import re

import os
import pickle
from multiprocessing import Pool
from pathlib import Path

import grequests
from bs4 import BeautifulSoup
import pandas as pd

usable_cpus = (os.cpu_count() // 2) -1

CATEGORY_URLS = []

def strip_white_chars(text):
    return text.strip("\n").strip(" ")

def get_product_data(product_request_categ):
    """Function is responsible for scraping product data from 4U.am product content
    """
    product_request=product_request_categ[0]
    category = product_request_categ[1]
    try:
        soup = BeautifulSoup(product_request.content, 'html.parser')
        sp = soup.find_all("div", {"class": "info_container"})[0]

        product_data = {}
        product_data["product"] = sp.find('p', attrs={'class' : 'name_info'}).text

        brand_partner = sp.find_all('div', attrs={'class' : 'brand_partner'})
        product_data["item_code"] = brand_partner[0].span.strong.text
        product_data["store"] = strip_white_chars(brand_partner[1].find_all("span")[0].a.text)
        try:
            product_data["brand"] = strip_white_chars(brand_partner[1].find_all("span")[1].a.text)
        except:
            pass
        product_data["url"] = product_request.url
        product_data["price"] = strip_white_chars(sp.find("p", attrs={'class' : 'item_price'}).span.span.text)
        product_data["item description"] = strip_white_chars(sp.find("div", attrs={'id' : 'description'}).div.text)
        product_data["image url"] = soup.find("div", attrs={'class' : 'show_tumb'}).img["src"]
        product_data["category"] = category

        return product_data
    except:
        return dict()

def get_category_names():
    r = requests.get("https://4u.am/en/")
    soup = BeautifulSoup(r.content, 'html.parser')
    text = str(soup)
    return list(set(re.findall(r"\/en/category/([\w-]+)[\?|\"]\b", text)))
    
def extract_category_contents(category_names):
    rs = (grequests.get("https://4u.am/en/category/"+cat) for cat in category_names)
    return grequests.map(rs)

def extract_item_contents(item_urls):
    rs = (grequests.get("https://4u.am"+item) for item in item_urls)
    return grequests.map(rs)

def extract_item_urls(category_request):
    items = []
    soup = BeautifulSoup(category_request.content, 'html.parser')
    sp= soup.find_all('div', attrs={'class' : 'category_item'})
    for i in sp: items.append((i.find_all("a")[1]["href"],category_request.url.split("/")[-1]))
    return items

def extract_item_info(category_names):
    
    with Pool(5) as p:
        item_urls = p.map(extract_item_urls, extract_category_contents(category_names), chunksize=1)
        
    urls = [j[0] for i in item_urls for j in i]
    category = [j[1] for i in item_urls for j in i]
    item_contents = extract_item_contents(urls)

    zip_item_categ = list(zip(item_contents, category))

    with Pool(5) as p:
        result = p.map(get_product_data,zip_item_categ)
    
    return result

if __name__=='__main__':
    file_loc = Path(__file__).parent / 'data'
    #TODO missing category URLS
    category_names =  get_category_names()
    data = extract_item_info(category_names)
    pd.DataFrame(data).to_csv("data.csv",index=False)
    """
    sample output:
        [{'product': 'Մատանի «DF Project» արծաթյա №14',
        'item_code': 'N:051649',
        'store': 'DF project',
        'brand': 'DF Project',
        'url': 'https://4u.am/hy/product/matani-df-project-arcatya-no14',
        'price': '9,000',
        'item description': '925 հարգի արծաթյա մատանի:\nՉափը՝ կարգավորվող:\nՔարը՝ օնիքս։\nՔաշը՝ 3.5 գ։',
        'image url': 'https://static.4u.am/origin/product/1024/dejhlp-iRIAG78l4.jpg'},
        {'product': 'Բրոշ «LilmArt» աստղ',
        'item_code': 'N:006014',
        'store': 'LilmArt',
        'url': 'https://4u.am/hy/product/bros-lilmart-astg',
        'price': '4,400',
        'item description': 'Բրոշը ամբոջությամբ ձեռքի աշխատանք է:\n\n\nՔարերը`բյուրեղ:\n\n\nԵրկարությունը` 4 սմ: \n\n\nԿարող եք պատվիրել Ձեր ցանկացած չափի:',
        'image url': 'https://static.4u.am/origin/product/1024/0sTXJB1jHm82-zwM.jpg'},
        {'product': 'Թևնոց «SOKOLOV» 94050369',
        'item_code': 'N:074276',
        'store': 'Charm.am',
        'url': 'https://4u.am/hy/product/tevnoc-sokolov-94050369',
        'price': '13,900',
        'item description': 'Ապրանքանիշ` SOKOLOV\nՄետաղը՝ 925 հարգի արծաթ՝ ռոդիումապատ',
        'image url': 'https://static.4u.am/origin/product/1024/5uIfr0JyNob8-wzp.jpg'},
        {'product': 'Ականջօղեր «DF Project» լուսածին արծաթյա',
        'item_code': 'N:000719',
        'store': 'DF project',
        ...
        'store': 'THE BOX',
        'url': 'https://4u.am/hy/product/nver-tup-the-box-no85-mankakan-agjka-hamar',
        'price': '14,500',
        'item description': 'Նվեր-տուփը ներառում է՝ \n\n\n- Սանր մանկական \n- Հայելի \n- Կերամիկական բաժակ \n- Գունավոր թուղթ\n- Քանոն միաեղջյուրով\n- Վարդագույն միաեղջյուրով գրիչ\n- Նոթատետր սպիտակ փայլիկներով\n- Դակիչ միաղջյուրով\n- Մարշմելո 100 գրամ \n\n\n\n\nՏուփի չափերը՝  \nԵրկարությունը՝ 19 սմ \nԼայնությունը՝ 26 սմ\nԲարձրությունը՝ 10 սմ\n\nԱպրանքները ենթակա են փոփոխության համարժեք գնով եւ տեսքով ապրանքների հետ:',
        'image url': 'https://static.4u.am/origin/product/1024/Em3kAg3hhDY8406B.jpg'}]
    """
