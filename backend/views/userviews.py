import json

from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from SoftwareEngineOnline import settings
from backend.serializers.groupserializers import *
from backend.serializers.userserializers import *
from backend.serializers.judgementserializers import *

import hashlib
import json

from os import urandom

class UserViewSetNormal(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    serializer_classes_by_action = {
        'updatepassword':  UserUpdatePasswordSerializer,
        'mygroup': GroupTokenSerializer,
        'groupinfo': GroupInfoSerializer,
        'judgements': JudgementInfoSerializer,
    }
    # lookup_field = 'stuid'
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.role != User.TEST_GROUP and self.request.user != self.get_object():
            return Response({
                    'success': False,
                    'message': '你走错地方惹，这儿啥也没有~'
                }, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                    'success': False,
                    'message': '你走错地方惹，这儿啥也没有~'
                }, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        serializer_class = self.serializer_classes_by_action.get(self.action, UserInfoSerializer)
        return serializer_class

    @action(methods=['GET'], detail=False, name='我的个人资料')
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def __serialize_group_info_data(self, user):
        assert self.action in ['groupinfo', 'mygroup']
        double_group, big_group = Group.filter_group_by_from_user(user)
        data = {
            'double': None,
            'big': None
        }

        if double_group:
            data['double'] = self.get_serializer(double_group).data
        if big_group:
            data['big'] = self.get_serializer(big_group).data
        return data

    @action(methods=['GET'], detail=False, name='评分查询')
    def judgements(self, request):
        double_group, big_group = Group.filter_group_by_from_user(self.request.user)
        data = dict()
        data['big'] = self.get_serializer(Judgement.objects.filter(group=big_group), many=True).data if big_group else []
        data['double'] = self.get_serializer(Judgement.objects.filter(group=double_group), many=True).data if double_group else []
        data['single'] = self.get_serializer(Judgement.objects.filter(student=self.request.user), many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True, name='组队查询')
    def groupinfo(self, request, pk):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                    'success': False,
                    'message': '你走错地方惹，这儿啥也没有~'
                }, status=status.HTTP_403_FORBIDDEN)
        return Response(
            self.__serialize_group_info_data(self.get_object()),
            status=status.HTTP_200_OK
        )

    @action(methods=['GET'], detail=False, name='我的组队')
    def mygroup(self, request):
        return Response(
            self.__serialize_group_info_data(self.request.user),
            status=status.HTTP_200_OK
        )

    @action(methods=['POST'], detail=False, name='修改密码')
    def updatepassword(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({
            'success': True,
            'message': '密码已修改'
        }, status=status.HTTP_200_OK)



    @action(methods=['GET'], detail=True, name='重置密码')
    def resetpassword(self, request, pk=None):
        if not self.request.user.is_staff:
            return Response({
                    'success': False,
                    'message': '你没有权限给别人重置密码QwQ'
                }, status=status.HTTP_403_FORBIDDEN)

        new_pwd = hashlib.md5(urandom(64)).hexdigest()
        user = self.get_object()

        subject = '福大软工在线-密码找回'
        message = f'您好，{user.stuname}！\n您在福大软工在线平台的密码已重置，新密码是：{new_pwd}\n新密码是随机生成的如果觉得新密码不满意可以随后登录系统进行修改密码~'
        email = EmailMessage(subject, message, to=[user.email])
        email.send()
        '''
            TO-DO:
            Using Cryptographic-signing in Django to implements reset password by a link.
        '''
        user.set_password(new_pwd)
        # user.save()

        return Response({
            'success': True,
            'message': '密码重置成功！'
        }, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, name='排行榜')
    def rank(self, request):
        def get_and_append_if_not_exist(student, rankdict):
            if student.id not in rankdict:
                rankdict[student.id] = UserSimpleSerializer(student).data
                rankdict[student.id]['scoredetail'] = []
                rankdict[student.id]['totalscore'] = 0.00
            if student.id not in has_score:
                has_score[student.id] = {}
            return rankdict[student.id]

        def append_record(student, homework, score, rank_item, factor=1.00):

            if score is not None:
                if homework.homeworktype != HomeWork.SINGLE:
                    factor *= 10
                score = score * homework.weight * factor
                score = round(score, 2)
                rank_item['scoredetail'].append({
                    'homework': homework.id,
                    'weight': homework.weight,
                    'factor': factor,
                    'score': score
                })

                rank_item['totalscore'] =  round(rank_item['totalscore']+score, 2)
                has_score[student.id][homework.id] = True
            else:
                rank_item['scoredetail'].append({
                    'homework': homework.id,
                    'weight': homework.weight,
                    'factor': None,
                    'score': None
                })
                has_score[student.id][homework.id] = False

        judgements = Judgement.objects.select_related('homework', 'group', 'student')
        allstudents = User.objects.all()
        rank_excludes = User.objects.filter(~Q(role__in=[User.GROUP_MEMBER, User.GROUP_LEADER]))
        homeworks = HomeWork.objects.all()

        rank = {}
        has_score = {}
        for judgement in judgements:
            student = judgement.student
            group = judgement.group

            homework = judgement.homework

            if student:
                rank_item = get_and_append_if_not_exist(student, rank)
                append_record(student, homework, judgement.totalscore, rank_item)
            elif group:
                group_members = json.loads(group.members)
                group_members.append(group.leader)
                if group.grouptype == Group.GROUP:
                    rate = []
                    try:
                        rate = json.loads(Rate.objects.get(group=group, homework=homework).ratedetail)
                    except Rate.DoesNotExist:
                        pass
                    for rate_item in rate:
                        try:
                            pk = rate_item['member']
                            student = User.objects.get(pk=pk)
                            rate_factor = rate_item['rate']
                            rank_item = get_and_append_if_not_exist(student, rank)
                            append_record(student, homework, judgement.totalscore, rank_item, rate_factor/100.00)
                        except User.DoesNotExist:
                            pass

                elif group.grouptype == Group.DOUBLE:
                    for member in group_members:
                        pk = member
                        student = User.objects.get(pk=pk)
                        rank_item = get_and_append_if_not_exist(student, rank)
                        append_record(student, homework, judgement.totalscore, rank_item, 0.50)

        for student in allstudents:
            rank_item = get_and_append_if_not_exist(student, rank)
            for homework in homeworks:
                if homework.id not in has_score[student.id]:
                    append_record(student, homework, None, rank_item)

        for student in rank_excludes:
            if student.id in rank:
                rank.pop(student.id)

        rankdata = list(rank.values())
        rankdata.sort(key=lambda rank_item: rank_item['totalscore'], reverse=True)
        count = 1
        for i in rankdata:
            i['rank'] = count
            i['scoredetail'].sort(key=lambda scoredetail: scoredetail['homework'])
            count += 1

        return Response(rankdata, status=status.HTTP_200_OK)
