from rest_framework.routers import DefaultRouter
from .views import TalhaoViewSet

router = DefaultRouter()
router.register(r'talhoes', TalhaoViewSet)

urlpatterns = router.urls
