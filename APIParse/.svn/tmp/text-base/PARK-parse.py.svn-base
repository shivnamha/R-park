#!/usr/bin/python

# parse timescity webiste
# parse zomato.com

import requests 
from BeautifulSoup import BeautifulSoup 
import json
import os.path
from sys import exit

Data = {}
FILE1 = "parking_data.json"
FILE2 = "parking_review.json"

def write(data=Data,FILE=FILE1):
    FILE = "./" + FILE
    if os.path.exists(FILE):
        print FILE
        exit(0) 
    fp = open(FILE,"w")
    json.dump(data,fp, indent = 1)
    fp.close()

def parse_html( link='http://timescity.com/delhi/restaurant/parking-available-facility/'):
    headers = {'x-li-format': 'json', 'Content-Type': 'application/json'}
    kw = dict(headers=headers)
    try:
        req = requests.request('GET',link,**kw)
        return BeautifulSoup(req.content)
    except:
        return ""

def parse_timescity(parsed_html):
    uls =  parsed_html.body.find('ul', attrs={'id':'showMoredata_restaurant'})
    lis = uls.findAll('li')
    print len(lis)
    #{ id = {"Name": "Diva The Italian",
    #        "address": { "streetAddress": "",       
    #                     "addressLocality": "",
    #                     "postalCode":  "",
    #                     "addressRegion": "",
    #                     "nearbyplace": ""},
    #         "phoneNo" : "",
    #          "link": ""}  }
    # 
    for j in lis:
	if len(j.findAll('a')) <= 2:
	    continue
	link = str(j.findAll('a')[1]['href'])
	name = str(j.findAll('a')[1].string)
	Data[name] = { "Name": "Diva The Italian",
		       "address": { "streetAddress": "",       
				    "addressLocality": "",
				    "postalCode":  "",
				    "addressRegion": "",
				    "nearbyplace": ""},
		       "phoneNo" : "",
		       "link": ""
		      }
	Data[name]['Name'] = name
	Data[name]['link'] = link
	res_data = ""

	par_det = parse_html(link)
        if par_det == "":
            continue
	addr = par_det.body.find('span', attrs={'itemprop':'address'})
        tel  = par_det.body.find('span', attrs={'itemprop':'telephone'})
        near  = par_det.body.find('span', attrs={'itemprop':'name'})
       
	if addr is None or len(addr) <= 0:
	    continue
	Data[name]['address']['streetAddress'] = str(addr.find('span').string)
	locality = addr.findAll('meta')
	
	for k in locality:
	    if k["itemprop"] == "addressLocality":
		Data[name]['address']['addressLocality'] = k['content']
	    elif k["itemprop"] == "postalCode":
		Data[name]['address']['postalCode'] = k['content']
	    else:
		Data[name]['address']['addressRegion'] = k['content']

        if tel is None or len(tel.findAll('a')) <= 0:
            continue
        tel_a= tel.findAll('a')
        for i in tel_a:
            Data[name]['phoneNo'] += str(i['href']) + ","

        if near is None:
            continue 
        Data[name]['address']['nearbyplace'] = str(near.string) 

reviews = []
def parse_zomato(parsed_html):
    if parsed_html == "":
        return 
    uls = parsed_html.body.find('ol')
    rws =  uls.findAll('p', attrs= {"class":"dish_search_display"})
    for i in rws:
        reviews.append(i['title'])    
    write(reviews, FILE2)


def timescity():
    link = 'http://timescity.com/delhi/restaurant/parking-available-facility/'
    theature = "http://timescity.com/delhi/theatre/theatresearch?byfs=Parking+Available"
    night = "http://timescity.com/delhi/nightlife/parking-available-facility/?"
    for i in range(200,500):
	url = ""
	if i == 1:
	    url = link
	else:
	    url = link + "?pg=" + str(i)
	print url 
	cont = parse_html(url)
	if cont == "":
	    print "Null Content"
	    continue
	parse_timescity(cont)
	write()

def time():

    theature = "http://timescity.com/delhi/theatre/theatresearch?byfs=Parking+Available"
    night = "http://timescity.com/delhi/nightlife/parking-available-facility/?"
    for i in range(200,500):
	url = ""
	if i == 1:
	    url = link
	else:
	    url = link + "?pg=" + str(i)
	print url 
	cont = parse_html(url)
	if cont == "":
	    print "Null Content"
	    continue
	parse_timescity(cont)
	write()

def zomato(link = "https://www.zomato.com/ncr/restaurants?q=parking"):
    for i in range(1,45):
        if i == 1:
            url = link 
        else:
            url = link + "&page="  + str(i)
        print url
        parse_zomato(parse_html(url))
