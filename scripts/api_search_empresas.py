
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


from oosapy import AnonymousAuthentication, API
import json

from search_engine.models import *

CONSUMER_KEY = '2a4b1369527b4646ca74c5457d4e6a16' #appToken

oauth = AnonymousAuthentication(CONSUMER_KEY)
api = API(oauth)

#filename = 'empresas_malaga.json'
#~ parameters = [
                #~ "web",
                #~ "seo",
                #~ "marketing",
                #~ "programacion",
                #~ "usabilidad",
                #~ "diseno",
                #~ "lopd",
                #~ "android",
                #~ "iphone",
                #~ "phonegap"
            #~ ]
parameters = [
        "diseno-grafico",
        "marketing",
        "empresas-informatica"
        ]
ciudad = "sevilla"
              #"as": "/es/madrid"}

empresas=[]
#f=open(filename, 'wb')
for parameter in parameters:
    donde = "/es/"+ciudad
    results = api.search({"category":parameter,"as": donde})
    print 'Resultados con %s %s' % (parameter,len(results))
    for empresa in results:
        if not empresa in empresas:
            del empresa._api
            #empresas.append(empresa.__dict__)
            if not hasattr(empresa, 'url'):
                empresa.url=""
            if not hasattr(empresa, 'telephone'):
                empresa.telephone=""
            if not hasattr(empresa, 'useraddress'):
                empresa.useraddress=""
            empresas.append(dict(   nombre=empresa.name,
                                    url=empresa.url,
                                    telefono=empresa.telephone,
                                    direccion=empresa.useraddress
                                ))
        #print dibujante.name, dibujante.link,'\n', dibujante.telephone,'\n', dibujante.useraddress
#~ f.write(json.dumps(empresas))
print 'Total de empresas', len(empresas)

for e in empresas:
    e["nombre"]=e.get("nombre").strip()
    if Empresa.objects.filter(nombre=e.get('nombre')).count() == 0:
        if Empresa.objects.filter(web=e.get('url')).count() == 0:
            Empresa(nombre=e.get('nombre'),web=e.get('url'),telefono=e.get('telefono'),direccion=e.get('direccion'),ciudad=ciudad).save()

#~ f.close()


#~ for kk in empresas:
    #~ print kk.name,'\n', kk.link,'\n', kk.telephone,'\n', kk.useraddress

#~ 
#~ {'_api': <oosapy.api.API instance at 0xb73e742c>,
 #~ 'attributes': [],
 #~ 'categories': [],
 #~ 'country': u'Espa\xf1a',
 #~ 'id': 298999,
 #~ 'latitude': 37.378590000000003,
 #~ 'link': 'http://11870.com/pro/imadoc',
 #~ 'locality': 'Sevilla',
 #~ 'longitude': -5.9740799999999998,
 #~ 'name': 'Imadoc',
 #~ 'reviews_counter': 0,
 #~ 'saved_by': [],
 #~ 'saved_counter': 0,
 #~ 'slug': 'imadoc',
 #~ 'snapshots': [],
 #~ 'snippet': None,
 #~ 'subadministrativearea': 'Sevilla provincia',
 #~ 'tags': [],
 #~ 'telephone': '+34 954 66 03 80',
 #~ 'useraddress': 'Calle Carlos De Cepeda 2'}
