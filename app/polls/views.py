from .models import Poll, Option, Category, Like
from .serializers import OptionSerializer, PollSerializer, CategorySerializer, PollCreateSerializer, LikeSerializer
from .permissions import IsAuthor

from rest_framework import generics, mixins
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
# Create your views here.

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        categories = list(self.get_queryset().order_by("name").values_list("name", flat=True))
        return Response({"categories": categories})

class PollListView(generics.ListAPIView):
    serializer_class = PollSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["category"]
    ordering = ["-creation_date"]
    ordering_fields = ["creation_date"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Poll.objects.annotate(
            like_count=Count("likes")
        )

class PollSingleView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollCreateView(generics.CreateAPIView):
    serializer_class = PollCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        poll = Poll.objects.create(
            user=self.request.user,
            title=serializer.validated_data["title"],
            category=serializer.validated_data["category"],
            description=serializer.validated_data.get("description", ""),
            vote_period=serializer.validated_data["vote_period"]
        )
        Option.objects.bulk_create([
            Option(poll=poll, label=label.strip(), order=i) for i, label in enumerate(serializer.validated_data["options"])
        ])

class PollUpdateDeleteView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PollLikedView(generics.ListAPIView):
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Poll.objects.filter(likes__user=user)

class PollVotedView(generics.ListAPIView):
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Poll.objects.filter(options__votes__user=user).distinct()
        

class LikeView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer=None):
        user = self.request.user
        poll_id = self.kwargs["pk"]
        poll = get_object_or_404(Poll, pk=poll_id)
        existing_like = Like.objects.filter(poll=poll, user=user).first()
        if not existing_like:
            Like.objects.create(poll=poll, user=user)
        

class UnlikeView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_object(self):
        user = self.request.user
        poll_id = self.kwargs["pk"]
        poll = get_object_or_404(Poll, pk=poll_id)
        return get_object_or_404(Like, poll=poll, user=user)
