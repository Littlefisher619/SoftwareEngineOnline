from rest_framework import serializers
from rest_framework.fields import ChoiceField

from backend.models import Judgement, Group
from .jsonserializer import JsonSerializer


class JudgementInfoSerializer(serializers.ModelSerializer):
    scoredatail = JsonSerializer(label='评分详情')

    class Meta:
        model = Judgement
        fields = ('id', 'student', 'group', 'judger', 'homework', 'scoredatail', 'createat', )
        read_only_fields = ('id', 'creatat', 'judger', )
