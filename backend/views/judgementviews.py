from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from backend.models import Judgement, User
from backend.serializers.judgementserializers import *


class JudgementViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = JudgementInfoSerializer
    queryset = Judgement.objects.all()
    permission_classes = [IsAuthenticated, ]


    @action(methods=['POST'], url_path='create', detail=False)
    def _create(self, request):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                    'success': False,
                    'message': '不是测试组的成员不能创建评分诶'
                }, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer.validated_data['']



        # if Group.objects.filter(leader=self.request.user, grouptype=serializer.validated_data['grouptype']).exists():
        #     return Response({
        #         'success': False,
        #         'message': '你已经是当前队伍类型的组长了，不能再创建新的队伍'
        #     }, status=status.HTTP_200_OK)
        #
        # for data in Group.objects.filter(grouptype=serializer.validated_data['grouptype']).values('members'):
        #     if self.request.user.pk in json.loads(data['members']):
        #         return Response({
        #             'success': False,
        #             'message': '你已经是当前队伍类型的某个组的组员，不能再创建新的队伍'
        #         }, status=status.HTTP_200_OK)
        #
        #
        self.perform_create(serializer)
        # return Response(
        #     {
        #         'success': True,
        #         'message': '创建成功',
        #         'data': serializer.data
        #     }, status=status.HTTP_201_CREATED
        # )

    def perform_create(self, serializer):
        serializer.validated_data['judger'] = self.request.user
        serializer.validated_data['members'] = json.dumps([self.request.user.pk,])
        serializer.save()

