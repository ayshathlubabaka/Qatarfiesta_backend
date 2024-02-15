from django.urls import path
from .views import *

urlpatterns = [
    path("create-checkout-session/", StripeCheckoutView.as_view()),
    path("create-booking/", CreateBookingView.as_view()),
    path("confirm-booking/", BookingConfirmView.as_view()),
    path("my-booking/", ViewBooking.as_view()),
    path("cancel-booking/<int:booking_id>/", CancelBookingAPI.as_view()),
    path("wallet/", walletViewAPI.as_view()),
    path("debit-wallet/", payWithWallet.as_view()),
    path("credit-wallet/", CreditToWalletAPI.as_view()),
    path("transaction/", TransactionViewAPI.as_view()),
]
