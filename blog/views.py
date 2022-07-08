from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime
from .models import Post,Comment,Contact
from .forms import NowComment, PostCreateForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
User = settings.AUTH_USER_MODEL

def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
    
    context = {
        'title': 'الاخبار',
        'posts': posts,
        'page': page,
    }
    return render(request,'blog/blog.html',context)

def Post_detail(request,title, post_id):
    post = get_object_or_404(Post,pk=post_id)
    posts = Post.objects.all()
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)
    comments = post.comments.filter(active=True)
    comment_form = NowComment()
    next_comment = None
    context = {
            'title': post,
            'post':post,
            'posts': posts,
            'comments':comments,
            'comment_form': comment_form,
    }
   
    if request.method == 'POST':
        comment_form = NowComment(data=request.POST)
        if request.method == 'POST':
            comment_form = NowComment(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                comment_form = NowComment()
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)
                #messages.success(request,'تم ارسال التعليق بنجاح')
                # return render(request,'blog/comment_render.html')
            else:
                comment_form = NowComment()
    return render(request, 'blog/detail.html',context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title', 'content']
    template_name = 'blog/new_post.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
