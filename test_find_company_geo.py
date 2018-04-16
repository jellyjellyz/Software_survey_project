import requests
import json
import plotly.plotly as py
from secrets import *

# google_places_key = 'AIzaSyAE0QigYI1lotM5qPpzsdgNo1c0uFhaiWU'
# google_url_text = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
google_url_text = "https://maps.googleapis.com/maps/api/geocode/json?"
# thequery = 'CAMP+Systems+International+Dover+NH'
thequery = 'New+York+City,NY'

search_params = {"key": google_places_key, "address": thequery}
# search_params = {"key": google_places_key, "type": "park", "query": thequery}


CACHE_FNAME = 'company_coordinate_test.json'
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
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)


def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        print("Making a request for new data...")
        resp = requests.get(baseurl, params)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION, indent = 4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() 
        return CACHE_DICTION[unique_ident]

# resp = requests.get(google_url_text, search_params).text
# resp = json.loads(resp)
resp = make_request_using_cache(google_url_text, search_params)
print(len(resp['results']))
print(resp['results'][0]['geometry'])


