from rest_framework import serializers
from backend.models import HomeWork

from .jsonserializer import JsonSerializer


class HomeWorkSerializer(serializers.ModelSerializer):
    scorerules = JsonSerializer(label='评分细则')

    class Meta:
        model = HomeWork
        fields = ('id', 'title', 'homeworktype', 'scorerules', 'weight', 'author', 'blogurl')
        read_only_fields = ('id', 'author', )