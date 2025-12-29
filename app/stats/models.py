from polls.models import Option
from users.models import User

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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="votes")
    characteristics_snapshot = models.JSONField()

    def __str__(self):
        return f"Vote {self.id} for {self.option}"