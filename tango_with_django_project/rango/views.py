from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    con_dict={'boldmessage':'我 要 吃 鸡 腿 ！'}
    return render(request,'rango/index.html',context=con_dict)

def about(request):
    return  render(request,'rango/about.html')