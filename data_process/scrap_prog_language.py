#####scrap top100+ popular programming languages from https://www.whoishostingthis.com/resources/programming/
###save top100+ popular programming languages into prog_language.txt
import requests
import json
from bs4 import BeautifulSoup

CACHE_FNAME = './caches/programming_language_page.json' 

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def make_request_using_cache(url):
    unique_ident = url
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        pass

    print("Making a request for new data...")
    # Make the request and cache the new data
    resp = requests.get(url)
    try:
        CACHE_DICTION[unique_ident] = str(resp.content, 'utf-8')
    except:
        CACHE_DICTION[unique_ident] = resp.text
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(CACHE_FNAME,"w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return CACHE_DICTION[unique_ident]

prog_language = []
theurl = 'https://www.whoishostingthis.com/resources/programming/'
resp = make_request_using_cache(theurl)
soup = BeautifulSoup(resp, 'html.parser')
sections = soup.find(name = 'dl')
languages = sections.find_all(name = 'dt')
for language in languages:
    prog_language.append(language.string.lower())


print(prog_language)
f = open('prog_language.txt', 'w')
f.write('\n'.join(prog_language))
f.close()