from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from .models import Talhao
from .serializers import TalhaoSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class TalhaoViewSet(ModelViewSet):
    queryset = Talhao.objects.all()
    serializer_class = TalhaoSerializer
    pagination_class = StandardResultsSetPagination
