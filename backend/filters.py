import django_filters

from backend.models import *


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ("grouptype", "leader", )