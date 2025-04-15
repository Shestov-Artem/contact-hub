from django.urls import path
from contact_hub_app.views import login_view, register_view, contact_list, contact_create, contact_delete

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path("", contact_list, name="contact_list"),
    path("create/", contact_create, name="contact_create"),  # Оставляем только для POST-запросов
    path("<int:pk>/delete/", contact_delete, name="contact_delete"),  # Только для POST
    # Удаляем маршрут для contact_detail
]