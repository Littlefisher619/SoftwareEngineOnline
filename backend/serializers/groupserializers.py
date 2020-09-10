from rest_framework import serializers
from rest_framework.fields import CharField

from backend.models import Group, User
from .jsonserializer import JsonSerializer
from .userserializers import UserInfoSerializer
import json


class GroupInfoSerializer(serializers.ModelSerializer):
    members = JsonSerializer(write_only=True)
    member_detail = serializers.SerializerMethodField()
    leader = UserInfoSerializer(label='队长', read_only=True)
    groupname = CharField(min_length=5, label='队伍名称')

    def get_member_detail(self, group):
        member_list = []
        for i in JsonSerializer().to_representation(group.members):
            if group.leader.pk != i:
                member_list.append(UserInfoSerializer(User.objects.get(pk=i)).data)
        return member_list

    class Meta:
        model = Group
        fields = ('id', 'leader', 'grouptype', 'members', 'groupname', 'member_detail')
        read_only_fields = ('id', 'leader', 'member_detail', )