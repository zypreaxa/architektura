from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
# Registration view
def register_view(request):
    form = UserCreationForm()
    return render(request, "register.html", { "form": form })