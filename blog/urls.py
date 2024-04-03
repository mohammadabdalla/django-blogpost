from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register-page"),
    path("user-login/", views.LoginView.as_view(), name="user-login-page"),
    path("logout/", views.LogoutView.as_view(), name="logout-page"),
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("posts/", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(),
         name="post-detail-page"),  # /posts/my-first-post
    path("read-later/", views.ReadLaterView.as_view(), name="read-later")
]
