from rest_framework import serializers
from rest_framework.fields import CharField

from backend.models import *


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'stuid', 'stuname', 'role', )
        read_only_fields = fields


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'stuid', 'stuname', )
        read_only_fields = fields


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    password = CharField(min_length=8, max_length=32, label='密码', required=True)

    class Meta:
        model = User
        fields = ('id', 'password', )
        read_only_fields = ('id', )