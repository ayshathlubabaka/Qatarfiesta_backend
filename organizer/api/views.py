import datetime
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from ..models import *
from payment.models import EventBooking
from payment.serializer import MyBookingSerializer

from myadmin.signals import event_request_submitted

class EventAPI(APIView):

    def get(self, request):
        events = Events.objects.all().order_by('-id')
        serializer = EventSerializer(events, many=True)
        data=serializer.data
        for event_data in data:
            event_id = event_data['id']
            try:
                event = Events.objects.get(id=event_id)
                image = event.image
                event_data['image'] = request.build_absolute_uri('/')[:-1] + image.url
            except Events.DoesNotExist:
                event_data['image'] = '' 
        return Response(serializer.data)
    
    
    def post(self, request):

        try:
            serializer = AddEventSerializer(data=request.data)

            if serializer.is_valid():
                event = serializer.save()
                if 'image' in request.FILES:
                    event.image=request.FILES['image']
                    event.save()
                event_request_submitted.send(sender=self.__class__, event_request=event)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class OrganizerEventsAPI(APIView):
    def get(self, request):
        organizer = request.user
        organizer_id = organizer.id
        events = Events.objects.filter(organizer=organizer_id).order_by('-id')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
        
class ChangeEventAPI(APIView):
    def put(self, request, event_id):
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, event_id):
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ActiveEvents(APIView):
    def get(self, request):
        today = date.today()
        events = Events.objects.filter(is_active=True, endDate__gte=today).order_by('-id')
        serializer = EventSerializer(events, many=True)
        data=serializer.data
        for event_data in data:
            event_id = event_data['id']
            try:
                event = Events.objects.get(id=event_id)
                image = event.image
                event_data['image'] = request.build_absolute_uri('/')[:-1] + image.url
            except Events.DoesNotExist:
                event_data['image'] = '' 
        return Response(serializer.data)
    
class DateFilterAPI(APIView):
    def get(self, request, *args, **kwargs):
        date_param = self.request.query_params.get('date', None)

        if date_param is None:
            return Response({'error': 'Date parameter is required.'}, status=400)

        try:
            date = datetime.datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        events = Events.objects.filter(startDate__lte=date, endDate__gte=date)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    

class GetBookingAPI(APIView):
    def get(self, request):
        events = Events.objects.filter(organizer=request.user)
        bookings = EventBooking.objects.filter(event__in=events).order_by('-id')
        serializer = MyBookingSerializer(bookings, many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ManageBookingAPI(APIView):
    
    def put(self, request, booking_id):
        try:
            booking = EventBooking.objects.get(id=booking_id)
        except EventBooking.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        booking.is_active = False
        booking.save()

        return Response(status=status.HTTP_200_OK)
    

        
