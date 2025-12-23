from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def get_posts():
    now = timezone.now()
    posts = Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now
    )
    return posts


def index(request):
    post_list = get_posts()[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(
        get_posts(),
        pk=id
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    now = timezone.now()
    post_list = category.posts.select_related(
        'author', 'location'
    ).filter(
        is_published=True,
        pub_date__lte=now
    )

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
