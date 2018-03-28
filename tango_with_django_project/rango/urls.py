#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.conf.urls import url
from rango import views

urlpatterns=[
    url(r'^about/',views.about,name='about'),
    url(r'^$',views.index,name='index')
]