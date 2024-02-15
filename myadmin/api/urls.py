from django.urls import path
from .views import *


urlpatterns = [
    path("category/", CategoryAPI.as_view()),
    path("category-change/<int:category_id>/", CategoryChangeAPI.as_view()),
    path("events/", GetEventAPI.as_view()),
    path("approve-event-request/<int:event_request_id>/", ApproveEventAPI.as_view()),
    path("reject-event-request/<int:event_request_id>/", RejectEventAPI.as_view()),
    path("booking/", GetBookingAPI.as_view()),
    path("credit-wallet/<int:event_id>/", CreditWalletAPI.as_view()),
]
