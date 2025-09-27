from rest_framework import serializers
from .models import User, Poll, Option, Draft

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "username"]

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["option_id", "choice", "votes"]

class PollSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = ["user_id", "title", "description", "options", "likes"]
    
    def get_options(self, obj):
        option_ids = obj.options
        options_map = {o.option_id: o for o in Option.objects.filter(option_id__in=option_ids)}
        options = [options_map[option_id] for option_id in option_ids if option_id in options_map]
        return OptionSerializer(options, many=True).data
    
class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ["draft_id", "title", "description", "options"]