from .models import Category, Poll, Option
from users.serializers import UserSerializer

from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
        read_only_fields = ["name"]

class OptionSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    
    class Meta:
        model = Option
        fields = ["id", "label", "votes"]
        read_only_fields = ["id", "label", "votes"]
    
    def get_votes(self, obj):
        return obj.votes.count()

class PollCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=300)
    category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    options = serializers.ListField(child=serializers.CharField(max_length=64), min_length=2, max_length=10)
    vote_period = serializers.IntegerField()

    def validate_options(self, value):
        if len(set(value)) != len(value):
            raise serializers.ValidationError("Options must be unique.")
        return value

class PollSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    options = serializers.SerializerMethodField()
    voted = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    time_left = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ["id", "title", "user", "category", "description", "options", "votable", "likes", "liked", "creation_date", "time_left"]
        read_only_fields = ["id", "title", "user", "options", "votable", "likes", "liked", "creation_date", "time_left"]

    def get_options(self, obj):
        return OptionSerializer(obj.options.all(), many=True).data
    
    def get_voted(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.options.filter(votes__user=request.user).exists()

    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_liked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(user=request.user).exists()
    
    def get_time_left(self, obj):
        return max(obj.closing_date - timezone.now(), timedelta(0))