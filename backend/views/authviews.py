from django.contrib.auth import get_user_model, logout

from django.contrib.auth.password_validation import MinimumLengthValidator
from django.shortcuts import render

from rest_framework import generics, views, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.utils import jwt_response_payload_handler

from backend.models import User
from backend.serializers.authserializers import SignupSerializer, LoginSerializer


class LoginView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, **kwargs):
        if self.request.user.username:
            return Response({
                'success': False,
                'message': '你已经登录过了，不需要再次登录'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token = serializer.validated_data.get('token')
            print(serializer.validated_data)
            response_data = {
                'token': token,
                'username': user.username,
            }
            response = Response(response_data)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, **kwargs):
        if self.request.user.username:
            return Response({
                'success': False,
                'message': '已经登录的状态下不允许注册账号'
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response({
                'success': True,
                'message': '注册成功',
                'token': serializer.data['token'],
                'username': serializer.data['username'],
            }, status=status.HTTP_200_OK)

