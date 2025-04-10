from django.urls import path
from contact_hub_app.views import login_view, index, register_view

urlpatterns = [
    path('', index, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]