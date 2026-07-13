from django import forms

SORT_CHOICES = [
    ("newest","جدیدترین"),
    ("oldest","قدیمی ترین"),
    ("title","عنوان"),
]
class SearchForm(forms.Form):
    q = forms.CharField(
        max_length = 100,
        required = False ,
        widget = forms.TextInput(
            attrs= {
                "placeholder": "جست و جو",
            }
        )
    )
    sort = forms.ChoiceField(
        choices = SORT_CHOICES,
        required=False
    )
    #مرتب سازی نتایج  جست و جو 
    #کلمه جست و جو شده باید اعتبار سنجی شود
    #پر کردن فیلد جست و جو اجباری نیست عبارت جست و جو شده باید کمتر از 100 کاراکتر باشد 