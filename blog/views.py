from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

def post_list(request):
    post_list = Post.published.all()

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # Если PageNumber находится вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # Если PageNumber не целое число, то выдать первую страницу
        posts = paginator.page(1)
    context = {
        'posts': posts
    }
    return render(request=request, template_name='blog/post/list.html', context=context)

def post_detail(request,year, month, day, post):
    post = get_object_or_404(
        klass=Post, 
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    context = {
        'post': post
    }
    return render(request=request, template_name='blog/post/detail.html', context=context)

