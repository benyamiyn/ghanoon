from django.shortcuts import render
from django.db.models import Q

from blog.models import Maqale
from .forms import SearchForm 

def search(requests):
    form = SearchForm(requests.GET)
    
    articles = Maqale.objects.none()
    
    if form.is_valid():
        
        q = form.cleaned_data["q"]
        
        if q:
            
            
            articles = Maqale.objects.filter(
            Q(title__icontains=q) |
            Q(matn__icontains=q) |
            Q(author__username__icontains=q) |
            Q(category__title__icontains=q)
        ).distinct()
    context = {
        "form":form,
        "articles":articles,
        "query": q if form.is_valid() else "",
        
    }
    return render(requests,"search/results.html",context)
            