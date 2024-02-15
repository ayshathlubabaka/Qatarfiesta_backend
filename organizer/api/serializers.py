from rest_framework import serializers
from organizer.models import Events

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class AddEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

    def create(self, validated_data):

        event = Events.objects.create(
            title = validated_data['title'],
            venue = validated_data['venue'],
            address = validated_data['address'],
            latitude=float(validated_data['latitude']),
            longitude=float(validated_data['longitude']),
            startDate = validated_data['startDate'],
            endDate = validated_data['endDate'],
            startTime = validated_data['startTime'],
            endTime = validated_data['endTime'],
            category = validated_data['category'],
            description = validated_data['description'],
            organizer=validated_data['organizer'],
            ticketPrice=float(validated_data['ticketPrice']),
            ticketQuantity=int(validated_data['ticketQuantity']),
        )
     

        return event
    
