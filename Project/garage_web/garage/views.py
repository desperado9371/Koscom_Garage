from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def post_list(request):
    return render(request, 'garage/index.html', {})


def algo(request):
    return render(request, 'garage/algo.html', {})


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("login as "+username)
            return redirect('/')
        else:
            print("login fail")
            return render(request, 'garage/login.html', { 'error':'username or password is incorrect!'})
    return render(request, 'garage/login.html', {})


@csrf_exempt
def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            auth.login(request, user)
            return redirect('/')
        return render(request, 'garage/signup.html', {})
    return render(request, 'garage/signup.html', {})


def logout(request):
    auth.logout(request)
    return redirect('/')


def backtest(request):
    return render(request, 'garage/backtest.html',{})





