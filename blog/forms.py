
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "category", "image", "content"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": (
                    "w-full rounded-xl border border-slate-300 "
                    "bg-white px-4 py-3 text-slate-900 "
                    "outline-none transition "
                    "focus:border-indigo-500 focus:ring-4 "
                    "focus:ring-indigo-100"
                ),
                "placeholder": "Enter an engaging blog title",
            }),
            "category": forms.Select(attrs={
                "class": (
                    "w-full rounded-xl border border-slate-300 "
                    "bg-white px-4 py-3 text-slate-900 "
                    "outline-none focus:border-indigo-500 "
                    "focus:ring-4 focus:ring-indigo-100"
                ),
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": (
                    "block w-full rounded-xl border "
                    "border-slate-300 bg-slate-50 p-3 "
                    "text-sm text-slate-700"
                ),
                "accept": "image/*",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Share your thoughts...",
                "class": (
                    "w-full rounded-xl border border-slate-300 "
                    "px-4 py-3 focus:border-indigo-500 "
                    "focus:ring-4 focus:ring-indigo-100"
                ),
            }),
        }
