from django.shortcuts import render, redirect
from .forms import CustomLoginForm, RegisterForm, ContactForm

# Регистрация пользователя
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # В реальном приложении здесь будет создание пользователя
            username = form.cleaned_data['username']
            print(f"Регистрация нового пользователя: {username}")
            return redirect('contact_list')
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
            
            # Кастомная проверка (замените на реальную проверку в БД позже)
            if username != "1" and password != "1":
                return redirect('contact_list')
            else:
                error_message = "Неверный логин или пароль"
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {
        'form': form,
        'error_message': error_message  # Передаём сообщение об ошибке
    })


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

# # Просмотр деталей контакта
# def contact_detail(request, pk):
#     # Находим контакт по id (pk — это число из URL)
#     contact = next((c for c in CONTACTS if c['id'] == pk), None)
    
#     if not contact:
#         return redirect('contact_list')  # Если контакт не найден
    
#     return render(request, 'contacts/contact_detail.html', {
#         'contact': contact
#     })

# Упрощаем view для создания контакта
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

# Упрощаем view для удаления контакта
def contact_delete(request, pk):
    if request.method == 'POST':
        global CONTACTS
        CONTACTS = [c for c in CONTACTS if c['id'] != pk]
    return redirect('contact_list')
