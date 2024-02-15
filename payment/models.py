from django.db import models
from organizer.models import Events
from accounts.models import User

# Create your models here.


class EventBooking(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=True)
    numTickets = models.PositiveIntegerField(default=0)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    visitor_names = models.JSONField(null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_active": True}
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("complete", "Complete"),
        ("cancelled", "Cancelled"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    is_paid = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now=True)
    stripe_session_id = models.CharField(max_length=100, blank=True, null=True)
    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
    )

    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    is_active = models.BooleanField(default=False)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.name}'s Wallet"


class Transaction(models.Model):

    TRANSACTION_TYPES = [("credit", "Credit"), ("debit", "Debit")]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    event_booking = models.ForeignKey(
        EventBooking, on_delete=models.SET_NULL, null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.transaction_type == "credit":
            self.wallet.balance += self.amount
        elif self.transaction_type == "debit":
            self.wallet.balance -= self.amount

        self.wallet.save()

    def __str__(self):
        return f"Transaction - {self.transaction_type}: {self.amount}"
