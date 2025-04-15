from django.urls import path

# Авторизация/регистрация
from contact_hub_app.views import login_view, index, register_view
# Редактирование карточек
from contact_hub_app.views import contact_list, contact_detail, contact_create, contact_delete

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),

    #path('', index, name='home'),
    #path('login/', login_view, name='login'),
    #path('register/', register_view, name='register'),

    path("", contact_list, name="contact_list"),
    path("create/", contact_create, name="contact_create"),
    path("<int:pk>/", contact_detail, name="contact_detail"),
    path("<int:pk>/delete/", contact_delete, name="contact_delete"),
]