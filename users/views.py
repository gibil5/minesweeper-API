from django.contrib.auth.decorators import login_required
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
    print('*** logout')
    logout(request)
    return render(request, "users/login.html", {
        "message":  "Logged out.",        
    })


@login_required(login_url='/login')
def games(request):
    print('*** games')
    print(request)
    user = request.user
    print(user)
    return render(request, "minesweeper/index.html",
        {
            "boards": util.list_boards_user(user)
        })


def users(request):
    print('*** users')
    return render(request, "users/users.html", {
        "users":  util.get_users(),
    })

def show(request, user_id):
    print('*** show user')
    return render(request, "users/user.html",
        {
        })

# Add users
def add_users(request):
    print('*** add_users')

    # 3d$uN4SD
    # Y6t@UKsW
    # yb3N+KVV
    datax = [
                ('admin_prod',    'Adminus',    'Adminex',    'admin@gmail.com',  "65uznC=m",    True),
                ('harry',    'Harry',    'Potter',    'hpotter@gmail.com',  "nyctal6+",     False),
                ('ron',      'Ron',      'Weasly',    'rweasly@gmail.com',  "@2wHGS#B+",    False),
                ('hermione', 'Hermione', 'Granger',   'hgranger@gmail.com', "Tz9+8ndB",     False),
            ]
    
    for data in datax:
        user = util.add_user(data)
    
    return HttpResponseRedirect(reverse("index"))




