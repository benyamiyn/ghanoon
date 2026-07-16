from django import forms


SORT_CHOICES = [
    ("newest", "جدیدترین"),
    ("oldest", "قدیمی ترین"),
    ("title", "عنوان"),
]


class SearchForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "جست و جو",
            }
        ),
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
    )
