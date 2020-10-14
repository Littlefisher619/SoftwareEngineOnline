from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from backend.filters import RateFilter
from backend.models import Rate
from backend.serializers.rateserializers import RateCreateSerializer

class RateViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = RateCreateSerializer
    queryset = Rate.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_class = RateFilter

    @action(methods=['POST'], url_path='create', detail=False)
    def _create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.validated_data['group']
        if self.request.user != group.leader:
            return Response({
                    'success': False,
                    'message': '你不是这个组的队长，不能评分！'
                }, status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)

        return Response(
            {
                'success': True,
                'message': '创建成功',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save()
