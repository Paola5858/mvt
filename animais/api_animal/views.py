from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Animal
from .serializers import AnimalSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    pagination_class = StandardResultsSetPagination
