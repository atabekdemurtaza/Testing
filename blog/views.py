from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts
    }
    return render(request=request, template_name='blog/post/list.html', context=context)

def post_detail(request, pk):
    post = get_object_or_404(klass=Post, pk=pk, status=Post.Status.PUBLISHED)
    context = {
        'post': post
    }
    return render(request=request, template_name='blog/post/detail.html', context=context)

