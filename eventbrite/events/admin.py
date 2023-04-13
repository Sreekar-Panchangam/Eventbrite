from django.contrib import admin
from . import models

# Register your models here.
class EventLikesInline(admin.TabularInline):
    model = models.EventLikes

admin.site.register(models.Event)
