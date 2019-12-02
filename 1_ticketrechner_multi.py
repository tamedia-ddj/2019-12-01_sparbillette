import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime, timedelta
from time import strftime
from random import randint, shuffle
import re
from os import listdir
from random import shuffle
import concurrent.futures
import tqdm

# Grundeinstellungen
datenordner = '/mnt/rohdaten3/'
columns = ['datetime', 'datum', 'start', 'ziel', 'zeit', 'abfahrt', 'ankunft', 'dauer', 'umsteigen', 'belegung_1', 'belegung_2', 'zug', 'minimalpreis', 'sparticket', 'login', 'file']

def worker(f):
    try:
        n = 0
        s = BeautifulSoup(open(datenordner + f), 'lxml')

        # Die allgemeinen Daten zur Suche werden ausgelesen.  
        verbindungen = s.find_all('div', {'class': 'mod_accordion_item_heading'})

        start = s.find('span', {'class': 'mod_pagetitle_origin_destination'})
        start = start.text.replace('von', '').strip()

        ziel = s.find('span', {'class': 'mod_pagetitle_target_destination'})
        ziel = ziel.text.replace('nach', '').strip()

        t = s.find('h2', {'class': 'mod_pagesubtitle'}).find_all('span')[1].text.strip()
        datum = re.search(r'\d{2}.\d{2}.\d{4}', t)[0]
        zeit = re.search(r'\d{2}:\d{2}', t)[0]

        datetime = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', f)[0]

        if 'XYZ' in s.text: # Hier den Namen des Swisspass-Kontoinhabers einfügen.
            login = True
        else:
            login = False

        # Die Informationen zu den einzelnen Verbindungen werden ausgelesen. 
        discount_dict = dict()
        for i in range(len(verbindungen)):
            n += 1
            abfahrt = verbindungen[i].find('div', {'class': 'mod_timetable_starttime'}).find('span').text.strip()
            ankunft = verbindungen[i].find('div', {'class': 'mod_timetable_endtime'}).find('span').text.strip()
            dauer = verbindungen[i].find('div', {'class': 'mod_timetable_duration'}).find('span').text.strip()
            umsteigen = verbindungen[i].find('div', {'class': 'mod_timetable_change'}).find('p', {'role': 'presentation'}).text
            belegung = verbindungen[i].find('div', {'class': 'mod_timetable_occupancy'}).find_all('span', {'class': 'visuallyhidden'})
            zug = verbindungen[i].find('div', {'class': 'mod_timetable_connection'}).find_all('span', {'class': 'visuallyhidden'})[1].text
            # Bei Verbindungen in der ferneren Zukunft, werden keine Angaben zur Belegung mitgeliefert.
            if len(belegung) > 1:
                belegung1 = verbindungen[i].find('div', {'class': 'mod_timetable_occupancy'}).find_all('span', {'class': 'visuallyhidden'})[0].text
                belegung2 = verbindungen[i].find('div', {'class': 'mod_timetable_occupancy'}).find_all('span', {'class': 'visuallyhidden'})[1].text
            else:
                belegung1 = ''
                belegung2 = ''
            try:
                minimalpreis = float(re.search(r'CHF (\d{1,4}.\d{2}?)', verbindungen[i].find('span', {'class': 'mod_timetable_buy_button_label'}).text).group(1))
            except:
                minimalpreis = ''
            
            try:
                if verbindungen[i].find('div', {'class': 'mod_timetable_discountlabel'}) != None:
                    sparticket = True
                else:
                    sparticket = False
            except:
                sparticket = False

            # Ablegen der Informationen. 
            discount_dict[n] = [datetime, datum, start, ziel, zeit, abfahrt, ankunft, dauer, umsteigen, belegung1, belegung2, zug, minimalpreis, sparticket, login, f]
        return discount_dict

    except:
        pass


inventar = listdir(datenordner)

with concurrent.futures.ProcessPoolExecutor(16) as pool:
    results = list(tqdm.tqdm(pool.map(worker, inventar, chunksize=10), total=len(inventar)))

print('Alle Daten wurden verarbeitet.')

try:
    import pickle
    with open("daten/sparbillette_3.pkl","wb") as f:
        pickle.dump(results,f)
except:
    pass

print('\nEin DataFrame wird kreiert und abgespeichert.')
df = pd.DataFrame()
for i in tqdm.tqdm(list(results)): 
    try:
        df_temp = pd.DataFrame.from_dict(i, orient='index', columns=columns)
        df = df.append(df_temp)
    except:
        pass
df.to_csv('daten/sparbillette_3.csv')
print('Die Daten wurden abgespeichert.')
