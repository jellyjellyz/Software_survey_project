import requests
from bs4 import BeautifulSoup
import proxy_ip
import json
import time
import sqlite3
import re

def make_request_using_cache(url, theheader, the_num_of_job):
    file_num = the_num_of_job//101
    CACHE_FNAME = './caches/detail_pages{}.json'.format(file_num)
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()

    except:
        CACHE_DICTION = {}

    unique_ident = url
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        pass

    print("Making a request for new data...")
    # Make the request and cache the new data
    iplists = proxy_ip.get_the_ip()
    theip = proxy_ip.get_random_ip(iplists)
    time.sleep(10)
    resp = requests.get(url, headers = theheader, proxies=theip)
    try:
        CACHE_DICTION[unique_ident] = str(resp.content, 'utf-8')
    except:
        CACHE_DICTION[unique_ident] = resp.text
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return CACHE_DICTION[unique_ident]

count = 0
FILENAME = './caches/detail_urls.text'
errorfile = open('./caches/error_url.text', "w")
detailurl_file = open(FILENAME, "r") 

for aurl in detailurl_file.readlines()[:10]:
    aurl = aurl[:-1]
    count += 1
    para = {'Referer': '{}'.format(aurl), \
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    resp = make_request_using_cache(aurl, para, count)
    soup = BeautifulSoup(resp, 'html.parser')

    company_name = soup.find(name="div", attrs={"class":"company-info-panel"})\
                        .find(name="div", attrs={"class":"company-info"}).find(name = "header").text.strip()
    # try:
    #     company_address = soup.find(name="div", attrs={"class":"company-info-panel"})\
    #                         .find(name="ul", attrs={"class":"address"}).find_all(name = "li").text
    # except:
    #     company_address = soup.find(name="div", attrs={"class":"company-info-panel"})\
    #                     .find(name="ul", attrs={"class":"address"}).find(name = "li").text
    # try:
    company_address_li = soup.find(name="div", attrs={"class":"company-info-panel"})\
                            .find(name="ul", attrs={"class":"address"}).find_all(name = "li")
    company_address = ''
    pattern = re.compile(r', \w{2}')

    for item in company_address_li:
        company_address += item.text.replace('\n', ' ').strip()
        if pattern.findall(item.text) != []:
            break



    # except:
    #     company_address = soup.find(name="div", attrs={"class":"company-info-panel"})\
    #                     .find(name="ul", attrs={"class":"address"}).find(name = "li").text

    print(company_name)
    print(company_address)
    print('='*20)


