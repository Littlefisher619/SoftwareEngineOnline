from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from backend.filters import JudgementFilter
from backend.models import Judgement, User
from backend.serializers.judgementserializers import *


class JudgementViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    serializer_class = JudgementInfoSerializer
    queryset = Judgement.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_class = JudgementFilter
    filter_backend = (SearchFilter,)

    def get_serializer_class(self):
        print(self.action)
        if self.action in ['update', 'partial_update']:
            return JudgementUpdateSerializer
        else:
            return JudgementInfoSerializer

    def update(self, request, *args, **kwargs):
        if self.request.user != self.get_object().judger:
            return Response({
                    'success': False,
                    'message': '只能修改自己创建的评分'
                }, status=status.HTTP_200_OK)
        return super().update(request, *args, **kwargs)

    @action(methods=['POST'], url_path='create', detail=False)
    def _create(self, request):
        if self.request.user.role != User.TEST_GROUP:
            return Response({
                    'success': False,
                    'message': '不是测试组的成员不能创建评分诶'
                }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                'success': True,
                'message': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.validated_data['judger'] = self.request.user
        serializer.save()

