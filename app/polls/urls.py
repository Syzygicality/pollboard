from .views import (  
    CategoryView, 
    PollSingleView, 
    PollUpdateDeleteView, 
    PollListView, 
    PollCreateView, 
    PollLikedView, 
    PollVotedView,
    LikeView, 
    UnlikeView,
)

from django.urls import path

urlpatterns = [
    path("categories", CategoryView.as_view(), name="categories"),
    path("polls", PollListView.as_view(), name="poll-list"),
    path("polls/liked", PollLikedView.as_view(), name="poll-liked"),
    path("polls/voted", PollVotedView.as_view(), name="poll-voted"),
    path("polls/create", PollCreateView.as_view(), name="poll-create"),
    path("polls/<str:pk>", PollSingleView.as_view(), name="poll-single"),
    path("polls/<str:pk>/edit", PollUpdateDeleteView.as_view(), name="poll-edit"),
    path("polls/<str:pk>/like", LikeView.as_view(), name="poll-like"),
    path("polls/<str:pk>/unlike", UnlikeView.as_view(), name="poll-unlike"),
]