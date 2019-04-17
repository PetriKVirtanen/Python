import sqlite3
import time
import ssl
import json
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from urllib.parse import urlparse
import re
from datetime import datetime, timedelta

conn = sqlite3.connect('porssi.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Pelaaja')

cur.execute('''
CREATE TABLE Pelaaja (nimi TEXT, seura TEXT, ottelut INTEGER, tulos TEXT, til TEXT)''')

js_apu = list()
apikey = 'cd40f9b9a2ffbad8a57a0ef9ff8ce1b3'
#print('apikey = ', apikey)
if len(apikey) < 1 :
      print('apikey is invalid')
      quit()
else :
    #later you can add visual input here
    print('This print data from text tv page 223 and sub-pages')
    print('')
serviceurl = 'http://beta.yle.fi/api/ttvcontent/?a='+apikey+'&p=223&c=true'
#print('serviceurl = ', serviceurl)
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    team = input('ctrl + c quit ')
    count = 0
    looppi = 0
    alku = 6
    loppu = 12
    print('Retrieving', serviceurl)
    print('')
    uh = urllib.request.urlopen(serviceurl, None, 30, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    try:
        # Open with a timeout of 300 seconds
        if uh.getcode() != 200 :
            print("Error code=",uh.getcode(), serviceurl)
            break
        js = json.loads(data)
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        break
    except Exception as e:
        print("Unable to retrieve or parse page")
        print("Error",e)
        quit()
    #print('ladattu -----------------------------------------------------')
    #print(js["pages"])
    #print('Objektit ----------------------------------------------------')
    #print(json.dumps(js, indent=4))
    print('Sivu 233/3 ----------------------------------------------------')
    js_list = list(js.values())
    js_list = str(js_list)
    js_list = js_list.replace("[tgre]","")
    js_list = js_list.replace("[twhi]","")
    js_list = js_list.replace("[tcya]","")
    js_list = js_list.replace("\\n","")
    #print('kasitelty 1 : ', js_list)
    js_apu = js_list.split()
    x = js_apu.index("PISTEPÖRSSI")
    y = js_apu.index("MAALIVAHDIT")
    js_mod = js_apu[x:y]
    z = js_apu.index("'timestamp':")
    timeinfo = js_apu[z+1]
    print('Paivitetty :', timeinfo)
    xy = js_mod.index("'},")
    js_mod = js_mod[:xy]
    #print('kasitelty 2 : ', js_mod)
    #print(js_mod)
    print(js_mod[0], '(', js_mod[2], '', js_mod[3], '+', js_mod[4], '', js_mod[5],')')
    print('---------------------------------------------')
    while looppi < 20 :
        nimi = js_mod[alku] + ' ' + js_mod[alku + 1]
        #print (nimi)
        pisteet = ''
        for i in range (alku + 2, loppu) :
            # print(js_mod[i])
            pisteet = pisteet + js_mod[i] + ' '
        cur.execute('INSERT INTO Pelaaja (nimi, seura, ottelut, tulos, til) VALUES (?, ?, ?, ?, ?)', (nimi, js_mod[alku+2], js_mod[alku+3], js_mod[alku+4], js_mod[alku+5]))
        conn.commit()
        count = count + 1
        print(count, '. ', nimi,pisteet)
        print('---------------------------------------------')
        looppi = looppi + 1
        alku = alku + 6
        loppu = loppu + 6
cur.close()
