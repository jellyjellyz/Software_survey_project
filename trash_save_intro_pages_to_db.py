import requests
from bs4 import BeautifulSoup
import proxy_ip
import json
import time
import sqlite3
# time.sleep(1)

CACHE_FNAME = 'pages_cache.json' 

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

DBNAME = 'jobs.sqlite'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

no_detail_page_job_num_list = [78, 450, 493, 505, 535, 544, 611, 707, 768, 802, 856, 888, 1031, 1004, 1044, 1286, 1309, \
                                1331, 1391, 1402, 1573, 1614, 1638, 1677, 1730, 1806, 1835, 1858, 1861, 1868, 1938, \
                                1950, 1989, 2142, 2180, 2205, 2238, 2381, 2388, 2389]
baseurl = 'https://www.careerbuilder.com'
count = 0
c = 0
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
            # website = ajob.find(attrs = {"class": "job-title"}).find("a")["href"] 
            # job_location = ajob.find(name='div', attrs={"class": "columns end large-2 medium-3 small-12"})\
            #                             .find(name='h4', attrs={"class": "job-text"}).text
            job_info = ajob.find(name='h4', attrs={"class":'job-text employment-info'}).text.strip().split('|')
            count += 1
            if count not in no_detail_page_job_num_list:
                if len(job_info)==2:
                    job_payment = job_info[1].strip().replace(':','/').split('/')[1].strip()
                    job_payunit = job_info[1].strip().split('/')[-1]
                else:
                    job_payment = None
                    job_payunit = None
                job_type = job_info[0].strip()
                c += 1
                print('-'*10)
                print('Job{}'.format(count))
                # print(job_info)
                print(job_payment)
                print(job_type)
                print(job_payunit)
                # print(website)
                # print(job_title)
                # print(job_location)

                statement = '''
                UPDATE Jobs
                SET Jobtype = ?,
                    Payment = ?,
                    PayUnit = ?
                WHERE Id = ?
                '''
                params = (job_type, job_payment, job_payunit, c)
                cur.execute(statement, params)
                conn.commit()
            else:
                pass
        except:
            pass

    print("="*30)
conn.close()
# print(count)
# print(c)



