
from django import forms
from .models import Post, Comment
from django_ckeditor_5.widgets import CKEditor5Widget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "image",
            "content",
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

        labels = {
            "body": "Body",
        }

        widgets = {
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Share your thoughts...",
                    "rows": 3,
                    "maxlength": 1000,
                    "class": (
                        "w-full border border-gray-300 "
                        "rounded-lg p-3 focus:outline-none "
                        "focus:ring-2 focus:ring-indigo-500"
                    ),
                }
            ),
        }
