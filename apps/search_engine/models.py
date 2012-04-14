# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Empresa(models.Model):
    nombre = models.CharField(_(u"Nombre *"), max_length=128,blank=True)
    nombre_contacto = models.CharField(_(u"Nombre persona de contacto *"), max_length=128)
    apellidos_contacto = models.CharField(_(u"Apellidos persona de contacto"), max_length=128, blank=True)
    email = models.EmailField(_(u"Email *"),blank=True)
    ciudad = models.CharField(_(u"Ciudad"), max_length=128,blank=True)
    direccion = models.TextField(_(u"Dirección"), blank=True)
    telefono = models.CharField(_(u"Teléfono"), blank=True, max_length=32)
    web = models.URLField(_(u"Web"), blank=True)
    
    #~ empleados=models.ForeignKey('places.City', verbose_name=_(u"Ciudad *"),
                               #~ related_name='+')
    
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.nombre)
    
    def __str__(self):
        return self.__unicode__()
        
class Empleados(models.Model):
    nombre = models.CharField(_(u"Nombre"), max_length=128)
    apellidos = models.CharField(_(u"Apellidos"), max_length=256)
    cargo = models.CharField(_(u"Cargo"), max_length=256)
    
    def __unicode__(self):
        return unicode(self.nombre)
    
    def __str__(self):
        return self.__unicode__()