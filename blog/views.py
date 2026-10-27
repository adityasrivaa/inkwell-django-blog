
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.utils.text import slugify

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment


def home(request):
    posts = Post.objects.select_related(
        "author", "category"
    ).all()

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    if query:
        posts = posts.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(author__username__icontains=query)
            | Q(category__name__icontains=query)
        )

    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    categories = Category.objects.all()

    return render(
        request,
        "blog/home.html",
        {
            "posts": posts,
            "categories": categories,
            "query": query,
            "selected_category": category_slug,
        },
    )


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("author", "category"),
        slug=slug,
    )

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to comment.")
            return redirect("login")

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            messages.success(
                request,
                "Comment added successfully!",
            )

            return redirect(
                post.get_absolute_url() + "#comments"
            )

        messages.error(
            request,
            "Please correct the errors in your comment.",
        )

    else:
        comment_form = CommentForm()

    comments = post.comments.select_related(
        "author"
    ).order_by("-created_at")

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


def unique_post_slug(title, instance=None):
    base_slug = slugify(title) or "post"
    slug = base_slug
    counter = 1

    posts = Post.objects.all()

    if instance:
        posts = posts.exclude(pk=instance.pk)

    while posts.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = unique_post_slug(post.title)
            post.save()

            messages.success(
                request,
                "Your blog post was published.",
            )

            return redirect(post.get_absolute_url())

    else:
        form = PostForm()

    return render(
        request,
        "blog/post_form.html",
        {
            "form": form,
            "page_title": "Write a Blog",
        },
    )


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author_id != request.user.id:
        return HttpResponseForbidden(
            "You can edit only your own blog posts."
        )

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            messages.success(
                request,
                "Your blog post was updated.",
            )

            return redirect(post.get_absolute_url())

    else:
        form = PostForm(instance=post)

    return render(
        request,
        "blog/post_form.html",
        {
            "form": form,
            "page_title": "Edit Blog",
        },
    )


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if post.author_id != request.user.id:
        return HttpResponseForbidden(
            "You can delete only your own blog posts."
        )

    if request.method == "POST":
        post.delete()

        messages.success(
            request,
            "Your blog post was deleted.",
        )

        return redirect("home")

    return render(
        request,
        "blog/post_confirm_delete.html",
        {"post": post},
    )


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(
        Comment.objects.select_related("post"),
        pk=pk,
    )

    if (
        comment.author_id != request.user.id
        and comment.post.author_id != request.user.id
    ):
        return HttpResponseForbidden(
            "You cannot delete this comment."
        )

    if request.method == "POST":
        post_url = comment.post.get_absolute_url()
        comment.delete()

        messages.success(request, "Comment deleted.")

        return redirect(post_url + "#comments")

    return HttpResponseForbidden(
        "POST request required."
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully.",
            )

            return redirect("home")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )
