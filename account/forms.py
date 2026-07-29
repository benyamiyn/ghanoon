from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profile

#فرم ثبت نام کاربران
class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
         model = User
         fields = [
             "username",
             "first_name",
             "last_name",
             "email",
             "password1",
             "password2",
         ]

#فرم تغییرات اکانت  ها
class UserUpdateForm(forms.ModelForm):

    class Meta :

        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

#فرم تغییر پروفایل
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "prof_image",
            "bio",
            "birth_date",

        ]