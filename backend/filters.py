import django_filters
from rest_framework.filters import SearchFilter

from backend.models import *


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ("grouptype", "leader__stuname", "groupname", "id", "leader")


class JudgementFilter(django_filters.FilterSet):
    class Meta:
        model = Judgement
        fields = ("homework", "judger", "group", "student", "student__stuname", "student__stuid", "group__leader__stuname")


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("stuname", "stuid", "id",)


class TasklistSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        if 'pk' in view.kwargs:
            pk = view.kwargs['pk']
            homework = HomeWork.objects.get(id=pk)
            if homework.homeworktype == HomeWork.SINGLE:
                return ["^stuname", "^stuid"]
            elif homework.homeworktype in [HomeWork.DOUBLE, HomeWork.GROUP]:
                return ["^leader__stuname", "^groupname", "^leader__stuid"]
        else:
            return []


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Rate
        fields = ("group", "homework",)
