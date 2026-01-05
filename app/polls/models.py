from users.models import User

from django.db import models
from django.utils import timezone
import shortuuid
from datetime import timedelta


# Create your models here.
class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=32)

    def __str__(self):
        return self.name

class Poll(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="polls")
    title = models.CharField(max_length=300, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    vote_period = models.IntegerField(default=3)

    @property
    def closing_date(self):
        return self.creation_date + timedelta(days=self.vote_period)
    
    @property
    def votable(self):
        return timezone.now() < self.closing_date

    def __str__(self):
        return self.title

class Option(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    label = models.CharField(max_length=64)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.label}: {str(self.votes)}"

class Like(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("poll", "user")

    def __str__(self):
        return f"Poll '{self.poll}' liked by {self.user}."

