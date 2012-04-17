# coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404,HttpResponse
from django.http import HttpResponseBadRequest
from django.template import RequestContext
from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.utils.encoding import smart_str
from scripts.linkedin import do_search,_profile_generator

from BeautifulSoup import BeautifulSoup as BS
import urllib2
import urllib
from models import *
import json
import scripts.pywhois as pywhois



def home(request):
    empresas = Empresa.objects.all()
    return render_to_response('home_back.html', 
                                dict(empresas=empresas),   
                                context_instance = RequestContext(request))

def home_old(request):
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
    company = ""
    
    if request.method == 'POST':
        company = request.POST.get('company','PideCurso')
    people=do_search(company=company)[1]
    
    persons=[p for p in _profile_generator(people)]
    

    return HttpResponse(dumps(persons), mimetype="application/json")
    
def linkedin_save(request):
    
    
    if request.method == 'POST':
        company_id = request.POST.get('id',None)
        
        if company_id:
            try:
                empresa = Empresa.objects.get(id=company_id)
                email=request.POST.get('email',None)
                if email:
                    if not empresa.email.filter(email=email).exists():
                        empresa.email.create(email=email)
                nombre_contacto = request.POST.get('nombre_contacto',None)
                if nombre_contacto:
                    empresa.nombre_contacto = nombre_contacto
                web = request.POST.get('web',None)
                if web:
                    empresa.web = web
                empresa.save()
            except Empresa.doesnotexist:
                pass
            
        else:
            raise KeyError
        
        return HttpResponse(serialize('json',[empresa]), mimetype="application/json")
    return HttpResponseBadRequest()


def google(request):
    
    if request.method == 'POST':
        query = request.POST.get('query',None)
        query = query.encode("ascii","replace")
        request = urllib2.Request("https://www.google.es/search?sourceid=chrome&ie=UTF-8&q="+urllib.quote(query)+"+-site%3Apaginasamarillas.es+-site%3A11870.com+-site%3Aes.qdq.com+-site.axesor.com&oq=%22Amadeus+Soluciones+Tecnologicas%22+sevilla++-site:paginasamarillas.es+-site%3A11870.com+-site%3Aes.qdq.com+-site.axesor.com")
        request.add_header('User-Agent', 'Mozilla/5.0 X11 Linux i686 AppleWebKit/535.19 KHTML, like Gecko Chrome/18.0.1025.151 Safari/535.19')
        response = urllib2.urlopen(request)
        html=response.read()
        u=BS(html)
        res=[]
        for h in u.findAll("h3"):
            link=dict()
            link['title']=' '.join(h.findAll('a')[0].findAll(text=True))
            link['href']=''.join(h.findAll('a')[0]['href'])
            aux=h.nextSibling
            if aux:#~ import ipdb
            #~ ipdb.set_trace()
                if len(aux.findAll("span"))>1:
                    link['desc']=''.join(aux.findAll("span")[1].findAll(text=True))
                res.append(link)
        #raise Exception(res)
        return HttpResponse(dumps(res), mimetype="application/json")
        
    else:
        return HttpResponseBadRequest()
        
def whois(request):
    
    if request.method == 'POST':
        w = pywhois.whois(request.POST.get('domain',"google.com"))
        res=dict()
        res['emails']=w.emails
        res['text']=w.text
        return HttpResponse(dumps([res]), mimetype="application/json")
    return HttpResponseBadRequest()
