# coding=utf-8

from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',
    
    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^$',
        views.home,
        name='home'
    ),     
    url(r'^(?i)empresas/(?P<ciudad>[\.\w]+)/$',
        views.empresas,
        name='empresas'
    ),
    
    url(r'^(?i)linkedin/$',
        views.linkedin_search,
        name='linkedin_search'
    ),
)
