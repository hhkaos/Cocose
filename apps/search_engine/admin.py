# coding=utf-8

from django.contrib import admin
from django.conf import settings

from models import *  

class AdminEmpresa(admin.ModelAdmin):
    list_display = ('nombre',)
    #list_filter = ('estado', 'ciudad','curso',)
    search_fields = ['nombre']
    #~ filter_horizontal = ('codigo','profesores','colaboradores')
    
class AdminEmpleados(admin.ModelAdmin):
    list_display = ('nombre',)
    #list_filter = ('estado', 'ciudad','curso',)
    search_fields = ['nombre']

admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Empleados, AdminEmpleados)
