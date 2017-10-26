from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
import datetime
from django.contrib.auth import authenticate, login as auth_login, logout
from smartHouse.forms import SignupForm
from django.contrib.auth import get_user_model
from smartHouse.models import house


# Create your views here.
def home(request):
    time = datetime.datetime.now()

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

