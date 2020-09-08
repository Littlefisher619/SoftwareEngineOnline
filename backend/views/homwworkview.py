from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from backend.serializers.homworkserializer import HomeWorkSerializer
from backend.models import HomeWork


class HomeWorkViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes_by_action = {
        'create': [IsAdminUser, ],
        'list': [IsAuthenticated, ],
    }
    serializer_class = HomeWorkSerializer
    queryset = HomeWork.objects

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [IsAuthenticated])]

    def perform_create(self, serializer):
        serializer.validated_data['author'] = self.request.user
        serializer.save()

