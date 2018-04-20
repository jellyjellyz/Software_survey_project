####SAMPLE of data processing

import requests
from bs4 import BeautifulSoup
import proxy_ip
import json
import time
import sqlite3
import re
from secrets import *

#######part1: scrap intro pages################################################
print('Scraping first level page>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ')
CACHE_FNAME = './caches/sample_pages_cache.json' 

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def make_request_using_cache_intro(url, theheader):
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
    time.sleep(2)
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


baseurl = 'https://www.careerbuilder.com'
count = 0
file = open("./caches/sample_detail_urls.text", "w")
for i in range(1, 2):
    # extendurl = baseurl + "/jobs-software-engineer?page_number={}".format(i)
    extendurl = baseurl + "/landing/software-engineer?page_number={}".format(i)
    para = {'Referer': '{}'.format(extendurl), \
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    resp = make_request_using_cache_intro(extendurl, theheader = para)
    soup = BeautifulSoup(resp, 'html.parser')

    jobs = soup.find_all(name="div", attrs={"class":"job-row"})
    print("-"*20)
    print("Getting page {}".format(i))
    for ajob in jobs:
        try:
            job_title = ajob.find(attrs={"class": "job-title"}).text.strip()
            website = ajob.find(attrs = {"class": "job-title"}).find("a")["href"] 
            count+=1
            print('-'*10)
            print('Job{}'.format(count))
            print(job_title)
            
            file.write(baseurl + website + '\n')

        except:
            pass   # it's an ad not a job in that position
    print("="*30)
file.close()

######part2: scrap detail pages#################################################
print('Scraping detail level page>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ')

def make_request_using_cache(url, theheader, the_num_of_job):
    file_num = the_num_of_job//101   ######seperate cached pages into 25 cache files, with each file including 100 job_pages.
    CACHE_FNAME = './caches/sample_detail_pages{}.json'.format(file_num)
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
    time.sleep(2)
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

def create_new_table(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    statement = '''
        DROP TABLE IF EXISTS `Jobs`;
        DROP TABLE IF EXISTS `Company`;
        CREATE TABLE `Jobs` (
            `Id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `Title`	TEXT,
            `Jobtype`	TEXT,
            `CompanyId`	INTEGER,
            `PostDate`	TEXT,
            `JobSnapshot`	TEXT,
            `JobDescription`	TEXT
        );
        CREATE TABLE `Company` (
            `Id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            `Name`	TEXT,
            `Region` TEXT,
            `State` TEXT,
            `Address` TEXT,
            `GeoLat`	REAL,
            `GeoLon`	REAL
        );
    '''
    cur.executescript(statement)
    conn.close()

def init_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
    except Exception as e:
        print("An error occurred:", e.args[0])
        quit()

    statement = '''
    SELECT count(*) FROM sqlite_master WHERE name = 'Jobs'
    '''
    cur.execute(statement)
    numOftable_jobs = cur.fetchone()[0]
    statement = '''
    SELECT count(*) FROM sqlite_master WHERE name = 'Company'
    '''
    cur.execute(statement)
    numOftable_company = cur.fetchone()[0]

    if numOftable_jobs == 0 and numOftable_company == 0:
        create_new_table(db_name)
    else:
        user_command = input('Jobs&Company Table already exists. Delete?yes/no\n').lower().strip()
        if user_command == 'yes':
            statement = '''
                        DROP TABLE IF EXISTS `Jobs`;
                        DROP TABLE IF EXISTS `Company`;
                '''
            print('Deleting the table...')
            cur.executescript(statement)
            conn.commit()
            print('Creating new table...')
            create_new_table(db_name)
            conn.close()
        else:
            quit()



count = 0
count_error = 0
FILENAME = './caches/sample_detail_urls.text'
errorfile = open('./caches/sample_error_url.text', "w")
detailurl_file = open(FILENAME, "r") 

### initialize database
DBNAME = 'sample_jobs.sqlite'           
init_db(DBNAME)

error_num = []

for aurl in detailurl_file.readlines():
    aurl = aurl[:-1]
    count += 1
    para = {'Referer': '{}'.format(aurl), \
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
    resp = make_request_using_cache(aurl, para, count)
    soup = BeautifulSoup(resp, 'html.parser')


    try:
        job_title = soup.find_all(name="div", attrs={"class":"small-12 item"})[0].text.strip()
    except:
        continue  # skip expired jobs

    try:
        job_company = soup.find_all(name="div", attrs={"class":"small-12 item"})[1].\
                        find(name="h2", attrs={"id":"job-company-name"}).text.strip()\
                        .replace('\n', '').replace('•',';').replace(',',';').split(';')
        if len(job_company) > 3:
            # job_company = [','.join(job_company[:2])]+job_company[2:]
            job_company = [','.join(job_company[:2])]+[','.join(job_company[2:-1])]+[job_company[-1].strip()]
        elif len(job_company) < 3:
            job_company = [None]+job_company
        else:
            job_company[-1] = job_company[-1].strip()

        job_date = soup.find_all(name="div", attrs={"class":"small-12 item"})[1].\
                        find(name="h3", attrs={"id":"job-begin-date"}).text.strip()
        job_snapshot_list = soup.find(name="div", attrs={"class":"job-facts item"}).text.strip().replace('\n\n\n',', ').split(',')
        job_snapshot = ','.join(job_snapshot_list[1:])
        job_type = job_snapshot_list[0]
        job_info = soup.find_all(name="div", attrs={"class":"description"})


        company_name = soup.find(name="div", attrs={"class":"company-info-panel"})\
                    .find(name="div", attrs={"class":"company-info"}).find(name = "header").text.strip()

        company_address_li = soup.find(name="div", attrs={"class":"company-info-panel"})\
                        .find(name="ul", attrs={"class":"address"}).find_all(name = "li")
        company_address = ''
        pattern = re.compile(r', \w{2}')
        for item in company_address_li:
            company_address += item.text.replace('\n', ' ').strip()
            if pattern.findall(item.text) != []:
                break

        if len(job_info) > 1:
            job_info = ','.join([ainfo.text.strip() for ainfo in job_info])
        else:
            job_info = job_info[0].text.strip()

        ####insert into db
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        statement = '''
            SELECT count(*)
            FROM Company
            WHERE Name=? AND Region=? AND State=?
        '''
        params = (company_name, job_company[1], job_company[2])
        cur.execute(statement, params)
        result = cur.fetchall()
        if result[0][0] == 0:
            statement = '''
                INSERT INTO Company (Name, Region, State, Address)
                VALUES (?, ?, ?, ?)
            '''
            insertion = (company_name, job_company[1], job_company[2].upper(), company_address)
            cur.execute(statement, insertion)
            conn.commit()

        statement = 'INSERT INTO Jobs (Title, Jobtype, CompanyId, PostDate, JobSnapshot, JobDescription)'
        statement += ''' SELECT ?, ?, c.Id, ?, ?, ? '''
        statement += ' FROM Company as c'
        statement += ' WHERE c.Name=? AND c.Region=? AND c.State=?'

        insertion = (job_title, job_type, job_date, job_snapshot, job_info, company_name, job_company[1], job_company[2])
        cur.execute(statement, insertion)
        conn.commit()

        print("-"*20)
        print(job_title)

    except Exception as e:
        error_num.append(count)
        print('ERROR:{}'.format(e))
        # print(statement)
        errorfile.write(aurl + '\n')# job expired
        count_error += 1
    print("="*30)

errorfile.close()
detailurl_file.close()
print("{} Error occured.".format(count_error)) 
print(error_num)


#######part3: get geometry coordinate for each company##########################
print('Getting geometry coordinate>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ')

CACHE_FNAME = './caches/sample_company_coordinate.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        if k != 'key':
            res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


def make_request_using_cache_geo(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        time.sleep(1)
        resp = json.loads(requests.get(baseurl, params).text)
        CACHE_DICTION[unique_ident] = resp
        if resp['status'] == 'OVER_QUERY_LIMIT':
            print('OVER_QUERY_LIMIT   CHANGE AN API KEY!!!!!!!!!!!!!!!!!!!!!!!!')
            print(count_zero_return)
            print(count)
            quit()
        print('>>>>>{}<<<<<'.format(resp['status']))
        dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() 
        return CACHE_DICTION[unique_ident]


conn = sqlite3.connect('sample_jobs.sqlite')
cur = conn.cursor()

statement = '''
    SELECT Name, Address, Id
    FROM Company
'''

cur.execute(statement)
result = cur.fetchall()
google_url_text = "https://maps.googleapis.com/maps/api/geocode/json?"
count_zero_return = 0
count = 0
zero_resp_query = {}
for aresult in result:
    count += 1
    thequery = aresult[1].replace(' ', '+')
    search_params = {"key": google_geo_key, "address": thequery}
    result = make_request_using_cache_geo(google_url_text, search_params)
    num_result = len(result['results'])
    print("-"*10)
    print(thequery)
    print(num_result)
    if num_result == 0:
        count_zero_return += 1
        zero_resp_query['{}'.format(aresult[-1])] = thequery
    try:
        lat = result['results'][0]['geometry']['location']['lat']
        lon = result['results'][0]['geometry']['location']['lng']
        statement = '''
            UPDATE Company
            SET GeoLat = {}, GeoLon = {}
            WHERE Id = {}
        '''.format(lat, lon, aresult[-1])
        cur.executescript(statement)
    except:
        continue

dumped_json = json.dumps(zero_resp_query, indent = 4)
f = open('./caches/sample_zero_reponse_query.json', 'w')
f.write(dumped_json)
f.close()


