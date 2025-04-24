from django.shortcuts import render, redirect
from .forms import CustomLoginForm, RegisterForm, ContactForm
from .database import create_user, find_user_by_credentials, get_db_connection

# Регистрация пользователя
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
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
            
            user_id = find_user_by_credentials(username, password)
            
            if user_id:
                # Здесь нужно добавить логику входа (сессии, куки и т.д.)
                # Пока просто сохраняем user_id в сессии
                request.session['user_id'] = user_id
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
    # Удаляем user_id из сессии
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')

# Функции для работы с контактами
def get_contacts(user_id, search_query=''):
    """Получает контакты пользователя из БД"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            if search_query:
                cursor.execute("""
                    SELECT id, name, phone_number as phone, email, description as notes 
                    FROM contacts 
                    WHERE user_id = %s AND LOWER(name) LIKE LOWER(%s)
                    ORDER BY name
                """, (user_id, f'%{search_query}%'))
            else:
                cursor.execute("""
                    SELECT id, name, phone_number as phone, email, description as notes 
                    FROM contacts 
                    WHERE user_id = %s
                    ORDER BY name
                """, (user_id,))
            
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Ошибка при получении контактов: {e}")
        return []
    finally:
        if conn:
            conn.close()

def contact_list(request):
    """Список контактов с поиском"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    search_query = request.GET.get('search', '')
    contacts = get_contacts(request.session['user_id'], search_query)
    
    return render(request, 'contacts/contact_list.html', {
        'contacts': contacts,
        'search_query': search_query
    })

def contact_create(request):
    """Создание нового контакта"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            conn = None
            try:
                conn = get_db_connection()
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO contacts 
                        (user_id, name, phone_number, email, description)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        request.session['user_id'],
                        form.cleaned_data['name'],
                        form.cleaned_data['phone'],
                        form.cleaned_data.get('email', ''),
                        form.cleaned_data.get('notes', '')
                    ))
                    conn.commit()
            except Exception as e:
                print(f"Ошибка при создании контакта: {e}")
            finally:
                if conn:
                    conn.close()
            
            return redirect('contact_list')
    
    return redirect('contact_list')

def contact_delete(request, pk):
    """Удаление контакта"""
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM contacts 
                    WHERE id = %s AND user_id = %s
                """, (pk, request.session['user_id']))
                conn.commit()
        except Exception as e:
            print(f"Ошибка при удалении контакта: {e}")
        finally:
            if conn:
                conn.close()
    
    return redirect('contact_list')