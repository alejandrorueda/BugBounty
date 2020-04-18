# -*- encoding: utf-8 -*-
'''
Notas:
Uso del servicio "http://httpbin.org/" para probar clientes HTTP.
Ver: 
https://www.hurl.it/
'''

import urllib, urllib2, requests, json

print "URLLib IP Service: "
response = urllib.urlopen('http://httpbin.org/ip')
print "Response Code: "+str(response.getcode())
print "Response: "+response.read()
print response.geturl()
for header, value in response.headers.items():
    print header+' : '+value

print "Requests Library tests."
responseGet = requests.get("http://httpbin.org/get")
responsePost = requests.post("http://httpbin.org/post")
responsePut = requests.put("http://httpbin.org/put")
responseDelete = requests.delete("http://httpbin.org/delete")

print "GET Request. Status code: "+str(responseGet.status_code)
print responseGet.text

print "POST Request. Status code: "+str(responsePost.status_code)
print responsePost.text

print "PUT Request. Status code: "+str(responsePut.status_code)
print responsePut.text

print "DELETE Request. Status code: "+str(responseDelete.status_code)
print responseDelete.text