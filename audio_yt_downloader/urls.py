from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('downloader/', include("downloader.urls")),
    path('admin/', admin.site.urls),
]
