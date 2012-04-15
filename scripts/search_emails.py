#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

from django.core.management import setup_environ
sys.path.insert(0,PROJECT_PATH)
import settings
settings.DEBUG = False
settings.TEMPLATE_DEBUG = False
setup_environ(settings)

from BeautifulSoup import BeautifulSoup as BS
import urllib2
import re

def sanitizeUrl(url,root=None):
    
    import re

    if re.match(r"^https?://",url,re.I):
        # asuming full url
        return url
    
    elif not root:
        return "http://"+url
    
    elif re.match(r"^(\w+\.)?\w+\.\w{1,3}",url,re.I):
            # have domain
            return "http://"+url
    
    if not re.match(r"^https?://",root,re.I):
        root = "http://" + root
    
    
    return root + ("" if url[0]=="/" else "/") + url

def extractMainDomain(url):
    import re
    
    m = re.match(r"^(https?://)?(\w+\.)?(?P<domain>[\w-]+)\.\w{1,3}(/|$)",url,re.I)

    if m and m.group("domain"):
        return m.group("domain").lower()
    
    return None

def allowed_link(link):
     return not link is None and\
        link <> "" and\
        not link.startswith("#") and\
        not "javascript:" in link and\
        not "?p=" in link and\
        not "?cat=" in link and\
        not link.startswith("mailto:") and\
        not "about:blank" in link and\
        not link.startswith("http://platform.twitter.com/widgets/") and\
        not link.startswith("https://plusone.google.com/") and\
        not link.startswith("http://www.connect.facebook.com/") and\
        not link.startswith("http://www.facebook.com/") and\
        not link.startswith("http://mediacdn.disqus.com/") and\
        not link.startswith("http://platform0.twitter.com/widgets/") and\
        not link.startswith("http://api.connect.facebook.com/") and\
        not link == "/"

def scrap_email(url):

    emails=set()
    html=""
    
    print "->",url

    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 X11 Linux i686 AppleWebKit/535.19 KHTML, like Gecko Chrome/18.0.1025.151 Safari/535.19')
        response = urllib2.urlopen(request)
        

        html = response.read()

        for line in html.split('\n'):
            match = re.search(r'([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})', line, re.I)
            if match:
                print match.group(1)
                emails.add(match.group(1))
    
    except urllib2.HTTPError:
        pass
    except UnicodeEncodeError:
        pass
    
    return emails,html
    
#~ **************************************
#~ SCRIPT PRINCIPAL
#~ **************************************

from search_engine.models import *
#Recuperamos las empresas con web pero sin email
empresas = Empresa.objects.all().exclude(web="")

for empresa in empresas:
    if empresa.email.all().count() == 0:
        url=empresa.web
        print "Buscamos email de ", url
        
            
        urls_visitadas=set()
        
        emails,html=scrap_email(url)


        if emails:
            print emails
            print "Añadimos a la BD"
            for email in emails:
                empresa.email.create(email=email)
                empresa.save()

        else:
            bs = BS(html)
            
            for a in bs.findAll("a"):
                if a.get('href') and allowed_link(a.get('href')):
                    newurl = sanitizeUrl(a.get('href'),url)
        
                    if newurl in urls_visitadas:
                        continue
                    
                    urls_visitadas.add(newurl)
                    
                    if extractMainDomain(url) == extractMainDomain(newurl):
                        emails,html=scrap_email(newurl)
                        
                        if emails:
                            print emails
                            print "Añadimos a la BD"
                            for email in emails:
                                empresa.email.create(email=email)
                                empresa.save()
                            #Empresa(nombre=e.get('nombre'),web=e.get('url'),telefono=e.get('telefono'),direccion=e.get('direccion')).save()
            
for email in emails:
    print email
