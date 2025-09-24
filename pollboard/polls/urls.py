from django.urls import path
from .views import PollListView, PollSingleView

urlpatterns = [
    path("polls/", PollListView.as_view(), name="poll-list"),
    path("polls/<uuid:poll_id>", PollSingleView.as_view(), name="poll-single")
]