#!/usr/bin/env python
import json
import requests
import cfscrape
import time

AFH_API_ENDPOINT = "https://androidfilehost.com/api/"
MAX_RETRIES = 5

errors = ""
_f=open('devices.json','w')
list_devices=[]

def count_pages():
    retries = 0
    scraper = cfscrape.create_scraper()
    payload={'action':'devices','limit':'1'}
    while True:
        data = []
        r = scraper.get(AFH_API_ENDPOINT, params=payload)
        try:
            data = r.json()
        except ValueError:
            if retries < MAX_RETRIES:
                retries += 1
                print r.content
                print "Error fetching number of pages. Retrying after 5s."
                time.sleep(5)
                continue
            else:
                errors += "Error: could not fetch number of pages\n"
                break
        temp_page_count = 0
#        try:
        temp_page_count = int(data['TOTALSz']['total_objects']
#        except:
#            errors += "Error: unexpected JSON in count_pages()\n"
#            break
        global PAGE_COUNT = 7
# (temp_page_count/100) + 1
        break

def fetch_devs(did):
    scraper = cfscrape.create_scraper()
    devs = []
    payload={'action':'developers','page':'1','limit':'1','did':did}
    data=scraper.get(AFH_API_ENDPOINT, params=payload).json()
    temp_dev_pages_count = (int(data['TOTALS']['total_objects'])/100) + 1
    while i <= temp_dev_pages_count:
        print "pass {0} of {1}".format(str(i),str(temp_dev_pages_count))
        payload={'action':'developers','page':i,'limit':'100','did':did}
        devs.extend(scraper.get(AFH_API_ENDPOINT,params=payload)).json()['DATA']
        time.sleep(3)
    return devs


def get_devices():
    scraper = cfscrape.create_scraper()
    i = 1
    while i <= PAGE_COUNT:
      print "pass {0} of {1}".format(str(i),str(PAGE_COUNT))
      payload={'action':'devices','limit':'100','page':i}
      r = scraper.get(AFH_API_ENDPOINT, params=payload)
      rJson = []
      try:
        rJson = r.json()['DATA']
      except ValueError:
        msg = "Error on page "
        msg += str(i)
        print msg
        print r.content
        time.sleep(5)
        # Retrying. So far, this has been a HTTP 502, and a retry fixes it
        # TODO: Check if it really is a 502, and set a MAX_RETRIES
        continue
      list_devices.extend(rJson)
      print "Currently synced down {0} devices!".format(str(len(list_devices)))
      i+=1
    json.dump(list_devices,_f,indent=2)

def get_developers():
    for i in list_devices:
        devs = fetch_devs(i['did'])
        _f = open(i['device_name'], 'w')
        json.dump(devs,_f,indent=2)

count_pages()
if 'PAGE_COUNT' in globals() && PAGE_COUNT >= 1:
    get_devices()
    get_developers()
print errors
