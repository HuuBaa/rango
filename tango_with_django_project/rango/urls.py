#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name='rango'

urlpatterns=[
    url(r'^about/$',views.about,name='about'),
    url(r'^$',views.index,name='index'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category,name='show_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page,name='add_page'),
    url(r'^add_category/$',views.add_category,name='add_category')
]