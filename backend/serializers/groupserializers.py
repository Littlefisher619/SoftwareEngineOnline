from rest_framework import serializers
from rest_framework.fields import CharField

from backend.models import Group, User
from .jsonserializer import JsonSerializer
from .userserializers import UserInfoSerializer
import json


class GroupInfoSerializer(serializers.ModelSerializer):
    members = serializers.HiddenField(label='组员列表', write_only=True, default=[])
    member_detail = serializers.SerializerMethodField()
    leader = UserInfoSerializer(label='队长', read_only=True)
    groupname = CharField(min_length=5, label='队伍名称')

    def get_member_detail(self, group):
        print(group.get_members())
        print(UserInfoSerializer(group.get_members(), many=True).data)
        return UserInfoSerializer(group.get_members(), many=True).data


    # def validate(self, data):
    #     super().validate(data)
    #     if Group.objects.filter(groupname=data.get('groupname')).exists():
    #         raise serializers.ValidationError(
    #             '组名已存在',
    #             code='login_invalid',
    #         )

    class Meta:
        model = Group
        fields = ('id', 'leader', 'grouptype', 'members', 'groupname', 'member_detail')
        read_only_fields = ('id', 'leader', 'member_detail', 'members')


class GroupTokenSerializer(GroupInfoSerializer):
    class Meta:
        model = Group
        fields = ('id', 'leader', 'grouptype', 'members', 'groupname', 'member_detail', 'token')
        read_only_fields = fields


class GroupVerifyTokenSerializer(GroupInfoSerializer):
    class Meta:
        model = Group
        fields = ('token', )
