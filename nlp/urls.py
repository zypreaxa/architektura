from django.urls import path
from . import views

urlpatterns = [
    path("process_chat/", views.process_chat, name="process_chat"),
]
