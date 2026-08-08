from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = "account"


urlpatterns = [

    path(
        "register/",
        views.register_view,
        name="register",
    ),


    path(
        "profile/",
        views.profile_view,
        name="profile",
    ),


    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile",
    ),


    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="account/login.html"
        ),
        name="login",
    ),


    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),


    path(
        "member/<int:id>/",
        views.member_profile,
        name="member_profile"
    ),


    path(
        "members/",
        views.members,
        name="members"
    ),


    path(
        "members/<int:id>/delete/",
        views.delete_member,
        name="delete_member"
    ),


    path(
        "members/<int:id>/update-role/",
        views.update_member_role,
        name="update_member_role",
    ),

]