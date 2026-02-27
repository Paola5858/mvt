from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.listar_animais, name='listar_animais'),
    path('criar/', views.criar_animal, name='criar_animal'),
    path('editar/<int:pk>/', views.editar_animal, name='editar_animal'),
    path('deletar/<int:pk>/', views.deletar_animal, name='deletar_animal'),
]
