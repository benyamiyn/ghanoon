from django.urls import path
from . import views

app_name = "search"

urlpatterns = [
    path("", views.search, name="search"),
    path(
    "suggest/",
    views.suggest,
    name="suggest"
    ),
    path(
        "live",
        views.live_search,
        name = "live"
    )
]
# تعریف کردن مسیری برای اپ
#مسیری برای فیچر های جست و جو پیشنهادی و جست و جو زنده 