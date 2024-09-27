from api.permissions import IsOwnerOrIsStaffOrReadOnly
from api.serializers import CarSerializer
from cars.models import Car
from rest_framework import mixins, viewsets


class CarViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    """View set that process requests related to car instances."""
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsOwnerOrIsStaffOrReadOnly, )

    def perform_create(self, serializer):
        # Set the author to the request user when creating a car
        serializer.save(owner=self.request.user)
