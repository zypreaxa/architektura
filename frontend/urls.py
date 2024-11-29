from django.urls import path
from django.views.generic import TemplateView
from . import views
app_name = "frontend"
urlpatterns = [
    path("", views.index, name="index"),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
]