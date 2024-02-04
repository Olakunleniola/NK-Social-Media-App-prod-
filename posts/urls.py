from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("", views.HopePage.as_view(), name="index"),
    path("following/", views.FollowingView.as_view(), name="following"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="detail"),
    path("new/", views.CreateNewPost.as_view(), name="new_post"),
]