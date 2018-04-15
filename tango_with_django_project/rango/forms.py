#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from .models import Category,Page,UserProfile

class CategoryForm(forms.ModelForm):
    name=forms.CharField(max_length=128,help_text="请输入category的name")
    views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug=forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model=Category
        fields=('name',)

class PageForm(forms.ModelForm):

    def clean(self):
        clean_data=self.cleaned_data
        url=clean_data.get('url')

        if url and not url.startswith('http://'):
            url='http://'+url
            clean_data['url']=url
        return clean_data

    title=forms.CharField(max_length=128,help_text='请输入page的title')
    url=forms.URLField(max_length=200,help_text='请输入page的url')
    views=forms.IntegerField(widget=forms.HiddenInput(),initial=0)

    class Meta:
        model=Page
        exclude=('category',)

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=('username','email','password')

class UserProfileForm(forms.ModelForm):

    website=forms.URLField(required=False)
    picture=forms.ImageField(required=False)

    class Meta:
        model=UserProfile
        fields=('website','picture')
