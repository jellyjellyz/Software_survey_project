import sqlite3
import requests
import json
from secrets import *
import time

CACHE_FNAME = './caches/company_coordinate.json'
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


def make_request_using_cache(baseurl, params):
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

# resp = requests.get(google_url_text, search_params).text
# resp = json.loads(resp)
# resp = make_request_using_cache(google_url_text, search_params)
# print(len(resp['results']))

conn = sqlite3.connect('jobs.sqlite')
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
    search_params = {"key": google_places_key, "address": thequery}
    result = make_request_using_cache(google_url_text, search_params)
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
f = open('./caches/zero_reponse_query.json', 'w')
f.write(dumped_json)
f.close()

print(count_zero_return)
print(count)


