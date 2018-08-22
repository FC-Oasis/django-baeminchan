from django.http import Http404
from rest_framework import generics

from comment import permissions
from ..serializers import CommentSerializer
from ..models import Comment


class CommentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(product=self.request.query_params.get('product_id'))
        if queryset:
            return queryset
        else:
            raise Http404

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
