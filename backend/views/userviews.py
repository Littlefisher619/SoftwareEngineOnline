from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

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
                }, status=status.HTTP_200_OK)
        super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                    'success': False,
                    'message': '你走错地方惹，这儿啥也没有~'
                }, status=status.HTTP_200_OK)
        super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        serializer_class = self.serializer_classes_by_action.get(self.action, UserInfoSerializer)
        return serializer_class

    @action(methods=['GET'], detail=False, name='我的个人资料')
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

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
