from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

# Vista para el registro de usuarios
def register(request):
    # Inicializa el formulario de registro
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Obtiene los datos del formulario
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            # Crea un nuevo usuario con los datos del formulario
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password )
            user.phone_number = phone_number
            user.save()
            # Redirige al usuario a la pagina de inicio de sesion
            return redirect('/accounts/login/')


    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)


#Vista que permite el login de usuarios
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Autentica al usuario
        user = auth.authenticate(email=email, password=password)
        print(email, password)
        if user is not None:    
            # Si la autenticación es exitosa, inicia sesión y redirige al dashboard
            auth.login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect('dashboard')
        else:
            # Si la autenticación falla, muestra un mensaje de error y redirige al inicio de sesión
            messages.error(request, 'The credentials are incorrect')
            return redirect('login')


    return render(request, 'accounts/login.html')

#Vista para cerrar sesion
@login_required(login_url='login')
def logout(request):
    # Cierra la sesión del usuario y redirige al inicio de sesión
    auth.logout(request)
    messages.success(request, 'You have logged out')
    return redirect('login')

