from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from backend.serializers.authserializers import UserInfoSerializer
from backend.serializers.groupserializers import GroupInfoSerializer
from backend.serializers.homworkserializer import HomeWorkSerializer
from backend.models import HomeWork, User, Judgement, Group
from backend.filters import GroupFilter, UserFilter, TasklistSearchFilter, JudgementFilter
import json

class HomeWorkViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin):
    permission_classes_by_action = {
        'create': [IsAdminUser, ],
    }
    serializer_class = HomeWorkSerializer
    queryset = HomeWork.objects.all()
    filter_backend = (TasklistSearchFilter,)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [IsAuthenticated])]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()

    @action(methods=['GET'], url_path='tasklist', detail=True)
    def tasklist(self, request, pk=None):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                'success': False,
                'message': '你走错地方惹，这儿啥也没有~'
            }, status=status.HTTP_403_FORBIDDEN)

        homework = self.get_object()
        taskqueryset = None
        serializer_class = None
        if homework.homeworktype == homework.SINGLE:
            serializer_class = UserInfoSerializer
            filter_class = UserFilter
            judged_user = Judgement.objects.filter(homework=homework).values_list('student', flat=True)
            taskqueryset = User.objects.filter(~Q(id__in=judged_user),Q(role__in=[User.GROUP_MEMBER, User.GROUP_LEADER]))

        elif homework.homeworktype in [homework.GROUP, homework.DOUBLE]:
            serializer_class = GroupInfoSerializer
            filter_class = GroupFilter
            judged_group = Judgement.objects.filter(homework=homework).values_list('student', flat=True)
            taskqueryset = Group.objects.filter(~Q(id__in=judged_group), Q(grouptype=homework.homeworktype))

        queryset = filter_class(request.GET, queryset=taskqueryset).qs
        queryset = TasklistSearchFilter().filter_queryset(request=self.request, queryset=queryset, view=self)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
        pass

    @action(methods=['GET'], url_path='statistics', detail=True)
    def statistics(self, request, pk=None):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                'success': False,
                'message': '只有测试组可以使用统计功能'
            }, status=status.HTTP_403_FORBIDDEN)

        homework = self.get_object()
        alljudgements = Judgement.objects.filter(homework=homework)
        judgements = JudgementFilter(request.GET, queryset=alljudgements).qs

        totalscore = {
            'min': None,
            'max': None,
            'avg': 0,
            'exclude': 0,
            'ranges': [
                {
                    'name': '>100',
                    'from': 100,
                    'to': None,
                    'count': 0,
                }
            ]
        }

        for i in range(0, 3):
            totalscore['ranges'].append(
                {
                    'name': f'[{i*20},{(i+1)*20})',
                    'from': i*20,
                    'to': i*20 + 19,
                    'count': 0,
                }
            )

        for i in range(60, 100, 5):
            totalscore['ranges'].append(
                {
                    'name': f'[{i},{i+5})',
                    'from': i,
                    'to': i + 4,
                    'count': 0,
                }
            )

        points = {}

        for judgement in judgements:
            for _range in totalscore['ranges']:
                in_range_from = _range['from'] is None or judgement.totalscore >= _range['from']
                in_range_to = _range['to'] is None or judgement.totalscore <= _range['to']
                if in_range_from and in_range_to:
                    _range['count'] += 1

            if judgement.totalscore == 0:
                totalscore['exclude'] += 1
                continue

            if totalscore['min'] is None or totalscore['min'] > judgement.totalscore:
                totalscore['min'] = judgement.totalscore

            if totalscore['max'] is None or totalscore['max'] < judgement.totalscore:
                totalscore['max'] = judgement.totalscore

            totalscore['avg'] += judgement.totalscore

            scorepoints = json.loads(judgement.scoredetail)['scorepoints']

            for detail in scorepoints:
                score = detail['score']

                if detail['point'] not in points:
                    points[detail['point']] = {
                        'point': detail['point'],
                        'max': None,
                        'min': None,
                        'avg': 0,
                        'exclude': 0,
                    }

                p = points[detail['point']]

                if score == 0:
                    p['exclude'] += 1
                    continue

                if p['min'] is None or p['min'] > score:
                    p['min'] = score

                if p['max'] is None or p['max'] < score:
                    p['max'] = score

                p['avg'] += score

        totalscore['avg'] = round(totalscore['avg'] / (len(judgements)-totalscore['exclude'])*1.00, 2)
        for pointname, point in points.items():
            point['avg'] = round(point['avg'] / (len(judgements) - point['exclude'])*1.00, 2)

        return Response({
            'totalscore': totalscore,
            'points': points.values()
        })

