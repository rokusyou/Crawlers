import sys, os
sys.path.append(os.pardir)
from common.tools import *
import numpy as np
import math
import csv
import datetime
from bs4 import BeautifulSoup
import urllib.request as req
from time import sleep

from  get_methods import *
"""
    SETTINGS
"""
date = datetime.datetime.now()
tstamp = '%04d%02d%02d%02d%02d%02d' % (date.year, date.month ,date.day,date.hour,date.minute,date.second)
global ROOT_URL
ROOT_URL = "https://www.1999.co.jp"
URL = "https://www.1999.co.jp/search?typ1_c=101&cat=&state=&sold=0&sortid=0&searchkey=%E8%81%96%E9%97%98%E5%A3%AB%E6%98%9F%E7%9F%A2&spage="
OUT_F = 'data/figure_items_%s.csv' % tstamp
LOG_F  = r"./log/log_%s.log" % tstamp
NUM_PER_PAGE = 40
SLEEP_SEC =1

if __name__ == '__main__':
    write_log(LOG_F, "Search items page")
    write_log(LOG_F, str(datetime.datetime.now()) )
    soup = get_soup(URL, SLEEP_SEC)
    searched_num = soup.find('div',class_='list_kensu02').text.split(" ")[0]
    searched_product_num = int(searched_num)
    searched_page_num = math.ceil(searched_product_num / NUM_PER_PAGE)

    for i in range(1,searched_page_num+1):
        print("page No = %s" % i)
        write_log(LOG_F, "page No = %s" % i )
        write_log(LOG_F, str(datetime.datetime.now()) )
        page_url = URL   + str(i)
        page_soup = get_soup(page_url, SLEEP_SEC)

        for produ_nm in page_soup.findAll('div','a',class_='ListItemName'):
            produ_id = produ_nm.find('a').get("href")
            item_url = ROOT_URL + produ_id
            write_log(LOG_F, ROOT_URL + produ_id )
            item_soup = get_soup(ROOT_URL + produ_id,SLEEP_SEC)
            name  = get_name(item_soup)
            price = get_price(item_soup)
            price_normal = get_price_normal(item_soup)
            jan_code = get_jan_code(item_soup)
            maker, scale, material, prototype, series, original, release_date = get_details(item_soup)
            hight = get_hight(item_soup)
            size = get_size(item_soup)
            item_info = [produ_id,name, price,price_normal, jan_code, item_url, maker, scale, material, prototype, series, original, release_date,hight,size]
            write_info(OUT_F,item_info)
            img_list_soup = item_soup.find("div", id="ImageDetail")
            try:
                for url in img_list_soup.findAll('a'):
                    img_show_url = url.get("href" )
                    get_img(ROOT_URL + img_show_url, ROOT_URL , "./data/images/%s/" % produ_id, SLEEP_SEC)
            except Exception as e:
                write_log(LOG_F, "when executing get_img")
                write_log(LOG_F, str(e) )
