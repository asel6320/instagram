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


# Create your views here.
@ensure_csrf_cookie
def get_csrf_token(request):
    if request.method == 'GET':
        return HttpResponse()
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])

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
        post.like_users.add(request.user)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        post.like_users.remove(request.user)
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)