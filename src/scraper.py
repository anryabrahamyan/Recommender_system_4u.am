"""
File containing the scraping logic for 4u.am
"""

import os
import pickle
from multiprocessing import Pool
from pathlib import Path

import grequests
from bs4 import BeautifulSoup

usable_cpus = (os.cpu_count() // 2) -1

CATEGORY_URLS = []

def strip_white_chars(text):
    return text.strip("\n").strip(" ")

def get_product_data(product_request):
    """Function is responsible for scraping product data from 4U.am product content
    """
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

    return product_data

def extract_category_contents(category_names):
    rs = (grequests.get("https://4u.am/hy/category/"+cat) for cat in category_names)
    return grequests.map(rs)

def extract_item_contents(item_urls):
    rs = (grequests.get("https://4u.am"+item) for item in item_urls)
    return grequests.map(rs)

def extract_item_urls(category_request):
    items = []
    soup = BeautifulSoup(category_request.content, 'html.parser')
    sp= soup.find_all('div', attrs={'class' : 'category_item'})
    for i in sp: items.append(i.find_all("a")[1]["href"])
    return items

def extract_item_info(category_names):
    with Pool(usable_cpus) as p:
        item_urls = p.map(extract_item_urls, extract_category_contents(category_names), chunksize=1)
    urls = [j for i in item_urls for j in i]

    with Pool(usable_cpus) as p:
        result = p.map(get_product_data,extract_item_contents(urls))

    return result

if __name__=='__main__':
    file_loc = Path(__file__).parent / 'data'
    #TODO missing category URLS
    data = extract_item_info(CATEGORY_URLS)

    with open("data.pkl", "wb") as f:
        pickle.dump(data,f)
