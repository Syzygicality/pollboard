from .models import User, Characteristics

from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

class CharacteristicsSerializer(ModelSerializer):
    class Meta:
        model = Characteristics
        fields = ['country', 'gender', 'age']
