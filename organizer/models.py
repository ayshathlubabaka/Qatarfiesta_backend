from django.db import models
from accounts.models import User
from myadmin.models import Category, TicketType, AgeGroup


class Events(models.Model):
    title = models.CharField(max_length=25, unique=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=50, decimal_places=40, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=50, decimal_places=40, null=True, blank=True
    )
    startDate = models.DateField()
    endDate = models.DateField(default=None, null=True)
    startTime = models.TimeField()
    endTime = models.TimeField(default=None, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="event_images/", null=True, blank=True)
    description = models.CharField(max_length=255)
    ticketPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ticketQuantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title
