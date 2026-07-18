from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Comment, Like, Maqale


def home(request):
    maqaleha = (
        Maqale.objects.select_related(
            "author",
            "category",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "blog/home.html",
        {
            "maqaleha": maqaleha,
        },
    )


def maqale_detail(request, slug):

    maqale = get_object_or_404(
        Maqale.objects.select_related(
            "author",
            "category",
        ),
        slug=slug,
    )

    comments = (
        maqale.comments.filter(
            parent__isnull=True,
            is_active=True,
        )
        .select_related("author")
        .prefetch_related("children")
    )

    like_count = maqale.likes.count()

    is_liked = False

    if request.user.is_authenticated:

        is_liked = Like.objects.filter(
            maqale=maqale,
            user=request.user,
        ).exists()

    context = {
        "maqale": maqale,
        "comments": comments,
        "like_count": like_count,
        "is_liked": is_liked,
    }

    return render(
        request,
        "blog/post_detail.html",
        context,
    )


@login_required
def add_comment(request, slug):

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    maqale = get_object_or_404(
        Maqale,
        slug=slug,
    )

    form = CommentForm(request.POST)

    if form.is_valid():

        comment = form.save(commit=False)
        comment.maqale = maqale
        comment.author = request.user

        parent_id = form.cleaned_data.get("parent_id")

        if parent_id:

            parent_comment = Comment.objects.filter(
                id=parent_id,
                maqale=maqale,
                is_active=True,
            ).first()

            if parent_comment:
                comment.parent = parent_comment

        comment.save()

        messages.success(
            request,
            "نظر شما ثبت شد.",
        )

    else:

        messages.error(
            request,
            "متن نظر نمی‌تواند خالی باشد.",
        )

    return redirect(
        maqale.get_absolute_url(),
    )


@login_required
def toggle_like(request, slug):

    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    maqale = get_object_or_404(
        Maqale,
        slug=slug,
    )

    like, created = Like.objects.get_or_create(
        maqale=maqale,
        user=request.user,
    )

    if created:

        messages.success(
            request,
            "مقاله لایک شد.",
        )

    else:

        like.delete()

        messages.info(
            request,
            "لایک حذف شد.",
        )

    return redirect(
        maqale.get_absolute_url(),
    )