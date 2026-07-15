from django.shortcuts import render, get_object_or_404
from .models import Maqale

# Create your views here.

def maqale_detail(request,slug):
    maqale = get_object_or_404(
        Maqale,
        slug = slug
    )
    context = {
        "maqale" : maqale,
    }
    return render(
        request,
        "blog/post_detail.html",
        context
    )
    

