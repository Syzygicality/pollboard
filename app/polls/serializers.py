from .models import Category, Poll, Option
from users.serializers import UserSerializer

from rest_framework.serializers import ModelSerializer, SerializerMethodField

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
        read_only_fields = ["name"]

class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "label", "votes"]
        read_only_fields = ["id", "label", "votes"]

class PollSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    options = SerializerMethodField()
    likes = SerializerMethodField()
    liked = SerializerMethodField()

    class Meta:
        model = Poll
        fields = ["id", "title", "user", "category", "description", "options", "likes", "liked", "creation_date"]
        read_only_fields = ["id", "title", "user", "options", "likes", "liked", "creation_date"]

    def get_options(self, obj):
        return OptionSerializer(obj.options.all(), many=True).data
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_liked(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        return obj.likes.filter(user=request.user).exists()