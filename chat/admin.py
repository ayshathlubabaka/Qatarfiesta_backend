from django.contrib import admin
from .models import VisitorOrganizerChat, PendingChat

# Register your models here.
admin.site.register(VisitorOrganizerChat)
admin.site.register(PendingChat)
