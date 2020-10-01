from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from backend.serializers.authserializers import UserInfoSerializer
from backend.serializers.groupserializers import GroupInfoSerializer
from backend.serializers.homworkserializer import HomeWorkSerializer
from backend.models import HomeWork, User, Judgement, Group
from backend.filters import GroupFilter, UserFilter

class HomeWorkViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    permission_classes_by_action = {
        'create': [IsAdminUser, ],
    }
    serializer_class = HomeWorkSerializer
    queryset = HomeWork.objects.all()

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
        tasklist = []
        serializer_class = None
        if homework.homeworktype == homework.SIGNGLE:
            serializer_class = UserInfoSerializer
            judgements = Judgement.objects.filter(homework=homework).values_list('student')
            users = User.objects.filter(~Q(role=User.TEST_GROUP))
            user_filtered = UserFilter(request.GET, queryset=users).qs
            for user in user_filtered:
                if not judgements.filter(student=user).exists():
                    tasklist.append(user)

        elif homework.homeworktype in [homework.GROUP, homework.DOUBLE]:
            serializer_class = GroupInfoSerializer
            judgements = Judgement.objects.filter(homework=homework).values_list('group')
            groups = Group.objects.filter(grouptype=homework.homeworktype)
            grouo_filtered = GroupFilter(request.GET, queryset=groups).qs
            for group in grouo_filtered:
                if not judgements.filter(group=group).exists():
                    tasklist.append(group)

        queryset = self.filter_queryset(tasklist)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
        pass

