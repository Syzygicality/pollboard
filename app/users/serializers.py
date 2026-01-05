from .models import User, Characteristics

from rest_framework.serializers import ModelSerializer
from django_countries.serializer_fields import CountryField


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['id']

class CharacteristicsSerializer(ModelSerializer):
    country = CountryField(allow_null=True, required=False)
    
    class Meta:
        model = Characteristics
        fields = ['country', 'gender', 'age']
