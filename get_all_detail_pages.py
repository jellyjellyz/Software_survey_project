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
c = 0
FILENAME = './caches/detail_urls.text'
errorfile = open('./caches/error_url.text', "w")
detailurl_file = open(FILENAME, "r") 

# # initialize database
DBNAME = 'jobs.sqlite'           
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
        # job_requirement = soup.find(name="div", attrs={"class":"description"}).find_all(name="ul")[1].text.strip().replace('\n', ',')

        if len(job_info) > 1:
            job_info = ','.join([ainfo.text.strip() for ainfo in job_info])
        else:
            job_info = job_info[0].text


        # print(job_company)
        # print(job_company)  # foreign key point to table company

        # print(job_info)
        # print(job_date) #post date
        # print(re.findall('\d+', job_date)[0])  #date(only number)
        # print(job_snapshot) 

        ####insert into db
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        statement = '''
            SELECT *
            FROM Company
            WHERE Name=? AND Region=? AND State=?
        '''
        params = (job_company[0], job_company[1], job_company[2])
        cur.execute(statement, params)
        result = cur.fetchall()
        if len(result) == 0:
            statement = '''
                INSERT INTO Company (Name, Region, State)
                VALUES (?, ?, ?)
            '''
            insertion = (job_company[0], job_company[1], job_company[2])
            cur.execute(statement, insertion)
            conn.commit()

        statement = 'INSERT INTO Jobs (Title, Jobtype, CompanyId, PostDate, JobSnapshot, JobDescription)'
        statement += ''' SELECT ?, ?, c.Id, ?, ?, ? '''
        statement += ' FROM Company as c'
        statement += ' WHERE c.Name=? AND c.Region=? AND c.State=?'

        insertion = (job_title, job_type, job_date, job_snapshot, job_info, job_company[0], job_company[1], job_company[2])
        cur.execute(statement, insertion)
        conn.commit()
        c += 1
        print("-"*20)
        print("JOB {}:".format(c))  # num of inserted jobs
        print(job_title)

    except Exception as e:
        error_num.append(count)
        print('ERROR:{}'.format(e))
        # print(statement)
        errorfile.write(aurl + '\n')# job expired
        count_error += 1
    print("="*30)

errorfile.close()
print("{} Error occured.".format(count_error)) 
print(error_num)


