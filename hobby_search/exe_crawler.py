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
import urllib
from  get_methods import *
"""
    SETTINGS
"""
date = datetime.datetime.now()
tstamp = '%04d%02d%02d%02d%02d%02d' % (date.year, date.month ,date.day,date.hour,date.minute,date.second)
#global ROOT_URL
ROOT_URL = "https://www.1999.co.jp"
URL = ROOT_URL +  "/search?typ1_c=101&cat=&state=&sold=0&sortid=0&searchkey=%E8%81%96%E9%97%98%E5%A3%AB%E6%98%9F%E7%9F%A2&spage="
OUT_F = 'data/figure_items_%s.csv' % tstamp
OUT_IMG_F = 'data/figure_items_images%s.csv' % tstamp
LOG_F  = r"./log/log_%s.log" % tstamp
NUM_PER_PAGE = 40
SLEEP_SEC =1
import urllib
KEYs = [
    "進撃の巨人",
    "僕のヒーローアカデミア ",
    "ジョジョ",
    "青春ブタ野郎はバニーガール先輩の夢を見ない",
    "七つの大罪",
    "転生したらスライムだった件",
    "シュタインズ・ゲート",
    "SAO",
    "BLEACH",
    "BORTO",
    "フェアリーテイル",
    "ラブライブ！",
    "炎炎ノ消防隊",
    "食戟のソーマ",
    "HUNTER×HUNTER",
    "ダンジョンに出会いを求めるのは間違っているだろうか",
    "盾の勇者の成り上がり",
    "アズールレーン",
    "攻殻機動隊",
    "カードキャプターさくら",
    "コードギアス",
    "カウボーイビバップ",
    "デート・ア・ライブ",
    "デジモン",
    "ファイナルファンタジー",
    "フルメタル・パニック!",
    "Gantz O",
    "銀魂",
    "天元突破グレンラガン",
    "ネプテューヌ",
    "けものフレンズ",
    "メイドインアビス",
    "魔法少女まどか☆マギカ",
    "ネコぱら",
    "NEW GAME!",
    "ノーゲーム・ノーライフ",
    "セーラームーン",
    "聖闘士星矢",
    "ドラゴンボール",
    "ワンピース",
    "エヴァンゲリオン",
    "仮面ライダー",
    "ナルト",
    "ホットトイズ",
    "超合金",
    "トランスフォーマー",
    "Vocaloid",
    "METAL BUILD",
    "鬼滅の刃",
    "デビルマン",
    "ハガレン",
    "Re:ゼロから始める異世界生活",
    "Fate",
    "艦隊これくしょん -艦これ-",
    "ごちうさ",
    "のんのんびより",
    "ゾンビランドサガ",
    "冴えない彼女の育てかた",
    "この素晴らしい世界に祝福を！",
    "とある魔術の禁書目録",
    "物語シリーズ",
    "THE IDOLM@STER",
    "ラブライブ！",
    "ガールズ・アンド・パンツァー",
    "アイカツ！",
    "バンドリ",
    "からかい上手の高木さん",
    "五等分の花嫁",
    "ベアブリック",
    "マクロス",
    "ゼノブレイド",
    "ゴブリンスレイヤー",
    "幼女戦記",
    "手品先輩",
    "ペルソナ"
]

if __name__ == '__main__':
    for key in KEYs:
        write_log(LOG_F,key)
        #if os.path.exists("./data/images/%s/" % key) == False:
        #    os.mkdir("./data/images/%s/" % key)
        search_key = urllib.parse.quote(key)
        URL = ROOT_URL +  "/search?typ1_c=101&cat=figure&state=&sold=0&sortid=0&searchkey={0}&spage=".format(search_key)
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
                        img_url = get_img_url(ROOT_URL + img_show_url , SLEEP_SEC)
                        img_info = [produ_id, jan_code, ROOT_URL + img_url]
                        write_info(OUT_IMG_F, img_info)
                except Exception as e:
                    write_log(LOG_F, "when executing get_img_url")
                    write_log(LOG_F, str(e) )
