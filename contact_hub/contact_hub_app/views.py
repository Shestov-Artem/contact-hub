from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomLoginForm

def index(request):
    return HttpResponse("Главная страница")

def register_view(request):
    return HttpResponse("Страница регистрации (здесь будет форма позже)")

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)  # Убрали параметр `data=`
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Просто выводим данные в консоль для теста
            print(f"Получены данные: Логин - {username}, Пароль - {password}")
            
            # Перенаправляем на главную страницу
            return redirect('home')  # Или другую страницу
            
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {'form': form})