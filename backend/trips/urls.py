from django.urls import path
from .views import plan_trip, health

urlpatterns = [
    path('plan', plan_trip, name='plan_trip'),
    path('health', health, name='health'),
]
