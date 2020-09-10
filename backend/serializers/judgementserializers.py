from rest_framework import serializers
from rest_framework.fields import ChoiceField

from backend.models import Judgement, Group, HomeWork
from .authserializers import UserInfoSerializer
from .homworkserializer import HomeWorkSerializer
from .jsonserializer import JsonSerializer


class JudgementInfoSerializer(serializers.ModelSerializer):
    scoredatail = JsonSerializer(label='评分详情')
    judger = UserInfoSerializer(label='评分员', read_only=True)
    homework = HomeWorkSerializer(label='作业')

    def validate(self, attrs):
        super().validate(attrs)
        print(attrs)
        if attrs.get('homework') is None:
            raise serializers.ValidationError("需指定一个作业才能进行评分")

        if attrs.get('homework').homeworktype == HomeWork.SIGNGLE:
            if not attrs.get('student'):
                raise serializers.ValidationError("作业为单人作业时，必须指定student关键字以创建评分对象")
            if attrs.get('group'):
                raise serializers.ValidationError("作业为单人作业时，只能指定student关键字")

        if attrs.get('homework').homeworktype in [HomeWork.GROUP, HomeWork.DOUBLE]:
            if not attrs.get('group'):
                raise serializers.ValidationError("作业为结对/团队作业时，必须指定group关键字以创建评分对象")
            if attrs.get('student'):
                raise serializers.ValidationError("作业为结对/团队作业时，只能指定group关键字")
        return attrs

    class Meta:
        model = Judgement
        fields = ('id', 'student', 'group', 'judger', 'homework', 'scoredatail', 'createat', )
        read_only_fields = ('id', 'creatat', 'judger', )
