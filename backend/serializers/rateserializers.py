from rest_framework import serializers

from backend.models import HomeWork, Group, Rate
from backend.serializers.jsonserializer import JsonSerializer
import json

class RateCreateSerializer(serializers.ModelSerializer):
    ratedetail = JsonSerializer(label='评分详情')

    def validate(self, attrs):
        super().validate(attrs)
        homework = attrs.get('homework')
        group = attrs.get('group')
        ratedetail = JsonSerializer().to_representation(attrs.get('ratedetail'))

        if homework is None or group is None or homework.homeworktype != HomeWork.GROUP or group.grouptype != Group.GROUP:
            raise serializers.ValidationError("需指定一个团队作业和团队类型的组才能进行评分")

        if Rate.objects.filter(homework=homework, group=group).exists():
            raise serializers.ValidationError("评分已经存在，只能对一个作业创建一个评分")

        '''
        [
            {
                "member": 1,
                "rate": 10,
            },
        ]
        '''

        members_in_group = json.loads(group.members)

        try:
            assert isinstance(ratedetail, list), "评分信息必须是一个列表"
            total_rate = 0
            member_count = 0
            for data in ratedetail:
                assert isinstance(data, dict), "评分项目必须是Dict类型的数据"
                assert len(data) == 2, "数据字段数量不正确"
                member = data['member']
                rate = data['rate']
                assert data.keys
                assert isinstance(rate, int) and 0 <= rate <= 100, "评分必须是[0,100]间的整数"
                assert member in members_in_group or member == group.leader.id, "只能对自己以及组员评分"
                total_rate += rate
                member_count += 1
            assert member_count == len(members_in_group) + 1, "必须对包含自己在内的所有组员都评分"
            assert total_rate == 100, "评分的总和必须为100"

        except KeyError:
             raise serializers.ValidationError("提交的评分信息缺少重要字段")
        except TypeError:
             raise serializers.ValidationError("提交的评分信息数据类型不正确")
        except AssertionError as e:
            raise serializers.ValidationError(e.__str__())
        except json.decoder.JSONDecodeError:
            raise serializers.ValidationError("不是一个有效的JSON数据")
        return attrs

    class Meta:
        model = Rate
        fields = ('id', 'createat', 'homework', 'group', 'ratedetail')
        read_only_fields = ('id', 'createat',)

