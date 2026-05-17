from django.urls import path

from .views import waiting_list_signup

urlpatterns = [
    path('', waiting_list_signup, name='waiting_list_signup'),
]
