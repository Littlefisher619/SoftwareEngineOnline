from rest_framework import serializers
from rest_framework.fields import CharField

from backend.models import Group
from .jsonserializer import JsonSerializer
from .userserializers import UserInfoSerializer


class GroupInfoSerializer(serializers.ModelSerializer):
    members = JsonSerializer(label='组员', read_only=True)
    leader = UserInfoSerializer(label='组长', read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'leader', 'grouptype', 'members', 'groupname')
        read_only_fields = ('id', 'leader', 'members', )