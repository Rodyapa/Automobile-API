from api.permissions import (IsAuthorOrIsStaffOrReadOnly,
                             IsOwnerOrIsStaffOrReadOnly)
from api.serializers import CarSerializer, CommentSerializer
from cars.models import Car
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
    http_method_names = ['get', 'post', 'put', 'delete']

    def perform_create(self, serializer):
        # Set the author to the request user when creating a car
        serializer.save(owner=self.request.user)


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """Вьюсет для обьектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrIsStaffOrReadOnly,
    )
    http_method_names = ['get', 'post']
    filter_backends = (OrderingFilter,)
    ordering = ('created_at',)

    def get_car(self):
        car = get_object_or_404(
            Car, id=self.kwargs['car_id']
        )
        return car

    def get_queryset(self):
        return self.get_car().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            car=self.get_car()
        )
