from .models import Category, Option, Poll, Like

from django.contrib import admin

# Register your models here.
admin.site.register(Category)
admin.site.register(Option)
admin.site.register(Poll)
admin.site.register(Like)