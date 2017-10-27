from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
import datetime
from django.contrib.auth import authenticate, login as auth_login, logout
from smartHouse.forms import SignupForm,LoginForm
from django.contrib.auth import get_user_model
from smartHouse.models import house,light as Light,kongtiao as KongTiao


# Create your views here.
def home(request):
    time = datetime.datetime.now()

    if request.user.id:
        u = request.user
        h = house.objects.get(id=u.house.id)
        light_set = h.light.all()
        kong_set = h.kongtiao.all()
    # for i in kong_set :
    #     print(i.temperature)

    return render(request, 'index.html', locals())


def about(request):
    return render(request, 'about.html', locals())


def signup(request):
    path = request.get_full_path()
    if request.method == 'POST':
        form = SignupForm(data=request.POST, auto_id="%s")
        if form.is_valid():
            UserModel = get_user_model()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            birthday = form.cleaned_data['birthday']
            houseId = form.cleaned_data['houseId']
            h = house.objects.get(id = houseId)
            user = UserModel.objects.create_user(username=username, email=email, password=password,birthday = birthday,house = h)
            user.save()
            auth_user = authenticate(username=username, password=password)
            auth_login(request, auth_user)
            return redirect("home")
    else:
        form = SignupForm(auto_id="%s")
    return render(request, 'signup.html', locals())


def logout_view(request):
    logout(request)
    return redirect('home')


def login(request):
    path = request.get_full_path()
    if request.method =='POST':
        loginForm = LoginForm(data = request.POST, auto_id="%s")
        if loginForm.is_valid():
            user_name = loginForm.cleaned_data['username']
            pass_word = loginForm.cleaned_data['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:  # 如果成功返回对象，失败返回None
                auth_login(request, user)  # 调用login方法登陆账号
                return redirect("home")
            else:
                # 登陆失败
                print(loginForm.cleaned_data)
                return render(request, "login.html", locals())
        else:
            # 登陆失败
            return render(request, "login.html", locals())

    else:
        loginForm = LoginForm(auto_id="%s")
    return render(request, 'login.html', locals())

def turnLight(request,light_id):
    # 改变状态：
    l = Light.objects.get(id = light_id)
    s = not l.state
    l.state = s
    l.save()

    time = datetime.datetime.now()

    if request.user.id:
        u = request.user
        h = house.objects.get(id=u.house.id)
        light_set = h.light.all()
        kong_set = h.kongtiao.all()
    # for i in kong_set :
    #     print(i.temperature)

    return render(request, 'index.html', locals())

def raise_temp(request,kong_id):
    # 获取空调对象
    kong = KongTiao.objects.get(id = kong_id)
    # 升温
    kong.temperature = kong.temperature+1
    # 保存
    kong.save()

    time = datetime.datetime.now()
    if request.user.id:
        u = request.user
        h = house.objects.get(id=u.house.id)
        light_set = h.light.all()
        kong_set = h.kongtiao.all()

    return render(request, 'index.html', locals())

def reduce_temp(request,kong_id):
    # 降温
    kong = KongTiao.objects.get(id = kong_id)
    kong.temperature = kong.temperature-1
    kong.save()

    time = datetime.datetime.now()
    if request.user.id:
        u = request.user
        h = house.objects.get(id=u.house.id)
        light_set = h.light.all()
        kong_set = h.kongtiao.all()

    return render(request, 'index.html', locals())

def reduce_temp_text(request):
    a = request.GET['a']
    print(a)