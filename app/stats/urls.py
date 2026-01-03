from .views import VoteView

from django.urls import path

urlpatterns = [
    path("vote/<str:poll_id>/<str:option_id>", VoteView.as_view(), name="vote")
]
