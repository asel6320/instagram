from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse

from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from api_v3.pagination import PostPagination
from api_v3.permissions import IsOwnerOrReadOnly
from api_v3.serializers import PostSerializer
from webapp.models import Post

User = get_user_model()
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user not in post.like_users.all():
            post.like_users.add(user)
            post.save()
            return Response({'status': 'liked', 'like_users': post.like_users.values_list('id', flat=True)},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.like_users.all():
            post.like_users.remove(user)
            post.save()
            return Response({'status': 'unliked', 'like_users': post.like_users.values_list('id', flat=True)},
                            status=status.HTTP_200_OK)
        else:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)