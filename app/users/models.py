from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_countries.fields import CountryField
from datetime import timedelta
import shortuuid

User = get_user_model()

class Characteristics(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="characteristics")
    country = CountryField(blank=True, null=True)
    gender = models.CharField(max_length=32, default="Prefer not to say", blank=True, null=True)
    age = models.CharField(blank=True, null=True)
    last_updated = models.DateTimeField(default=timezone.now())

    @property
    def updatable(self):
        return timezone.now() >= self.last_updated + timedelta(days=14)

    def __str__(self):
        return f"Characteristics for {self.user}"
