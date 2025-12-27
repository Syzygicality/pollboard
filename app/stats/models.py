from polls.models import Option

from django.db import models
from django_countries.fields import CountryField

import shortuuid
# Create your models here.
class Vote(models.Model):
    """
    NOTE: Update fields to match Characteristics model in users app
    """
    id = models.CharField(primary_key=True, default=shortuuid.uuid, editable=False)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="votes")
    country = CountryField(blank=True, null=True)
    gender = models.CharField(max_length=32, default="Prefer not to say", blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Vote {self.id} for {self.option}"