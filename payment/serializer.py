from rest_framework import serializers
from .models import EventBooking, Wallet, Transaction


class EventBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventBooking
        fields = "__all__"

    def create(self, validated_data):

        booking = EventBooking.objects.create(
            numTickets=validated_data["numTickets"],
            totalPrice=validated_data["totalPrice"],
            user=validated_data["user"],
            event=validated_data["event"],
            date=validated_data["date"],
            visitor_names=validated_data["visitor_names"],
        )

        return booking


class EventBookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = ["status"]

    def validate(self, data):
        status = data.get("status")
        return data


class MyBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = "__all__"


class walletViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class MyTransactionSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "transaction_type",
            "timestamp",
            "wallet",
            "event_booking",
        ]
