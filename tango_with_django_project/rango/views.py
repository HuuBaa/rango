from django.shortcuts import render
from django.http import HttpResponse
from .models import Category,Page

def index(request):
    category_list_liked=Category.objects.order_by('-likes')[:5]
    page_list_viewed=Page.objects.order_by('-views')[:5]
    con_dict={'categories_liked':category_list_liked,'page_list_viewed':page_list_viewed}
    return render(request,'rango/index.html',context=con_dict)

def show_category(request,category_name_slug):
    con_dict={}
    try:
        category=Category.objects.get(slug=category_name_slug)
        pages=Page.objects.filter(category=category)
        con_dict["pages"]=pages
        con_dict["category"] = category

    except Category.DoesNotExist:

        con_dict["pages"] = None
        con_dict["category"] = None
    return render(request,'rango/category.html',con_dict)

def about(request):
    return  render(request,'rango/about.html')