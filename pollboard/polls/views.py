from django.shortcuts import render
from rest_framework import generics
from .serializers import PollSerializer, DraftSerializer, UserSerializer, OptionSerializer
from .models import Poll, Draft, User, Option

# Create your views here.

class PollListView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollSingleView(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_field = "poll_id"

    def destroy(self, request, *args, **kwargs):
        poll = self.get_object()
        user = request.user
        if not (user.is_superuser or poll.user_id == user):
            raise PermissionDenied("You do not have permission to delete this poll.")
        Option.objects.filter(poll_id=poll).delete()
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)