from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
# Registration view
def register_view(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("frontend:index")
    else:
        form = UserCreationForm()
    return render(request, "register.html", { "form": form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("frontend:index")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", { "form": form })

def logout_view(request):
    if request.method=="POST":
        logout(request)
        return redirect("user:login")
        
@login_required(login_url="/user/login/")
def profile_view(request):
    return render(request, "profile.html")
