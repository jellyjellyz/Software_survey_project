import requests
from bs4 import BeautifulSoup
import proxy_ip
import json
import time


def make_request_using_cache(url, theheader, the_num_of_job):
    file_num = the_num_of_job//101
    CACHE_FNAME = 'detail_pages{}.json'.format(file_num)
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
count_error = 0
FILENAME = 'detail_urls.text'
errorfile = open('error_url.text', "w")
detailurl_file = open(FILENAME, "r") 
for aurl in detailurl_file.readlines():
    aurl = aurl[:-1]
    count += 1
    para = {'Referer': '{}'.format(aurl), \
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    resp = make_request_using_cache(aurl, para, count)
    soup = BeautifulSoup(resp, 'html.parser')
    job = soup.find(name="div", attrs={"class":"small-12 item"})
    print("-"*20)
    print("JOB {}:".format(count))
    try:
        print(job.text)
    except:
        errorfile.write(aurl + '\n')# job expired
        count_error += 1
    print("="*30)
print("{} Error occured.".format(count_error)) 