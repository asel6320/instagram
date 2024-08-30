from rest_framework import serializers

from accounts.models import User
from webapp.models import Post

class PostSerializer(serializers.ModelSerializer):
    like_users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all())
    class Meta:
        model = Post
        fields = ["id", "image", "content", "created_at", "updated_at", "author", "like_users"]
        read_only_fields = ["id", "created_at", "updated_at", "author", "like_users"]

