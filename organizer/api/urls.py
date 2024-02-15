from django.urls import path
from .views import  *

urlpatterns = [
    path('event/', EventAPI.as_view()),
    path('organizer-event/', OrganizerEventsAPI.as_view()),
    path('active-event/', ActiveEvents.as_view()),
    path('event-change/<int:event_id>/', ChangeEventAPI.as_view()),
    path('date-filter/', DateFilterAPI.as_view()),
    path('booking/', GetBookingAPI.as_view()),
    path('cancel-booking/<int:booking_id>/', ManageBookingAPI.as_view()),
]