from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse

from .forms import CommentForm
from .models import Comment, Maqale, Like

# Create your views here.
def maqale_detail(request, slug):
    maqale = get_object_or_404(Maqale, slug=slug)
    
    comments = (
        maqale.comments.filter(is_active=True, parent__isnull=True)
        .select_related("author")
        .prefetch_related("children__author")
    )
    form = CommentForm()

    liked = False
    if request.user.is_authenticated:
        liked = maqale.likes.filter(user=request.user).exists()
    
    context = {
        "maqale": maqale,
        "comments": comments,
        "form": form,
        "liked": liked,
        "likes_count": maqale.likes.count(),
    }
    return render(request, "blog/post_detail.html", context)
    
    
@login_required
def add_comment(request, slug):
    
    maqale = get_object_or_404(Maqale, slug=slug)
    
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
        
    form = CommentForm(request.POST)
        
    if form.is_valid():
            
        parent = None
        parent_id = form.cleaned_data.get("parent_id")
                  
        if parent_id:
            parent = get_object_or_404(
                Comment,
                pk=parent_id,
                maqale=maqale,
                is_active=True,
            )

        Comment.objects.create(
            maqale=maqale,
            author=request.user,
            parent=parent,
            text=form.cleaned_data["text"],
        )

    return redirect("blog:detail", slug=maqale.slug)


@login_required
def toggle_like(request, slug):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    maqale = get_object_or_404(Maqale, slug=slug)

    like = Like.objects.filter(maqale=maqale, user=request.user).first()

    if like:
        like.delete()
        liked = False
    else:
        Like.objects.create(maqale=maqale, user=request.user)
        liked = True

    likes_count = maqale.likes.count()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(
            {
                "liked": liked,
                "likes_count": likes_count,
            }
        )

    return redirect("blog:detail", slug=maqale.slug)
