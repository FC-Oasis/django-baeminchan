from rest_framework import serializers

from members.serializers import UserSimpleSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
