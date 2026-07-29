from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from blog.models import Maqale
from .forms import SearchForm


def search(request):

    form = SearchForm(request.GET)

    articles = Maqale.objects.none()

    q = ""

    if form.is_valid():

        q = form.cleaned_data.get("q", "")
        sort = form.cleaned_data.get("sort", "")

        if q:

            articles = (
                Maqale.objects.select_related(
                    "author",
                    "category",
                )
                .filter(
                    Q(title__icontains=q)
                    | Q(matn__icontains=q)
                    | Q(author__username__icontains=q)
                    | Q(category__title__icontains=q)
                )
                .distinct()
            )

            if sort == "newest":

                articles = articles.order_by(
                    "-created_at"
                )

            elif sort == "oldest":

                articles = articles.order_by(
                    "created_at"
                )

            elif sort == "title":

                articles = articles.order_by(
                    "title"
                )

            else:

                articles = articles.order_by(
                    "-created_at"
                )

    context = {
        "form": form,
        "articles": articles,
        "query": q,
    }

    return render(
        request,
        "search/search_results.html",
        context,
    )


def suggest(request):

    q = request.GET.get("q", "")

    data = []

    if q:

        data = list(
            Maqale.objects.filter(
                title__icontains=q
            )
            .values_list(
                "title",
                flat=True,
            )[:5]
        )

    return JsonResponse(
        data,
        safe=False,
    )


def live_search(request):

    q = request.GET.get("q", "")

    articles = Maqale.objects.none()

    if q:

        articles = (
            Maqale.objects.select_related(
                "author",
                "category",
            )
            .filter(
                Q(title__icontains=q)
                | Q(matn__icontains=q)
                | Q(author__username__icontains=q)
                | Q(category__title__icontains=q)
            )
            .distinct()
            .order_by("-created_at")[:10]
        )

    return render(
        request,
        "search/live_results.html",
        {
            "articles": articles,
        },
    )