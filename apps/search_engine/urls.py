# coding=utf-8

from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    
    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^$',
        views.home,
        name='home'
    ),     
    url(r'^(?i)old/$',
        views.home_old,
        name='home_old'
    ),     
    url(r'^(?i)backbone/$',
        views.home_backbone,
        name='home_backbone'
    ),     
    url(r'^(?i)empresas/(?P<ciudad>[\.\w]+)/$',
        views.empresas,
        name='empresas'
    ),
    
    url(r'^(?i)linkedin/$',
        views.linkedin_search,
        name='linkedin_search'
    ),
    
    url(r'^(?i)linkedin/save/$',
        views.linkedin_save,
        name='linkedin_save'
    ),
    
    url(r'^(?i)google/$',
        views.google,
        name='google'
    ),
    url(r'^(?i)del/$',
        views.remove_company,
        name='remove_company'
    ),
    url(r'^(?i)validar/$',
        views.validar_company,
        name='validar_company'
    ),
    url(r'^(?i)whois/$',
        views.whois,
        name='whois'
    ),
)
