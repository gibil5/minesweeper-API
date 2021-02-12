from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse 
from minesweeper import util

# Create your views here.
def index(request):
    print('*** index')
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")


def login_view(request):
    print('*** login')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message":  "Invalid credentials.",
            })
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message":  "Logged out.",        
    })


def games(request):
    print('*** games')

    user = request.user

    print(request)
    print(user)

    return render(request, "minesweeper/index.html",
        {
            "boards": util.list_boards_user(user)
        })
    #return render(request, "minesweeper/index.html")
