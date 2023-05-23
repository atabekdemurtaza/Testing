from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
from .models import Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count

class PostListView(ListView):
    """
        Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(klass=Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
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
        'posts': posts,
        'tag': tag
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

    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()

    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts
    }
    return render(request=request, template_name='blog/post/detail.html', context=context)


def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(
        klass=Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            # ... отправить электронное письмо
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}'s comment: {cd['comments']}"
            send_mail(subject, message, 'sprintdeliveryapp@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent
    }

    return render(request=request, template_name='blog/post/share.html', context=context)

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(klass=Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    # Комментарии отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать обьект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }

    return render(request=request, template_name='blog/post/comment.html', context=context)
