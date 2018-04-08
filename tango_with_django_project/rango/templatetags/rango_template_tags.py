#!/usr/bin/env python
#-*- coding: utf-8 -*-
from ..models import Category
from django import template

register=template.Library()
@register.inclusion_tag('rango/cats.html')
def get_category_list(cat=None):
    return {'cats':Category.objects.all(),'act_cat':cat}