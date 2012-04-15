# coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404,HttpResponse
from django.template import RequestContext
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.utils.encoding import smart_str
from scripts.linkedin import do_search
from models import *
import json
import ipdb
import sys
sys.setdefaultencoding('utf-8')

def home(request):
    empresas = Empresa.objects.all()
    return render_to_response('home.html', 
                                #dict(empresas=empresas),   
                                context_instance = RequestContext(request))

def empresas(request,ciudad):
    empresas = Empresa.objects.filter(ciudad=ciudad)
    #ipdb.set_trace()
    return HttpResponse(serialize('json',empresas), mimetype="application/json")

def linkedin_search(request):
    #Datos extraidos y cargados en el diccionario
    data=["id","first-name","last-name","public-profile-url","location","three-current-positions","primary-twitter-account"]
    people=do_search(company="PideCurso")[1]
    persons=[]
    for s in people:
        person=dict()
        for d in data:
            if s.getElementsByTagName(d):
                for n in s.getElementsByTagName(d)[0].childNodes:
                    if n.nodeType == n.TEXT_NODE:
                        person[d]=n.data
        persons.append(person)

    
    return render_to_response('linkedin.html', 
                                dict(results=persons),   
                                context_instance = RequestContext(request))
