from django.utils.translation import gettext_lazy as _
import django_filters

from .models import Ad, Response


class ResponseFilter(django_filters.FilterSet):

    class Meta:
        model = Response
        fields = {
            'is_accepted': ['exact'],
            'responseAd': ['exact'],
        }
