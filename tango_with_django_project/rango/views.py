from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


from .models import Category,Page
from .forms import PageForm,CategoryForm,UserForm,UserProfileForm
from datetime import datetime

def visitor_cookie_handler(request):
    visits=int(request.session.get('visits','1'))
    last_visit_cookie=request.session.get('last_visit',str(datetime.now()))
    last_visit_time=datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    if (datetime.now()-last_visit_time).seconds>60:
        visits+=1
        request.session['last_visit']=str(datetime.now())
    else:
        request.session['last_visit'] =last_visit_cookie

    request.session['visits']=visits

def index(request):
    # request.session.set_test_cookie()
    category_list_liked=Category.objects.order_by('-likes')[:5]
    page_list_viewed=Page.objects.order_by('-views')[:5]
    con_dict={'categories_liked':category_list_liked,'page_list_viewed':page_list_viewed}

    visitor_cookie_handler(request)
    con_dict['visits']=request.session['visits']

    response = render(request, 'rango/index.html', context=con_dict)
    return  response

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

@login_required
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
@login_required
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


# def register(request):
#
#     registered=False
#
#     if request.method=='POST':
#         user_form=UserForm(data=request.POST)
#         profile_form=UserProfileForm(data=request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user=user_form.save()
#
#             user.set_password(user.password)
#             user.save()
#
#             profile=profile_form.save(commit=False)
#             profile.user=user
#
#             if 'picture' in request.FILES:
#                 profile.picture=request.FILES['picture']
#
#             profile.save()
#             registered=True
#         else:
#             print(user_form.errors,profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     return render(request,'rango/register.html',
#                   {'user_form':user_form,'profile_form':profile_form,'registered':registered})
#
# def user_login(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user=authenticate(username=username,password=password)
#         if user:
#             if user.is_active:
#                 login(request,user)
#                 print('登录成功')
#                 return HttpResponseRedirect(reverse('rango:index'))
#             else:
#                 return HttpResponse("账户不可用！")
#         else:
#             print('无效的登录信息，{0}，{1}'.format(username,password))
#             return HttpResponse("无效的登录信息！")
#     else:
#         return render(request,'rango/login.html',{})

@login_required
def restricted(request):
    return HttpResponse("如果你登录了，你就能看见这段话！")

# @login_required
# def user_logout(request):
#     logout(request)
    return HttpResponseRedirect(reverse('rango:index'))

def about(request):
    # if request.session.test_cookie_worked():
    #     print('TEST COOKIE WORKED!')
    #     request.session.delete_test_cookie()
    visitor_cookie_handler(request)
    visits=request.session.get('visits')
    return  render(request,'rango/about.html',{'visits':visits})

def track_url(request):
    page_id=None
    if request.method=='GET':
        if 'page_id' in request.GET:
            page_id=request.GET['page_id']
    if page_id:
        try:
            page=Page.objects.get(id=page_id)
            page.views=page.views+1
            page.save()
            return redirect(page.url)
        except:
            return HttpResponseRedirect("page id : {} is not found.".format(page_id))
    print('no page_id in get string')
    return redirect(reverse('rango:index'))
