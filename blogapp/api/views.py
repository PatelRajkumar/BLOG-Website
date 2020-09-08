from rest_framework import viewsets
from blogapp.models import Post,Comment
from .serializers import PostSerializer,CommentSerializer
class PostCRUDCBV(viewsets.ModelViewSet):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
class CommentCRUDCBV(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    