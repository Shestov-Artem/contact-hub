from django.shortcuts import render, redirect
from .forms import CustomLoginForm, RegisterForm, ContactForm

from .database import create_user, find_user_by_credentials

# Регистрация пользователя
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Создаем пользователя в базе данных
            user_id = create_user(username, password)
            
            if user_id:
                print(f"Успешная регистрация пользователя {username} с ID {user_id}")
                return redirect('contact_list')
            else:
                form.add_error(None, "Ошибка при создании пользователя")
        else:
            print("Форма не валидна:", form.errors)
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

# Авторизация пользователя
def login_view(request):
    error_message = None
    
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Проверяем учетные данные в БД
            user_id = find_user_by_credentials(username, password)
            
            if user_id:
                return redirect('contact_list')
            else:
                error_message = "Неверный логин или пароль"
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {
        'form': form,
        'error_message': error_message
    })

# Выход из системы
def logout_view(request):
    # В реальном приложении здесь будет выход из системы
    # auth_logout(request)  # Раскомментируйте, когда добавите аутентификацию Django
    return redirect('login')  # Перенаправляем на страницу регистрации

# ------------------------------------------------------------------------------------------------------------------------

# Временное хранилище контактов (позже заменится на БД)
CONTACTS = [
    {"id": 1, "name": "Иван", "phone": "+79123456789"},
    {"id": 2, "name": "Мария", "phone": "+79876543210"},
]

# Главная страница со списком контактов
def contact_list(request):
    # Просто передаём все контакты в шаблон
    return render(request, 'contacts/contact_list.html', {
        'contacts': CONTACTS
    })

# view для создания контакта
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            new_contact = {
                'id': len(CONTACTS) + 1,
                'name': form.cleaned_data['name'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data.get('email', ''),
                'notes': form.cleaned_data.get('notes', ''),
            }
            CONTACTS.append(new_contact)
            return redirect('contact_list')
    return redirect('contact_list')  # Для GET-запросов просто редирект

# view для удаления контакта
def contact_delete(request, pk):
    if request.method == 'POST':
        global CONTACTS
        CONTACTS = [c for c in CONTACTS if c['id'] != pk]
    return redirect('contact_list')


def contact_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Фильтрация контактов по имени (регистронезависимо)
        filtered_contacts = [
            c for c in CONTACTS 
            if search_query.lower() in c['name'].lower()
        ]
    else:
        filtered_contacts = CONTACTS
    
    return render(request, 'contacts/contact_list.html', {
        'contacts': filtered_contacts,
        'search_query': search_query
    })


