from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

class Poll(models.Model):
    poll_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="polls")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4000, blank=True, null=True)
    options = ArrayField(base_field=models.UUIDField())
    likes = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class Option(models.Model):
    option_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.CharField(max_length=64)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice

class Draft(models.Model):
    draft_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="drafts")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=4000, blank=True, null=True)
    options = ArrayField(base_field=models.CharField(max_length=64))
    creation_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class Vote(models.Model):
    vote_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="votes")
    option_id = models.ForeignKey(Option, on_delete=models.CASCADE)
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)

class Like(models.Model):
    like_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="likes")
    poll_id = models.ForeignKey(Poll, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)