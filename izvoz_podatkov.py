import csv
import requests
import re
import json
from datetime import date
todays_date = date.today()
leto = todays_date.year

def dobi_linke(url):
    linki = []
    html = requests.get(url).text
    a = re.findall(r'<a class="bb-xs pb-xs-1_1 pl-xs-1 g-xs-6 g-sm-3 g-md-2 g-lg-2 justify-left" href="https://www\.fis-ski\.com/DB/general/results\.html\?sectorcode=JP&raceid=[0-9][0-9][0-9][0-9]', html)
    for i in range(len(a)):
        linki.append(a[i].split('href="')[1])
    return linki

def zapisi_linke(tab_linkov, ime_dat):
    with open(ime_dat, 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(tab_linkov)):
            writer.writerow([tab_linkov[i]])

def dobi_podatek(url, isci, razdeli):
    podatek = []
    html = requests.get(url).text
    a = re.findall(isci, html)
    for i in range(len(a)):
        podatek.append(a[i].split(razdeli)[1])
    return podatek

tab_linkov = dobi_linke('https://www.fis-ski.com/DB/general/statistics.html?statistictype=positions&positionstype=position&offset=50&sectorcode=JP&seasoncode=&categorycode=OWG&gendercode=W&competitornationcode=&place=&nationcode=&position=4&disciplinecode=NH,LH')
zapisi_linke(tab_linkov, 'linki_olimpijske.csv')

tab_linkov = dobi_linke('https://www.fis-ski.com/DB/general/statistics.html?statistictype=positions&positionstype=position&offset=50&sectorcode=JP&seasoncode=&categorycode=WSC&gendercode=W&competitornationcode=&place=&nationcode=&position=4&disciplinecode=NH,LH')
zapisi_linke(tab_linkov, 'linki_svetovno_prvenstvo.csv')

tab_linkov = []
for i in range(2012,leto+1):
    url = 'https://www.fis-ski.com/DB/general/statistics.html?statistictype=positions&positionstype=position&offset=200&sectorcode=JP&seasoncode=' + str(i) + '&categorycode=WC&gendercode=W&competitornationcode=&place=&nationcode=&position=4&disciplinecode=NH,LH'
    tab_linkov += dobi_linke(url)
zapisi_linke(tab_linkov, 'linki_svetovni_pokal.csv')

def pridobi_podatke(ime_dat, vse_skakalnice = [], vse_kratice = set(), tekmovalke = {'id_tekmovalke': ['ime_priimek', 'letnica_rojstva', 'drzava']}, tekme = dict(), rezultati = dict(), datumi = dict(), r = 1):
    rezultati_posamezne_tekme = dict()
    meseci = {'November': '11', 'December': '12', 'January': '1', 'February': '2', 'March': '3'}
    tip_tekmovanja = {'Olympic Winter Games': 'olimpijske igre', 'World Ski Championships':'svetovno prvenstvo', 'World Cup':'svetovni pokal'}
    with open(ime_dat, 'r') as file:
        csvreader = csv.reader(file)
        for vrstica in csvreader:
            url = vrstica[0]
            html = requests.get(url).text
            kraj_in_kratica = dobi_podatek(url, r'<h1 class="heading heading_l2 heading_white heading_off-sm-style">[a-zA-Z\s()-]+', '">')[0]
            kraj = kraj_in_kratica[:-6]
            kratica_drzave = kraj_in_kratica[-4:-1]
            ang_vrsta_tekmovanja = dobi_podatek(url, r'<div class="event-header__subtitle">[a-zA-Z\s]+', '">')[0]
            if 'World Cup' in ang_vrsta_tekmovanja:
                ang_vrsta_tekmovanja = 'World Cup'
            vrsta_tekmovanja = tip_tekmovanja[ang_vrsta_tekmovanja]
            velikost = dobi_podatek(url, r'<div class="event-header__kind">Women\'s HS[0-9]+', 'HS')[0]
            c = dobi_podatek(url, r'<span class="date__full">[a-zA-Z\s0-9,]+', '">')[0].split(' ')
            datum = str(int(c[1][:-1])) + '.' + meseci[c[0]] + '.' + c[2]
            datumi[datum] = r
            if int(meseci[c[0]]) > 3:
                sezona = c[2]+'/'+str(int(c[2])+1)
            else:
                sezona = str(int(c[2])-1)+'/'+c[2]
            tekme[datum] = [vrsta_tekmovanja, '', sezona, kraj, velikost]
            if [kraj, kratica_drzave, velikost] not in vse_skakalnice:
                vse_skakalnice.append([kraj, kratica_drzave, velikost])
            vse_kratice.add(kratica_drzave)
            id_tekmovalke = dobi_podatek(url, r'<div class="g-lg-2 g-md-2 g-sm-2 hidden-xs justify-right gray pr-1">[0-9]+', '>')
            #ime_priimek = dobi_podatek(url, r'<div class="g-lg g-md g-sm g-xs justify-left bold">\s+[a-zA-Z\S]+\s[a-zA-Z\S]+\s?[a-zA-Z\S]+', '\n                                ')
            ime_priimek = dobi_podatek(url, r'<div class="g-lg g-md g-sm g-xs justify-left bold">\s+[a-zA-Z\S]+\s?[a-zA-Z\S]+\s?\s?[a-zA-Z\S]+', '\n                                ')
            mesto = dobi_podatek(url, r'<div class="g-lg-1 g-md-1 g-sm-1 g-xs-2 justify-right pr-1 gray bold">[0-9]+', '>')
            l_rojstva = dobi_podatek(url, r'\s+</div>\s+<div class="g-lg-1 g-md-1 g-sm-2 g-xs-3 justify-left">[0-9]+', '">')
            kratica_drzave_tek = dobi_podatek(url, r'<div class="country country_flag">\s+<span class="country__flag">\s+<span class="flag-[A-Z][A-Z][A-Z]\sflag"></span>\s+</span>\s+<span class="country__name-short">[A-Z]+', '<span class="country__name-short">')
            for i in range(len(id_tekmovalke)):
                if kratica_drzave_tek[i] == 'ROC' or kratica_drzave_tek[i] == 'RSF':
                    kratica_drzave_tek[i] = 'RUS'
                vse_kratice.add(kratica_drzave_tek[i])
                if id_tekmovalke[i] not in tekmovalke:
                    tekmovalke[id_tekmovalke[i]] = [ime_priimek[i], l_rojstva[i], kratica_drzave_tek[i]]
                if i >= len(mesto):
                    rezultati_posamezne_tekme[id_tekmovalke[i]] = ''
                if not(i >= len(mesto)):
                    rezultati_posamezne_tekme[id_tekmovalke[i]] = mesto[i]
            rezultati[datum] = rezultati_posamezne_tekme
            rezultati_posamezne_tekme = {}
            r += 1
    return vse_skakalnice, vse_kratice, tekmovalke, tekme, rezultati, datumi, r


