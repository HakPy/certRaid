import json
import sys
import requests
from bs4 import BeautifulSoup

def doSubSearch(hostname):
    session = requests.Session()
    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0","Connection":"close","Accept-Language":"en-GB,en;q=0.5","Accept-Encoding":"gzip, deflate"}
    response = session.get("http://crt.sh/?q=%25.{}".format(hostname), headers=headers)
    soup = BeautifulSoup(response.content,"lxml")
    tables = soup.findAll('table')
    searchString = str(tables[0].find('td').contents[0])
    data = tables[2].findAll('tr')[1:]
    resultsDict = {}
    for x in range(0,len(data)):
        line = data[x].text.split('\n')
        while '' in line: line.remove('')
        id = line[0]
        loggedAt = line[1]
        notBefore = line[2]
        identity = line[3]
        issuer = line[4]
        #print id,'|',loggedAt,'|',notBefore,'|',identity,'|',issuer
        resultsDict[x] = {'id':id,'loggedAt':loggedAt,'notBefore':notBefore,'identity':identity,'issuer':issuer}
    return resultsDict

print 'obtaining results for:',sys.argv[1]
data = doSubSearch(sys.argv[1])
dataJSON = json.dumps(data)
with open(sys.argv[1]+'.txt', "w") as result_file:
    result_file.write(dataJSON)
