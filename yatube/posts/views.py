from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
# from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post

amount = 10
User = get_user_model()


def index(request):

    template = 'posts/index.html'
    post_list = Post.objects.all()
    text = 'Это главная страница проекта Yatube'
    title = 'Main page'

    paginator = Paginator(post_list, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'text': text,
        'posts': post_list,
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()

    paginator = Paginator(post_list, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Сообщества',
        'group': group,
        'posts': post_list,
        'self_title': group.__str__,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    posts_count = posts.count()
    title = f'Профайл пользователя {username}'

    paginator = Paginator(posts, amount)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'username': username,
        'posts': posts,
        'posts_count': posts_count,
        'title': title,
        'page_obj': page_obj,
        'author': user,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post_text': post.text,
        'post': post,
    }
    return render(request, template, context)


def post_create(request):
    template = 'posts/create_post.html'

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author.username)

        return render(request, template, {
            'form': form,
            'title': 'Новый пост',
        })

    form = PostForm()
    return render(request, template, {
        'form': form,
        'title': 'Новый пост',
    })


def post_edit(request, post_id):
    template = 'posts/create_post.html'

    post = get_object_or_404(Post, pk=post_id)
    current_user = request.user

    if current_user != post.author:
        return redirect('posts:post_detail', post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = current_user
            post.save()
            return redirect('posts:post_detail', post_id)

        return render(request, template, {
            'form': form,
            'title': 'Редактировать пост',
            'is_edit': True,
            'post': post,
        })
    form = PostForm()
    return render(request, template, {
        'form': form,
        'title': 'Редактировать пост',
        'is_edit': True,
        'post_id': post_id,
    })
