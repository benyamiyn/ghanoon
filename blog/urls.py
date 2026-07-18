from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path(
        "<slug:slug>/",
        views.maqale_detail,
        name="detail",
    ),
    path(
        "<slug:slug>/comment/add/",
        views.add_comment,
        name="add_comment",
    ),
    path(
        "<slug:slug>/like/",
        views.toggle_like,
        name="toggle_like",
    ),
]
