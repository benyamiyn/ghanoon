from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "حساب کاربری با موفقیت ایجاد شد",
            )

            return redirect("blog:home")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


@login_required
def profile_view(request):

    return render(
        request,
        "accounts/profile.html",
        {
            "profile_user": request.user
        },
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user,
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile,

        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            messages.success(
                request,
                "پروفایل بروزرسانی شد",
            )

            return redirect("accounts:profile")

    else:

        user_form = UserUpdateForm(
            instance=request.user,
        )

        profile_form = ProfileUpdateForm(
            instance=request.user.profile,
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
        }
    )