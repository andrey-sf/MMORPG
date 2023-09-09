import django_filters
from .models import Response


class ResponseFilter(django_filters.FilterSet):
    responseText = django_filters.CharFilter(lookup_expr='icontains', label='Текст отклика')
    responseAd__title = django_filters.CharFilter(lookup_expr='icontains', label='Название объявления')
    is_accepted = django_filters.BooleanFilter(field_name='is_accepted', label='Принят отклик')

    class Meta:
        model = Response
        fields = []

    def __init__(self, *args, **kwargs):
        super(ResponseFilter, self).__init__(*args, **kwargs)
        self.form.fields['responseText'].widget.attrs.update({'placeholder': 'Поиск по тексту отклика'})
        self.form.fields['responseAd__title'].widget.attrs.update({'placeholder': 'Поиск по названию объявления'})
