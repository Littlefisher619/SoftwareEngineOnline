from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from backend.serializers.groupserializers import *
from backend.models import Group
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import json

class GroupViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = GroupInfoSerializer
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
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
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'success': True,
                'message': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.validated_data['leader'] = self.request.user
        serializer.validated_data['members'] = json.dumps([self.request.user.pk,])
        serializer.save()
