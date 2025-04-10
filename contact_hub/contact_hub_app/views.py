from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomLoginForm

def index(request):
    return HttpResponse("Главная страница")

def register_view(request):
    return HttpResponse("Страница регистрации (здесь будет форма позже)")

def login_view(request):
    error_message = None
    
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Кастомная проверка (замените на реальную проверку в БД позже)
            if username != "1" and password != "1":
                return redirect('home')
            else:
                error_message = "Неверный логин или пароль"
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {
        'form': form,
        'error_message': error_message  # Передаём сообщение об ошибке
    })