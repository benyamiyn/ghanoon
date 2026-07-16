from django import forms 
from .models import Comment

class CommentForm(forms.ModelForm):
    
    parent_id = forms.IntegerField(required = False, widget = forms.HiddenInput)
    
    class Meta:
        model = Comment 
        fields = ["text","parent_id"]
        widgets = {
            "text": forms.Textarea(
                attrs ={
                    "rows" : 4,
                    "placeholder": "نظر خود را بنویسید",
                }
            ),

        }