import django_filters
from .models import Title


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
