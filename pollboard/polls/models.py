from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Poll(models.Model):
    poll_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4000, blank=True, null=True)
    options = ArrayField(base_field=models.UUIDField())
    likes = models.IntegerField()

class Option(models.Model):
    option_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.CharField(max_length=64)
    votes = models.IntegerField()

class Draft(models.Model):
    poll_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4000, blank=True, null=True)
    options = ArrayField(base_field=models.CharField(max_length=64))
