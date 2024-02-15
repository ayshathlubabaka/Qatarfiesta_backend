from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from myadmin.models import Category
from organizer.models import Events
from payment.models import EventBooking
from payment.serializer import MyBookingSerializer
from payment.models import Wallet, Transaction
from organizer.api.serializers import EventSerializer


class CategoryAPI(APIView):

    def get(self, request):
        categories = Category.objects.all().order_by("-id")
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            data = request.data
            serializer = CategoryCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryChangeAPI(APIView):

    def put(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryCreateSerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetEventAPI(APIView):
    def get(self, request):
        events = Events.objects.all().order_by("-id")
        serializer = EventSerializer(events, many=True)
        data = serializer.data
        return Response(data)


class ApproveEventAPI(APIView):
    def put(self, request, event_request_id):
        try:
            event_request = Events.objects.get(id=event_request_id)
            event_request.is_active = True
            event_request.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RejectEventAPI(APIView):
    def put(self, request, event_request_id):
        try:
            event_request = Events.objects.get(id=event_request_id)
            event_request.is_active = False
            event_request.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetBookingAPI(APIView):
    def get(self, request):

        bookings = EventBooking.objects.all().order_by("-id")
        serializer = MyBookingSerializer(bookings, many=True)

        return Response(serializer.data)


class CreditWalletAPI(APIView):
    def post(self, request, event_id):
        bookings = EventBooking.objects.filter(event=event_id)
        for booking in bookings:
            user = booking.user
            amount = booking.totalPrice
            if booking.status == "complete" and booking.payment_status == "completed":
                wallet = Wallet.objects.get(user=user)
                transaction = Transaction.objects.create(
                    wallet=wallet,
                    amount=amount,
                    transaction_type="credit",
                    event_booking=booking,
                )
                booking.status = "cancelled"
                booking.payment_status = "pending"
                booking.save()
        return Response(
            {"message": "Transaction successful", "transaction_id": transaction.id},
            status=status.HTTP_200_OK,
        )
