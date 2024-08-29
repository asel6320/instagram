from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from webapp.forms import PostForm
from webapp.models import Post


class PostsListView(ListView):
    model = Post
    template_name = "posts/posts_list.html"
    context_object_name = "posts"
    paginate_by = 3
    ordering = ("-created_at",)

    def get_queryset(self):
        posts = super().get_queryset()
        if self.request.user.is_authenticated and not self.request.user.has_perm("webapp.view_post"):
            posts = posts.filter(author__in=self.request.user.following.all())
        return posts


class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_update.html"
    permission_required = "webapp.change_post"

    def has_permission(self):
        return self.request.user == self.get_object().author or super().has_permission()


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete.html"

    def has_permission(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse("accounts:profile", kwargs={"pk": self.request.user.pk})


class PostDetailView(DetailView):
    queryset = Post.objects.all()
    template_name = "posts/post_view.html"


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, pk, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.like_users.add(request.user)
        return JsonResponse({"like_count": post.like_users.count()})

    def delete(self, request, *args, pk, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.like_users.remove(request.user)
        return JsonResponse({"like_count": post.like_users.count()})


