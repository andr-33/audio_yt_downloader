from django.urls import path
from . import views

urlpatterns = [
    path("extract-audio", views.extract_audio, name="extract-audio"),
]

