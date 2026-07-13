from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.db.models import Q
from blog.models import Maqale
from .forms import SearchForm 



def search(requests):
    form = SearchForm(requests.GET)
    
    articles = Maqale.objects.none()
    #استخراج متن 
    
    if form.is_valid():
        #اگر فرم معتبر بود ادامه بده 
        
        q = form.cleaned_data["q"]
        
        if q:
            
            
            articles = Maqale.objects.filter(
            Q(title__icontains=q) |
            Q(matn__icontains=q) |
            Q(author__username__icontains=q) |
            Q(category__title__icontains=q)
            #قرار است جست و جو را روی عنوان نویسنده متن مقاله و و دسته بندی آن انجام دهیم
        ).distinct()
            
    sort = form.cleaned_data["sort"]
    
    if sort == "newest":
        
        articles = articles.order_by["-created_at"]
        
    elif sort == "o0ldest" :
        
        articles = articles.order_by["created_at"]
        
    elif sort == "title":
        
        articles = articles.order_by["title"]
        
    context = {
        "form":form,
        "articles":articles,
        "query": q if form.is_valid() else "",
    
    }
    return render(requests,"search/results.html",context)
#مرتب سازی بر اساس زمان نوشتن مقاله یا جیدید ترین یا قدیمی ترین یا مرتب سازی کلا بر اساس عنوان مقاله 
def suggest(request):
    q = request.GET.get("q","")
    data = []
    if q :
        data = list(
            Maqale.objects.filter(
                title_icontains=q
            ).values_list(
                "title",
                flat=True
            )[:5]
        )
    return JsonResponse(data, safe=False)