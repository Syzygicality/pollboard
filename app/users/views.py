from .models import User, Characteristics
from .serializers import UserSerializer, CharacteristicsSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError

# Create your views here.
class CharacteristicsCreateView(generics.CreateAPIView):
    serializer_class = CharacteristicsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if hasattr(user, "characteristics"):
            raise ValidationError("Characteristics already exist for this user.")
        serializer.save(user=user)

class CharacteristicsSingleView(generics.RetrieveUpdateAPIView):
    serializer_class = CharacteristicsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not hasattr(user, "characteristics"):
            raise ValidationError("No characteristics found for this user.")
        return user.characteristics

