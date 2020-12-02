from rest_framework import serializers
from rest_framework.fields import ChoiceField

from backend.models import Judgement, Group, HomeWork
from .authserializers import UserInfoSerializer
from .groupserializers import GroupInfoSerializer
from .homworkserializer import HomeWorkSerializer
from .jsonserializer import JsonSerializer
import re

class JudgementUpdateSerializer(serializers.ModelSerializer):
    scoredetail = JsonSerializer(label='评分详情')

    def validate(self, attrs):
        super().validate(attrs)
        scoredetail = JsonSerializer().to_representation(attrs.get('scoredetail'))

        try:
            assert isinstance(scoredetail, dict), "评分数据必须是Dict类型的数据"
            assert len(scoredetail) == 3, "数据字段数量不正确"

            bonus = scoredetail['bonus']
            points = scoredetail['scorepoints']

            totalscore = 0.0
            for point in points:
                assert isinstance(point, dict), "评分项目必须是Dict类型的数据"
                assert len(point) == 2, "数据字段数量不正确"
                assert re.match(r'^\d+\.\d+$', point['point']) is not None, "point字段格式需为X.Y"
                assert isinstance(point['score'], int), "score字段需为整数"

                totalscore += point['score']
            totalscore *= (1 + bonus)
            if totalscore < 0:
                totalscore = 0
            totalscore = round(totalscore, 2)
            attrs['totalscore'] = totalscore
            scoredetail['score'] = totalscore
            attrs['scoredetail'] = JsonSerializer().to_internal_value(scoredetail)
        except AssertionError as e:
            raise serializers.ValidationError(e.__str__())
        except KeyError:
             raise serializers.ValidationError("提交的评分信息缺少重要字段")
        except TypeError:
             raise serializers.ValidationError("提交的评分信息数据类型不正确")
        return attrs

    class Meta:
        model = Judgement
        fields = ('id', 'scoredetail', 'totalscore','createat',)
        read_only_fields = ('id', 'createat', 'totalscore',)


class JudgementCreateSerializer(serializers.ModelSerializer):
    scoredetail = JsonSerializer(label='评分详情')
    judger = UserInfoSerializer(label='评分员', read_only=True)
    # homework = HomeWorkSerializer(label='作业')

    def validate(self, attrs):
        super().validate(attrs)
        if attrs.get('homework') is None:
            raise serializers.ValidationError("需指定一个作业才能进行评分")

        if attrs.get('homework').homeworktype == HomeWork.SINGLE:
            if not attrs.get('student'):
                raise serializers.ValidationError("作业为单人作业时，必须指定student关键字以创建评分对象")
            if attrs.get('group'):
                raise serializers.ValidationError("作业为单人作业时，只能指定student关键字")
            if Judgement.objects.filter(homework=attrs.get('homework'), student=attrs.get('student')):
                raise serializers.ValidationError("对当前学生的这一项单人作业评分已经存在")

        if attrs.get('homework').homeworktype in [HomeWork.GROUP, HomeWork.DOUBLE]:
            if not attrs.get('group'):
                raise serializers.ValidationError("作业为结对/团队作业时，必须指定group关键字以创建评分对象")
            if attrs.get('student'):
                raise serializers.ValidationError("作业为结对/团队作业时，只能指定group关键字")
            if Judgement.objects.filter(homework=attrs.get('homework'), group=attrs.get('group')):
                raise serializers.ValidationError("对当前队伍的这一项结对/团队作业评分已经存在")

        scoredetail = JsonSerializer().to_representation(attrs.get('scoredetail'))

        try:
            bonus = scoredetail['bonus']
            points = scoredetail['scorepoints']
            totalscore = 0.0
            for point in points:
                assert isinstance(point, dict), "评分项目必须是Dict类型的数据"
                assert len(point) == 2, "数据字段数量不正确"
                assert re.match(r'^\d+\.\d+$', point['point']) is not None, "point字段格式需为X.Y"
                assert isinstance(point['score'], int), "score字段需为整数"
                totalscore += point['score']

            totalscore *= (1 + bonus)
            if totalscore < 0:
                totalscore = 0

            totalscore = round(totalscore, 2)
            attrs['totalscore'] = totalscore
            attrs['scoredetail'] = JsonSerializer().to_internal_value(scoredetail)
        except KeyError:
             raise serializers.ValidationError("提交的评分信息不正确")
        except TypeError:
             raise serializers.ValidationError("提交的评分信息不正确")
        except AssertionError as e:
            raise serializers.ValidationError(e.__str__())

        return attrs

    class Meta:
        model = Judgement
        fields = ('id', 'student', 'group', 'judger', 'homework', 'scoredetail', 'totalscore', 'createat', )
        read_only_fields = ('id', 'createat', 'judger', 'totalscore')


class JudgementInfoSerializer(serializers.ModelSerializer):
    scoredetail = JsonSerializer(label='评分详情')
    # totalscore = serializers.SerializerMethodField()
    # judger = UserInfoSerializer(label='评分员', read_only=True)
    student = UserInfoSerializer(label='学生', read_only=True)
    group = GroupInfoSerializer(label='组', read_only=True)
    # homework = HomeWorkSerializer(label='作业')

    # def get_total_socre(self, group):
    #     try:
    #         JsonSerializer().to_representation(self.scoredetail)
    #     except Exception:
    #         return None

    class Meta:
        model = Judgement
        fields = ('id', 'student', 'group', 'homework', 'scoredetail', 'createat', 'totalscore', 'blogurl')
        read_only_fields = fields
