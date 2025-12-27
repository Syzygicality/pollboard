from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
import shortuuid

User = get_user_model()

class Characteristics(models.Model):
    """
    Stores demographic traits for a user. 
    Age is stored as a bucket to reduce re-identification risk.
    """
    id = models.CharField(primary_key=True, default=shortuuid.uuid, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="characteristics")
    country = CountryField(blank=True, null=True)
    gender = models.CharField(max_length=32, default="Prefer not to say", blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Characteristics for {self.user}"
