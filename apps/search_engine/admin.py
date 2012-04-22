# coding=utf-8

from django.contrib import admin
from django.conf import settings

from models import *  

class AdminEmpresa(admin.ModelAdmin):
    list_display = ('nombre','_get_emails','ciudad','web','validada','ocultar')
    list_filter = ('ciudad','validada','ocultar')
    search_fields = ['ciudad']
    filter_horizontal = ('email',)
    
    def _get_emails(self, obj):
        return ', '.join([t for t in obj.email.all().values_list('email', flat=True)])
    _get_emails.short_description = u'Emails'
    
class AdminEmpleados(admin.ModelAdmin):
    list_display = ('nombre',)
    #list_filter = ('estado', 'ciudad','curso',)
    search_fields = ['nombre']

admin.site.register(Empresa, AdminEmpresa)
admin.site.register(Empleados, AdminEmpleados)
admin.site.register(Emails)
