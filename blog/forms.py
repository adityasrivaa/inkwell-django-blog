from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "category", "image", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Enter an engaging title",
                "class": "form-input",
                "content": CKEditor5Widget(config_name="extends"),
            }),
            "content": forms.Textarea(attrs={
                "rows": 10,
                "placeholder": "Write your article here...",
                "class": "form-input",
            }),
            "image": forms.ClearableFileInput(attrs={
                "accept": "image/*",
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        label = {"body": "Your Comment"}
        widgets = {
            "body": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Share your thoughts...",
                "class": "form-input",
            }),
        }