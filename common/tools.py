import urllib.request as req
from bs4 import BeautifulSoup
from time import sleep
import csv


def write_log(file,str):
    f_logout = open(file,'a')
    f_logout.writelines(str + "\n")
    f_logout.close()

def write_info(f_name,info_list):
	
	f_out = open(f_name,'a')
	writer = csv.writer(f_out,lineterminator='\n')
	
	try:
		writer.writerow(info_list)

	except UnicodeEncodeError as e:
		print(e)
	
	finally:
		f_out.close()
	

# Request URL & get html
def get_soup(url,sleep_sec):

    try:
        # Not Local 
        res = req.urlopen(url)
        soup = BeautifulSoup(res,'html.parser')
        return soup

    except urllib.error.HTTPError as http_e:
        print( http_e.code , http_e.reason, url)
        log_str = str( http_e.code) + http_e.reason +  url
        write_log(LOG_F, str(http_e.code)  )
    finally:
        sleep(sleep_sec)