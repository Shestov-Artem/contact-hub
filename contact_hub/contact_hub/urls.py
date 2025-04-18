from django.urls import path
from contact_hub_app.views import login_view, register_view, contact_list, contact_create, contact_delete, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path("", contact_list, name="contact_list"),
    path("create/", contact_create, name="contact_create"),
    path("<int:pk>/delete/", contact_delete, name="contact_delete"),
]