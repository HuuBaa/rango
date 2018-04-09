from django.shortcuts import render
from django.http import HttpResponse
from .models import Category,Page
from .forms import PageForm,CategoryForm,UserForm,UserProfileForm
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

def add_category(request):
    form=CategoryForm()
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            cat=form.save(commit=True)
            print(cat,cat.slug)
            return index(request)
        else:
            print(form.errors)
    return render(request,'rango/add_category.html',{'form':form})

def add_page(request,category_name_slug):

    try:
        category=Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None

    form = PageForm()
    if request.method=='POST':
        form=PageForm(request.POST)
        if form.is_valid():
            if category is not None:
                print(category)
                page=form.save(commit=False)
                page.category=category
                page.views=0
                page.save()
                print('save successfully')
            return show_category(request,category_name_slug)
        else:
            print(form.errors)

    return render(request,'rango/add_page.html',{'form':form,'category':category})


def register(request):

    registered=False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()

            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']

            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'rango/register.html',
                  {'user_form':user_form,'profile_form':profile_form,'registered':registered})


def about(request):
    return  render(request,'rango/about.html')