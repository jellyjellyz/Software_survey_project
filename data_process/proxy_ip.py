from bs4 import BeautifulSoup
from datetime import datetime
import requests
import random
import json

def get_new_ip_list():
    print("Getting new proxy IP table...")
    url = 'https://www.sslproxies.org/'
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    html = requests.get(url=url, headers=headers).text
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    ips = soup.find(id='list').find_all('tr')
    ip_list = []
    for i in range(1, len(ips)-1):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        # print(tds[0])
        # print(tds[1])
        # print(tds[2])
        ip_list.append(tds[0].text + ':' + tds[1].text)
    # print("Got IP table.")
    return ip_list

def get_random_ip(ip_list):
    print("Setting random proxy IP...")
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)  
    proxies = {'http': proxy_ip}
    # print("Successful setting.")
    return proxies


def get_the_ip():
    IP_LIST_NAME = "ip_list.json"
    try:
        cache_file = open(IP_LIST_NAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    if CACHE_DICTION != {}:
        MAX_STALENESS = 1200    # refresh every 20 minutes
        now = datetime.now().timestamp()
        staleness = now - CACHE_DICTION['cache_timestamp']
        if staleness < MAX_STALENESS:
            print('Getting cached ip list...')
            return CACHE_DICTION['the_ips']
        else:
            pass
    print('Requesting new ip list...')
    the_ips = get_new_ip_list()
    CACHE_DICTION['cache_timestamp'] = datetime.now().timestamp()
    CACHE_DICTION['the_ips'] = the_ips
    dumped_json_cache = json.dumps(CACHE_DICTION)
    fw = open(IP_LIST_NAME, "w")
    fw.write(dumped_json_cache)
    fw.close() # Close the open file
    return the_ips

        
if __name__ == '__main__':
    iplists = get_the_ip()
    # print(iplists)
    theip = get_random_ip(iplists)
    print(theip)