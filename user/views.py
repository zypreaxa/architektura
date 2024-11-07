from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

# Registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")  # Redirect to homepage or any other page
    else:
        form = UserCreationForm()
    return render(request, "frontend/register.html", {"form": form})

# You can create custom login/logout views or use Django's built-in views
class CustomLoginView(LoginView):
    template_name = "frontend/login.html"  # Path to template in the frontend app

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")  # Redirect after logout
