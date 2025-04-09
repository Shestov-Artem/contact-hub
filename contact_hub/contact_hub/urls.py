from django.urls import path
from contact_hub_app import views

urlpatterns = [
    path('', views.index, name='home'),
]
