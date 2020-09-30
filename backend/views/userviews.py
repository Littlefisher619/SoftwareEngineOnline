import json

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from backend.serializers.groupserializers import *
from backend.serializers.userserializers import *
from backend.serializers.judgementserializers import *


class UserViewSetNormal(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_classes_by_action = {
        'updatepassword':  UserUpdatePasswordSerializer,
        'mygroup': GroupTokenSerializer,
        'groupinfo': GroupInfoSerializer,
        'judgements': JudgementInfoSerializer,
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

    def __serialize_group_info_data(self, user):
        assert self.action in ['groupinfo', 'mygroup']
        double_group, big_group = Group.filter_group_by_from_user(user)
        data = {
            'double': None,
            'big': None
        }

        if double_group:
            data['double'] = self.get_serializer(double_group).data
        if big_group:
            data['big'] = self.get_serializer(big_group).data
        return data

    @action(methods=['GET'], detail=False, name='评分查询')
    def judgements(self, request):
        double_group, big_group = Group.filter_group_by_from_user(self.request.user)
        data = dict()
        data['big'] = self.get_serializer(Judgement.objects.filter(group=big_group), many=True).data if big_group else []
        data['double'] = self.get_serializer(Judgement.objects.filter(group=double_group), many=True).data if double_group else []
        data['single'] = self.get_serializer(Judgement.objects.filter(student=self.request.user), many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True, name='组队查询')
    def groupinfo(self, request, pk):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                    'success': False,
                    'message': '你走错地方惹，这儿啥也没有~'
                }, status=status.HTTP_403_FORBIDDEN)
        return Response(
            self.__serialize_group_info_data(self.get_object()),
            status=status.HTTP_200_OK
        )

    @action(methods=['GET'], detail=False, name='我的组队')
    def mygroup(self, request):
        return Response(
            self.__serialize_group_info_data(self.request.user),
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
