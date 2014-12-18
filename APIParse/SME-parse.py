#!/usr/bin/python
import urllib2
from BeautifulSoup import BeautifulSoup
import json
from os import _exit, fork 
from pandas import read_csv

def child(name, no , counter):
    comp_name_db = []
    fp = open("files/" + name,"w")
    fp.close()
    cp = open(counter,"w")
    cp.write("0")
    cp.close()
    print no 
    for i in range(no):
	url = "http://www.smelisting.com/categories/" + name
	if (i > 1):
	    url = url + "/" + str(i)
	print url 
	req = urllib2.urlopen(url)
	parsed_html = BeautifulSoup(req.read())
	data = parsed_html.body.findAll('div', attrs={'class':'search-result row'})
	for j in range(len(data)):
	    comp_name = data[j].findAll('span', attrs={'itemprop':'name'})
	    if len(comp_name):
		comp_name = comp_name[0].string
	    else:
		next
	    comp_desc = data[j].findAll('p', attrs={'class':'text-justify more'})
	    if len(comp_desc):
		comp_desc = comp_desc[0].string
	    else:
		comp_desc = ''
	    addr = data[j].findAll('span', attrs={'itemprop':'streetAddress'})
	    address = ''
	    for k in range(len(addr)):
		address += addr[k].string + "     \n"
	    comp_name_db.append({'name' : comp_name,
				 'desc' : comp_desc,
				 'addr' : address})
	fp = open("files/" + name,"w")
	print comp_name
	json.dump(comp_name_db, fp)
	fp.close()
	cp = open(counter,"w")
	cp.write(str(i))
	cp.close()
    _exit(0)

pd = read_csv('database')
print pd
for i in range(pd.name.size):
    newpid = fork()
    if newpid == 0:
        child(str(pd.name[i]), int(pd.no[i]), str(pd.counter[i]))
    
