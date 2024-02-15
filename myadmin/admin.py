from django.contrib import admin
from .models import Category, TicketType, AgeGroup

# Register your models here.

admin.site.register(Category)
admin.site.register(TicketType)
admin.site.register(AgeGroup)
