from cars.models import Car, Comment
from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    """Serializer for Car model instances."""
    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ['owner', ]


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model instances."""

    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'author',
            'created_at',
        ]
        read_only_fields = ['id', 'author', 'created_at']
