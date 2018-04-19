######scrap all pages in https://www.careerbuilder.com with seach query 'software-engineer'
######save detail page url into ./caches/detail_urls.text

import requests
from bs4 import BeautifulSoup
import proxy_ip
import json
import time
# time.sleep(1)

CACHE_FNAME = './caches/pages_cache.json' 

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def make_request_using_cache(url, theheader):
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


if __name__ == '__main__':
    baseurl = 'https://www.careerbuilder.com'
    count = 0
    file = open("./caches/detail_urls.text", "w")
    for i in range(1, 101):
    # for i in range(1, 2):
        extendurl = baseurl + "/jobs-software-engineer?page_number={}".format(i)
        para = {'Referer': '{}'.format(extendurl), \
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        resp = make_request_using_cache(extendurl, theheader = para)
        # resp = requests.get(url, headers = para).text
        soup = BeautifulSoup(resp, 'html.parser')
        # print(soup.prettify())

        jobs = soup.find_all(name="div", attrs={"class":"job-row"})
        print("-"*20)
        print("Getting page {}".format(i))
        for ajob in jobs:
            try:
                job_title = ajob.find(attrs={"class": "job-title"}).text.strip()
                website = ajob.find(attrs = {"class": "job-title"}).find("a")["href"] 
                job_location = ajob.find(name='div', attrs={"class": "columns end large-2 medium-3 small-12"})\
                                            .find(name='h4', attrs={"class": "job-text"}).text
                count+=1
                print('-'*10)
                print('Job{}'.format(count))
                # print(website)
                print(job_title)
                print(job_location)
                
                file.write(baseurl + website + '\n')

            except:
                pass   # it's an ad not a job in that position
        print("="*30)
    file.close()
