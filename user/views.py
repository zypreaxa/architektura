from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create the user and log them in
            user = form.save()
            login(request, user)

            # Create a UserProfile for the new user
            UserProfile.objects.create(user=user, preferred_cuisine="Italian", preferred_recipe_type="Vegan")

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
        return redirect("frontend:index")
        
@login_required(login_url="/user/login/")
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user_profile.preferred_cuisine = 'Italian'
    user_profile.save()
    return render(request, "profile.html", {"user_profile": user_profile})

