from django.contrib import admin
from .models import User, Poll, Draft, Option, Like, Vote
# Register your models here.
admin.site.register(User)
admin.site.register(Poll)
admin.site.register(Draft)
admin.site.register(Option)
admin.site.register(Like)
admin.site.register(Vote)