import django_filters

from .models import Title


class TitleFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    genre = django_filters.CharFilter(
        field_name='genre',                                                             
        lookup_expr='iexact'
    )

    class Meta:
        model = Title
        fields = ('name', 'genre',)
