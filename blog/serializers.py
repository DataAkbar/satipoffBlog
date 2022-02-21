from rest_framework import serializers
from .models import Blog


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'title', 'category', 'created_at',)
        model = Blog