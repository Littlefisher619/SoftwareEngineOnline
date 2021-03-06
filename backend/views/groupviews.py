from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from backend.filters import GroupFilter
from backend.serializers.groupserializers import *
from backend.models import Group
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from backend.models import User
import json
import uuid


class GroupViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = GroupInfoSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_class = GroupFilter
    filter_backend = (SearchFilter,)
    permission_classes_by_action = {
        'verifytoken': [AllowAny, ],
    }

    def get_serializer_class(self):
        if self.action in ['verifytoken', ]:
            return GroupVerifyTokenSerializer
        else:
            return GroupInfoSerializer

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [IsAuthenticated])]

    @action(methods=['POST'], url_path='create', detail=False)
    def _create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Group.objects.filter(leader=self.request.user, grouptype=serializer.validated_data['grouptype']).exists():
            return Response({
                'success': False,
                'message': '你已经是当前队伍类型的组长了，不能再创建新的队伍'
            }, status=status.HTTP_200_OK)

        for data in Group.objects.filter(grouptype=serializer.validated_data['grouptype']).values('members'):
            if self.request.user.pk in json.loads(data['members']):
                return Response({
                    'success': False,
                    'message': '你已经是当前队伍类型的某个组的组员，不能再创建新的队伍'
                }, status=status.HTTP_200_OK)

        self.perform_create(serializer)
        return Response(
            {
                'success': True,
                'message': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.validated_data['token'] = uuid.uuid4()
        serializer.validated_data['leader'] = self.request.user
        serializer.validated_data['members'] = '[]'
        if serializer.validated_data['grouptype'] == Group.GROUP and self.request.user.role == User.GROUP_MEMBER:
            self.request.user.role = User.GROUP_LEADER
            self.request.user.save()

        serializer.save()

    @action(methods=['POST'], detail=True, name='验证Token')
    def verifytoken(self, request, pk=None):
        group = self.get_object()
        return Response(
            {
                'success': request.data.get('token', None) == group.token,
            }, status=status.HTTP_200_OK
        )

    @action(methods=['GET'], detail=True, name='加入')
    def join(self, request, pk=None):
        group = self.get_object()
        grouptype = group.grouptype
        if Group.objects.filter(leader=self.request.user, grouptype=group.grouptype).exists():
            return Response({
                'success': False,
                'message': '你已经是当前队伍类型的组长了，不能再加入其它队伍'
            }, status=status.HTTP_200_OK)

        for member_list in Group.objects.filter(grouptype=grouptype).values('members'):
            if self.request.user.pk in json.loads(member_list['members']):
                return Response({
                    'success': False,
                    'message': '你已经是当前队伍类型的某个组的组员，不能再加入其它队伍'
                }, status=status.HTTP_200_OK)

        members_limit = 2 if grouptype == Group.DOUBLE else 10
        members = json.loads(group.members)
        members_len = len(members)
        if members_len >= members_limit - 1:
            return Response({
                'success': False,
                'message': '这个组已经满员惹~'
            }, status=status.HTTP_200_OK)
        else:
            members.append(self.request.user.pk)
            group.members = json.dumps(members)
            group.save()
            return Response(
                {
                    'success': True,
                    'message': '加入成功',
                    'data':  self.get_serializer(group).data
                }, status=status.HTTP_200_OK
            )