vse_skakalnice, vse_kratice, tekmovalke, tekme, rezultati, datumi, r = pridobi_podatke('linki_olimpijske.csv', [], set(), {'id_tekmovalke': ['ime_priimek', 'letnica_rojstva', 'drzava']}, dict(), dict(), dict(), 1)
vse_skakalnice, vse_kratice, tekmovalke, tekme, rezultati, datumi, r = pridobi_podatke('linki_svetovno_prvenstvo.csv', vse_skakalnice, vse_kratice, tekmovalke, tekme, rezultati, datumi, r)
vse_skakalnice, vse_kratice, tekmovalke, tekme, rezultati, datumi, r = pridobi_podatke('linki_svetovni_pokal.csv', vse_skakalnice, vse_kratice, tekmovalke, tekme, rezultati, datumi, r)

###########################################################################################
id_skakalnic = dict()
prva_vrstica = ['id_skakalnice', 'kraj', 'velikost', 'drzava', 'tip_skakalnice']
nepravilne_velikosti = [['Zao','JPN','100'],['Zao','JPN','106'],['Zao','JPN','103'], ['Lillehammer','NOR','98'], ['Hinzenbach','AUT','90'], ['Ljubno','SLO','95'], ['Chaikovsky','RUS','106'], ['Rasnov','ROU','100'], ['Nizhny Tagil','RUS','100']] 
i = 1
#vse_skakalnice = ...
with open('skakalnice2.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(prva_vrstica)
    for skakalnica in vse_skakalnice:
        if skakalnica not in nepravilne_velikosti:
            if int(skakalnica[2]) >= 110:
                tip = 'velika'
            else:
                tip = 'srednja'
            kraj, drzava, velikost = skakalnica
            id_skakalnic[kraj, velikost] = i
            vrstica1 = i, kraj, velikost, drzava, tip
            writer.writerow(vrstica1)
            i += 1

###########################################################################################
#tekmovalke = ...
with open('tekmovalke2.json', 'w', encoding='UTF8', newline='') as file:
    niz = json.dumps(tekmovalke)
    file.write(niz)

###########################################################################################
#tekme = {'datum': ['tekmovanje', 'skakalnica', 'sezona', 'kraj', 'velikost']} 
#datumi = {'datum': id}
popravljanje_velikosti = {('Zao','100'): ('Zao','102'), ('Zao','106'): ('Zao','102'), ('Zao','103'): ('Zao','102'), ('Lillehammer','98'): ('Lillehammer','100'),
                      ('Hinzenbach','90'): ('Hinzenbach','94'), ('Ljubno','95'): ('Ljubno','94'), ('Chaikovsky','106'): ('Chaikovsky','102'),
                      ('Rasnov','100'): ('Rasnov','97'), ('Nizhny Tagil','100'): ('Nizhny Tagil','97')}
tekme_nove = {'id_tekme': ['datum', 'tekmovanje', 'skakalnica', 'sezona']}
with open('tekme2.json', 'w', encoding='UTF8', newline='') as file:
    for kljuc, vrednost in tekme.items():
        if (vrednost[3], vrednost[4]) in popravljanje_velikosti:
            id_dodaj = id_skakalnic[popravljanje_velikosti[vrednost[3], vrednost[4]]]
        else:
            id_dodaj = id_skakalnic[vrednost[3], vrednost[4]]
        tekme_nove[datumi[kljuc]] = [kljuc, tekme[kljuc][0], id_dodaj, tekme[kljuc][2]]
    jsonString = json.dumps(tekme_nove)
    file.write(jsonString)

###########################################################################################   
#rezultati = {'datum': {'mesto':'tekmovalka'}}
prva_vrstica = ['mesto', 'tekmovalka', 'tekma']
with open('rezultati2.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(prva_vrstica)
    for kljuc, vrednost in rezultati.items():
        for kljuc1, vrednost1 in vrednost.items():
            vrstica = vrednost1, kljuc1, datumi[kljuc]
            writer.writerow(vrstica)
            