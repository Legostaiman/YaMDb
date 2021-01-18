import django_filters

from .models import Title


class TitleFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    genre = django_filters.ModelMultipleChoiceFilter(
        field_name='genre',                                                
        queryset=Title.objects.all(),
    )

    category = django_filters.CharFilter(
        field_name='category',
        lookup_expr='icontaions'
    )

    class Meta:
        model = Title
        fields = ('name', 'genre',)
