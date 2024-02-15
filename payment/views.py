import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import EventBooking, Wallet, Transaction
from organizer.models import Events
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .serializer import (
    EventBookingSerializer,
    walletViewSerializer,
    MyTransactionSerializer,
)
from organizer.models import Events

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateBookingView(APIView):
    def post(self, request):
        try:
            serializer = EventBookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(csrf_exempt, name="dispatch")
class StripeCheckoutView(APIView):
    def post(self, request):
        booking_id = request.data["booking_id"]
        try:
            booking = EventBooking.objects.get(id=booking_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "qar",
                            "product_data": {
                                "name": booking.event,
                            },
                            "unit_amount": int(booking.totalPrice * 100),
                        },
                        "quantity": 1,
                    }
                ],
                payment_method_types=["card"],
                mode="payment",
                success_url=settings.SITE_URL
                + f"/order-status/?success=true&bookingId={booking.id}",
                cancel_url=settings.SITE_URL + "/order-status/?canceled=true",
            )
            booking.stripe_session_id = checkout_session.id
            booking.save()

            return JsonResponse(
                {
                    "session_id": checkout_session.id,
                    "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
                    "session_url": checkout_session.url,
                }
            )

        except Exception as e:
            import traceback

            traceback.print_exc()
            return Response(
                {"error": "Something went wrong when creating stripe checkout session"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BookingConfirmView(APIView):
    def put(self, request):
        print(request.data)
        try:
            booking_id = request.data["booking_id"]
            booking = EventBooking.objects.get(id=booking_id)
            booking.is_paid = True
            booking.is_active = True
            booking.status = "complete"
            booking.payment_status = "completed"
            booking.save()

            event_title = booking.event
            event = Events.objects.get(title=event_title)
            event.ticketQuantity -= booking.numTickets
            event.save()

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": "Something went wrong when creating stripe checkout session"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ViewBooking(APIView):
    def get(self, request):
        booking = EventBooking.objects.filter(user=request.user).order_by("-id")
        serializer = EventBookingSerializer(booking, many=True)
        return Response(serializer.data)


class CancelBookingAPI(APIView):
    def put(self, request, booking_id):
        try:
            booking = EventBooking.objects.get(id=booking_id)
            booking.status = "cancelled"
            booking.save()
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": "Something went wrong when cancelling booking"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class walletViewAPI(APIView):
    def get(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
            serializer = walletViewSerializer(wallet)
            return Response(serializer.data)
        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user, balance=0.0)
            serializer = walletViewSerializer(wallet)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class payWithWallet(APIView):
    def post(self, request):
        try:
            user = request.user
            amount = request.data.get("amount", 0.00)
            bookingId = request.data.get("bookingId")
            booking = EventBooking.objects.get(id=bookingId)
            wallet = Wallet.objects.get(user=user)
            if wallet.balance < amount:
                return Response(
                    {"error": "Insufficient balance"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            transaction = Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type="debit",
                event_booking=booking,
            )
            booking.is_paid = True
            booking.is_active = True
            booking.status = "complete"
            booking.payment_status = "completed"
            booking.save()

            return Response(
                {"message": "Transaction successful", "transaction_id": transaction.id},
                status=status.HTTP_200_OK,
            )

        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found for the user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CreditToWalletAPI(APIView):
    def post(self, request):
        try:
            user = request.user
            bookingId = request.data.get("booking_id")
            booking = EventBooking.objects.get(id=bookingId)
            amount = booking.totalPrice
            wallet = Wallet.objects.get(user=user)
            transaction = Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type="credit",
                event_booking=booking,
            )
            return Response(
                {"message": "Transaction successful", "transaction_id": transaction.id},
                status=status.HTTP_200_OK,
            )

        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found for the user"},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TransactionViewAPI(APIView):
    def get(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
            transaction = Transaction.objects.filter(wallet=wallet.id).order_by("-id")
            serializer = MyTransactionSerializer(transaction, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
