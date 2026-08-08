from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from django.contrib import messages

from .forms import (
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)



def is_owner(user):
    return user.is_superuser





@login_required
@user_passes_test(is_owner)
def members(request):

    members = User.objects.all()

    q = request.GET.get("q")


    if q:

        members = members.filter(
            username__icontains=q
        ) | members.filter(
            email__icontains=q
        )



    return render(
        request,
        "accounts/members.html",
        {
            "members": members
        }
    )







@login_required
@user_passes_test(is_owner)
def member_profile(request, id):

    member = get_object_or_404(
        User,
        id=id
    )


    comment_count = member.comments.count()



    context = {

        "member": member,

        "comment_count": comment_count,

    }



    return render(
        request,
        "accounts/member_profile.html",
        context
    )








@login_required
@user_passes_test(is_owner)
def update_member_role(request, id):


    if request.method == "POST":


        member = get_object_or_404(
            User,
            id=id
        )



        new_role = request.POST.get(
            "new_role"
        )



        if new_role in [
            "member",
            "writer"
        ]:


            member.profile.role = new_role

            member.profile.save()



            messages.success(
                request,
                "نقش کاربر با موفقیت تغییر کرد"
            )



    return redirect(
        "accounts:member_profile",
        id=id
    )









@login_required
@user_passes_test(is_owner)
def delete_member(request, id):


    if request.method == "POST":


        member = get_object_or_404(
            User,
            id=id
        )



        if member == request.user:


            messages.error(
                request,
                "نمی‌توانید حساب خودتان را حذف کنید"
            )



            return redirect(
                "accounts:members"
            )




        member.delete()



        messages.success(
            request,
            "کاربر حذف شد"
        )




    return redirect(
        "accounts:members"
    )









def register_view(request):


    if request.method == "POST":


        form = RegisterForm(
            request.POST
        )



        if form.is_valid():


            user = form.save()



            login(
                request,
                user
            )



            messages.success(
                request,
                "حساب کاربری با موفقیت ایجاد شد"
            )



            return redirect(
                "blog:home"
            )



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
        }
    )









@login_required
def edit_profile(request):


    if request.method == "POST":


        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )



        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )



        if user_form.is_valid() and profile_form.is_valid():


            user_form.save()

            profile_form.save()



            messages.success(
                request,
                "پروفایل بروزرسانی شد"
            )



            return redirect(
                "accounts:profile"
            )



    else:


        user_form = UserUpdateForm(
            instance=request.user
        )


        profile_form = ProfileUpdateForm(
            instance=request.user.profile
        )




    return render(
        request,
        "accounts/edit_profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form
        }
    )