from django.shortcuts import render
from rest_framework import generics, status, permissions
from .serializers import PollSerializer, DraftSerializer, UserSerializer, OptionSerializer
from .models import Poll, Draft, User, Option
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound, ValidationError
from django.db import transaction

# Create your views here.

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.user_id == request.user

class PollListView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollSingleView(generics.RetrieveDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    lookup_field = "poll_id"

    def destroy(self, request, *args, **kwargs):
        poll = self.get_object()
        user = self.request.user
        if not (user.is_superuser or poll.user_id == user):
            raise PermissionDenied("You do not have permission to delete this poll.")
        poll.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PollCreateView(generics.CreateAPIView):
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        draft_id = kwargs.get("draft_id")
        try:
            draft = Draft.objects.get(draft_id=draft_id)
        except Draft.DoesNotExist:
            raise NotFound("Draft not found.")
        if draft.user_id != self.request.user:
            raise PermissionDenied("You do not have permission to publish this draft.")
        elif len(draft.options) < 2:
            raise ValidationError("Polls must have a minimum of two options.")
        elif not draft.title:
            raise ValidationError("Polls are required to have a title.")

        with transaction.atomic():
            poll = Poll.objects.create(
                user_id=draft.user_id,
                title=draft.title,
                description=draft.description,
                likes=0,
                options=[]
            )
            option_ids = []
            for choice in draft.options:
                option = Option.objects.create(
                    poll_id=poll,
                    choice=choice,
                    votes=0
                )
                option_ids.append(option.option_id)
            poll.options = option_ids
            poll.save()
            draft.delete()

        serializer = self.get_serializer(poll)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DraftListView(generics.ListCreateAPIView):
    serializer_class = DraftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Draft.objects.all()
        return Draft.objects.filter(user_id=user)

    def create(self, request, *args, **kwargs):
        draft = Draft.objects.create(user_id=self.request.user)
        serializer = self.get_serializer(draft)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DraftSingleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DraftSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = "draft_id"
    queryset = Draft.objects.all()

