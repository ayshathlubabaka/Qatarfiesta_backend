from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TicketType(models.Model):
    name = models.CharField(max_length=25)
    is_available = models.BooleanField(default=True)


class AgeGroup(models.Model):
    name = models.CharField(max_length=25)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    is_available = models.BooleanField(default=True)
