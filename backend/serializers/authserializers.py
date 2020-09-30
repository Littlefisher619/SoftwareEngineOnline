from django.contrib.auth import get_user_model, authenticate
from backend.models import User
from rest_framework import serializers
from rest_framework.fields import CharField, EmailField
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.settings import api_settings


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'stuid', 'stuname', 'username', 'role', )


class LoginSerializer(serializers.ModelSerializer):
    username = CharField(label='用户名', required=False)
    stuid = CharField(label='学号', required=False)
    password = CharField(label='密码', required=True, write_only=True, )
    token = CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'stuid', 'password', 'token')

    def validate(self, data):
        stuid = data.get('stuid')
        username = data.get('username')
        password = data.get('password')

        if stuid is None and username is None:
            raise serializers.ValidationError(
                '在登录时必须填写用户名或学号字段之一',
                code='login_invalid',
            )
        if not stuid is None and not username is None:
            raise serializers.ValidationError(
                '只能使用用户名或学号之一进行登录',
                code='login_invalid',
            )

        if username is None:
            try:
                username = User.objects.get(stuid=stuid).username
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    '该学号未在系统上注册',
                    code='login_failed',
                )

        credentials = {
            'username': username,
            'password': password
        }

        user = authenticate(**credentials)

        if user:
            if not user.is_active:
                msg = '当前用户未激活'
                raise serializers.ValidationError(msg)

            payload = jwt_payload_handler(user)
            return {
                'token': jwt_encode_handler(payload),
                'user': user
            }
        else:
            msg = '提供的凭据信息无效'
            raise serializers.ValidationError(msg)


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'token', 'stuid', 'stuname')
        # read_only_fields = ('token', )

    password = CharField(min_length=6, max_length=100, label='密码', required=True)
    username = CharField(min_length=3, max_length=100, label='用户名', required=True)
    stuid = CharField(max_length=10, label='学号', required=True)
    stuname = CharField(max_length=200, label='姓名', required=True)
    email = EmailField(label='邮箱', required=True)
    token = CharField(read_only=True)


    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        stuid = data.get('stuid')
        users = User.objects.all()
        for user in users:
            if user.email == email:
                raise serializers.ValidationError(
                    '邮箱已经被注册了',
                    code='email_not_unique',
                )
            if user.username == username:
                raise serializers.ValidationError(
                    '用户名已经被注册了',
                    code='username_not_unique',
                )
            if user.stuid == stuid:
                raise serializers.ValidationError(
                    '这个学号已经被注册了',
                    code='username_not_unique',
                )

        return data


    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        # 用已经通过数据合法性唯一性校验的用户数据生成token
        user.save()
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        return user