from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoSanguineoViewSet, DoadorViewSet

router = DefaultRouter()
router.register(r'tipos-sanguineos', TipoSanguineoViewSet, basename='tiposanguineo')
router.register(r'doadores', DoadorViewSet, basename='doador')

urlpatterns = [
    path('v1/', include(router.urls)),
]
