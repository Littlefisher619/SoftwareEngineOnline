import json

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from backend.serializers.groupserializers import GroupInfoSerializer
from backend.serializers.userserializers import *


class UserViewSetNormal(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_classes_by_action = {
        'updatepassword':  UserUpdatePasswordSerializer,
    }
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.role != User.TEST_GROUP and self.request.user != self.get_object():
            return Response({
                    'success': False,
                    'message': '你走错地方惹，这儿啥也没有~'
                }, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                    'success': False,
                    'message': '你走错地方惹，这儿啥也没有~'
                }, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        serializer_class = self.serializer_classes_by_action.get(self.action, UserInfoSerializer)
        return serializer_class

    @action(methods=['GET'], detail=False, name='我的个人资料')
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def __get_group_info_json_data(self, user):
        double_group = None
        big_group = None

        try:
            double_group = Group.objects.get(leader=user, grouptype=Group.DOUBLE)
        except Group.DoesNotExist:
            for group in Group.objects.filter(grouptype=Group.DOUBLE):

                if self.request.user.pk in json.loads(group.members):
                    double_group = group
                    break

        try:
            big_group = Group.objects.get(leader=user, grouptype=Group.GROUP)
        except Group.DoesNotExist:
            for group in Group.objects.filter(grouptype=Group.GROUP):
                if self.request.user.pk in json.loads(group.members):
                    big_group = group
                    break

        data = {}

        data['double'] = None if double_group is None else GroupInfoSerializer(double_group).data
        data['big'] = None if big_group is None else GroupInfoSerializer(big_group).data
        return data

    @action(methods=['GET'], detail=True, name='组队查询')
    def groupinfo(self, request, pk):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                    'success': False,
                    'message': '你走错地方惹，这儿啥也没有~'
                }, status=status.HTTP_403_FORBIDDEN)
        return Response(
            self.__get_group_info_json_data(self.get_object()),
            status=status.HTTP_200_OK
        )

    @action(methods=['GET'], detail=False, name='我的组队')
    def mygroup(self, request):
        return Response(
            self.__get_group_info_json_data(self.request.user),
            status=status.HTTP_200_OK
        )

    @action(methods=['POST'], detail=False, name='修改密码')
    def updatepassword(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({
            'success': True,
            'message': '密码已修改'
        }, status=status.HTTP_200_OK)
