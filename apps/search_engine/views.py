# coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import *

def home(request):
    empresas = Empresa.objects.all()
    return render_to_response('home.html', 
                                dict(empresas=empresas),   
                                context_instance = RequestContext(request))
