from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api_animal.urls')),
    path('', include('api_talhao.urls')),
]
