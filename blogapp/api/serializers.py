from rest_framework.serializers import ModelSerializer
from blogapp.models import Post,Comment
class PostSerializer(ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'
class CommentSerializer(ModelSerializer):
    class Meta:
        model=Comment 
        fields='__all__'