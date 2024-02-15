from django.contrib import admin
from .models import EventBooking, Wallet, Transaction

# Register your models here.
admin.site.register(EventBooking)
admin.site.register(Wallet)
admin.site.register(Transaction)