from rest_framework import serializers
from .models import User, Poll, Option, Draft

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["choice", "votes"]

class PollSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    user_id = UserSerializer()

    class Meta:
        model = Poll
        fields = ["user_id", "title", "description", "options", "likes"]
    
    def get_options(self, obj):
        options = Option.objects.filter(id__in=obj.options)
        return OptionSerializer(options, many=True).data
    
class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ["title", "description", "options"]