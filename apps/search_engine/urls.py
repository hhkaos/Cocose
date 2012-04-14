# coding=utf-8

from django.conf.urls.defaults import patterns, include, url

import views

urlpatterns = patterns('',

    #(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^$',
        views.home,
        name='home'
    ),     
)
