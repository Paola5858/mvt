from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoSanguineoViewSet, DoadorViewSet

router = DefaultRouter()
router.register(r'tipo-sanguineo', TipoSanguineoViewSet)
router.register(r'doador', DoadorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
