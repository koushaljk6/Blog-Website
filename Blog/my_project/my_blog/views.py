from typing import Any, Optional
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Post
from django.urls import reverse_lazy, reverse
from .forms import UserRegisterForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .forms import CommentForm


# Create your views here.
class LandingPageView(ListView):
    template_name = "my_blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:2]
        return data


class AllPostView(LoginRequiredMixin, ListView):
    template_name = "my_blog/all_posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class DetailPostView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")

        }
        return render(request, "my_blog/post_detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("detail_posts_page", args=[slug]))

        context = {
            "post": post,
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id")
        }

        return render(request, "my_blog/post_detail.html", context)


def Contactview(request):
    return render(request, "my_blog/contact.html")


class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = "my_blog/register.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "my_blog/create_post.html"
    fields = ['title', 'token', 'slug', 'image', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy("posts_page")


class PostUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    template_name = "my_blog/create_post.html"
    model = Post
    fields = ['title', 'token', 'image', 'content']
    success_url = reverse_lazy('posts_page')

    def form_valid(self, form):
        form.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = Post
    success_url = reverse_lazy('posts_page')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False