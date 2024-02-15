from rest_framework import serializers
from myadmin.models import Category, TicketType, AgeGroup


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "is_active"]


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]

    def create(self, validated_data):

        category = Category.objects.create(name=validated_data["name"])

        return category


class TicketTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketType
        fields = "__all__"


class CreateTicketTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketType
        fields = ["name"]

    def create(self, validated_data):

        ticketType = TicketType.objects.create(name=validated_data["name"])
        return ticketType


class AgeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgeGroup
        fields = "__all__"


class CreateAgeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgeGroup
        fields = ["name", "min_age", "max_age"]

    def create(self, validated_data):
        ageGroup = AgeGroup.objects.create(
            name=validated_data["name"],
            min_age=validated_data["min_age"],
            max_age=validated_data["max_age"],
        )
        return ageGroup
