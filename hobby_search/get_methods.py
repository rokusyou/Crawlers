import sys, os
sys.path.append(os.pardir)
from common.tools import *
from bs4 import BeautifulSoup
import urllib.request as req
from time import sleep
import requests

        
def get_name(soup):
    name =""
    try:
        name = soup.find('h2',class_='h2_itemDetail').text
    except:
        write_log(LOG_F, "when executing get_name")
        write_log(LOG_F, str(e) )
    finally:
        return name
    
def get_price(soup):
    price = ''
    try:
        soup = soup.find('tr',id="masterBody_trPrice")
        #print(soup)
        price = soup.find('span',class_="Price_Dai").text
        if '¥' in price:
            price = price.replace("\n","")
            price = price.replace("\r","")
            price = price.replace(" ","")
            price = price.split('(税')[0]
            price = price.replace("¥","").replace(",","")                    
    except:
        write_log(LOG_F, "when executing get_price")
        write_log(LOG_F, str(e) )
    finally:
        return price

def get_price_normal(soup):        
    price_normal = ''
    try:
        soup = soup.find('tr',id="masterBody_trPriceNormal")
        for td_soup in soup.findAll('td'):
                price_normal = td_soup.text
                if '¥' in price_normal:
                    price_normal = price_normal.split('(税')[0]
                    price_normal = price_normal.replace("¥","").replace(",","")                    
    except:
        write_log(LOG_F, "when executing get_price_normal")
        write_log(LOG_F, str(e) )
    finally:
        return price_normal


def get_jan_code(soup):
    jan_code = ""
    try:
        soup = soup.find('tr',id="masterBody_trJanCode")
        for jtest2 in soup.findAll('td'):
            jan_code = jtest2.text
            if jan_code.isdecimal():
                return jan_code
    except:
        write_log(LOG_F, "when executing get_jan_code")
        write_log(LOG_F, str(e) )
    finally:
        return jan_code

def get_hight(soup):
    hight =""
    try:
        for div in item_soup.find("div", id="masterBody_pnlItemExp").findAll("div"):
            if  "●全高：" in div.text:
                hight = div.text.split("●全高：")[1].split("\n")[0].replace("\n","").replace("\r","")[:20]
    except:
        write_log(LOG_F, "when executing get_hight")
        write_log(LOG_F, str(e) )
    finally:
        return hight

def get_size(soup):
    size =""
    try:
        for div  in soup.find("div", class_="txt14px").findAll("div",class_=""):
            size_str = div.text.replace("\r\n","")
            if "●サイズ：" in size_str:
                size = size_str.split("●サイズ：")[1]
    except:
        write_log(LOG_F, "when executing get_size")
        write_log(LOG_F, str(e) )
    finally:
            return size

        
def get_img(img_show_url, root_url, out_dir, sleep_sec):
    try:
        img_url = get_soup(img_show_url,sleep_sec).find("table", id="imgTarget").find("img")["src"]

        output_img_path = img_url.replace("/","_")
        img_url = root_url + img_url
        r = requests.get(img_url)
        if os.path.exists(out_dir) == False:
                os.mkdir(out_dir)
        with open( out_dir + output_img_path,'wb') as file: 
            file.write(r.content)
    except:
        write_log(LOG_F, "when executing get_img")
        write_log(LOG_F, str(e) )

def get_maker(soup):
    maker = ""
    try:
        maker = soup.find("a").text
    except:
        write_log(LOG_F, "when executing get_price")
        write_log(LOG_F, str(e) )
    finally:
        return maker

def get_details(soup):
    try:
        item_details_soup = soup.find("table", id="tblItemInfo")
        maker = scale = material = prototype = series = original = release_date = ""
        for td in item_details_soup.findAll("tr" ): 
            attri = td.text.replace("\n","").replace(" ","")
            if "メーカー：" in attri:
                maker = attri.replace("メーカー：","")
            elif "スケール：" in attri:
                scale = attri.replace("スケール：","")
            elif "素材：" in attri:
                material = attri.replace("素材：","")
            elif "原型制作：" in attri:
                prototype = attri.replace("原型制作：","")
                print("test")
            elif "シリーズ：" in attri:
                 series = attri.replace("シリーズ：","")
            elif "原作：" in attri:
                original  = attri.replace("原作：","")
            elif "発売" in attri and "日" in attri:
                 release_date = attri.split("：")[1]
    except Exception as e:
        write_log(LOG_F, "when executing get_details")
        write_log(LOG_F, str(e) )
    finally:
        details  = [maker, scale, material, prototype, series, original, release_date]
        return details
