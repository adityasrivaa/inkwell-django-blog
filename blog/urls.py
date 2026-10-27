from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("post/new/",views.post_create, name="post_create"),
    path("post/<slug:slug>/",views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/",views.post_edit, name="post_edit"),
    path("post/<slug:slug>/delete/",views.post_delete, name="post_delete"),

    path("post/<int:pk>/delete/",views.comment_delete, name="comment_delete"),
    path("accounts/register/", views.register, name="register"),
]
