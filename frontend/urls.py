from django.urls import path
from django.views.generic import TemplateView
from . import views
app_name = "frontend"
urlpatterns = [
    path("", views.index, name="index"),
]