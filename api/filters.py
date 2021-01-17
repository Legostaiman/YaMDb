import django_filters


class TitleFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
