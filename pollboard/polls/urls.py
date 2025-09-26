from django.urls import path
from .views import PollListView, PollSingleView, PollCreateView, DraftListView, DraftSingleView, PollLikeView, VoteView

urlpatterns = [
    path("polls/", PollListView.as_view(), name="poll-list"),
    path("polls/<uuid:poll_id>", PollSingleView.as_view(), name="poll-single"),
    path("polls/post/<uuid:draft_id>", PollCreateView.as_view(), name="poll-create"),
    path("drafts/", DraftListView.as_view(), name="draft-list"),
    path("drafts/<uuid:draft_id>", DraftSingleView.as_view(), name="draft-single"),
    path("polls/like/<uuid:poll_id>", PollLikeView.as_view(), name="poll-like"),
    path("polls/vote/<uuid:option_id>", VoteView.as_view(), name="poll-vote"),
]