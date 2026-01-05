from .models import Vote
from .serializers import VoteSerializer
from polls.models import Poll, Option
from users.models import Characteristics
from users.serializers import CharacteristicsSerializer

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class VoteView(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer=None):
        user = self.request.user
        option_id = self.kwargs["option_id"]
        option = get_object_or_404(Option, pk=option_id)
        poll_id = self.kwargs["poll_id"]
        poll = get_object_or_404(Poll, pk=poll_id)
        if poll.votable and not Vote.objects.filter(user=user, option=option).first():
            characteristics = Characteristics.objects.get(user=user)
            json = CharacteristicsSerializer(characteristics).data if characteristics else {}
            Vote.objects.create(
                user=user,
                option=option,
                characteristics_snapshot=json
            )