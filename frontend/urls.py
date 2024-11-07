from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),        # Use the `login` view
    path("register/", views.register, name="register") # Use the `register` view
]