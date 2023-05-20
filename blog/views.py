from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm

class PostListView(ListView):
    """
        Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

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


def post_share(request, post_id):
    # Изввлечь пост по идентификатору id
    post = get_object_or_404(
        klass=Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # ... отправить электронное письмо
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form
    }

    return render(request=request, template_name='blog/post/share.html', context=context)