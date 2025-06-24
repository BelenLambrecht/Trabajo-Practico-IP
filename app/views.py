# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.layers.services.services import getAllImages

#función muestra la página de inicio:

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
#def home(request):

from django.shortcuts import render
from .layers.services import services  

def home(request):
    images = services.getAllImages()  
    favourite_list = [] 

    return render(request, 'home.html', {
        'images': images,
        'favourite_list': favourite_list
    })


# función utilizada en el buscador:

def search(request):
    name = request.POST.get('query', '')

    if name != '':
        images = services.filterByCharacter(name)
        favourite_list = []  

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })
    else:
        return redirect('home')


# función utilizada para filtrar por el tipo del Pokemon:

def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = services.filterByType(type)  
        favourite_list = [] 

        return render(request, 'home.html', {
            'images': images,
            'favourite_list': favourite_list
        })
    else:
        return redirect('home')

#funcion utilizada para guardar pokemones en la lista de favoritos:

from django.shortcuts import redirect
from django.contrib import messages

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        name = request.POST.get('name')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        base_experience = request.POST.get('base_experience')
        types = request.POST.getlist('types[]')
        image = request.POST.get('image')

        # Validación
        if not item_id or not name:
            messages.error(request, 'Datos incompletos.')
            return redirect('home')

        #FALTA validar que no se agreguen pokemones ya en la lista de favoritos 

        # Crear el favorito
        favorito= Favourite.objects.create(
            id=item_id,
            name=name,
            height=height,
            weight=weight,
            base_experience=base_experience,
            types=types,
            image=image,
            user=request.user
        )
        
        messages.success(request, 'Favorito guardado con éxito')

    return redirect("home")

# Estas funciones se usan cuando el usuario está logueado en la aplicación.

#funcion filtra los pokemones para obtener la lista de los favoritos del usuario:

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Favourite 

@login_required
def getAllFavouritesByUser(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'favourites.html', {'favourite_list': favourites})

#funcion que elimina el pokemon que le usuario desee borrar de la lista de favoritos:

from app.layers.services import services

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        fav_id = request.POST.get('id')
        success = services.deleteFavourite(request)
        if success:
            messages.success(request, 'Favorito eliminado con éxito')
        else:
            messages.error(request, 'No se pudo eliminar el favorito')
    else:
        messages.error(request, 'Método no permitido')
    return redirect('favoritos')

#funcion para cerrar sesión del usuario:

from django.contrib.auth import logout

@login_required
def exit(request):
    logout(request)
    return redirect('home')

#aca se inseta la funcion de registro:

from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def registro(request):
    if request.user.is_authenticated:
        return redirect('home')  # si ya está logueado, redirige
        
    if request.method == 'POST':
        nombre = request.POST.get('nombre').strip()
        apellido = request.POST.get('apellido').strip()
        usuario = request.POST.get('usuario').strip()
        password = request.POST.get('password')
        email = request.POST.get('email').strip()

        # Validaciones básicas
        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'registro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'registro.html')

        # Crear usuario
        user = User.objects.create_user(
            username=usuario,
            email=email,
            password=password,
            first_name=nombre,
            last_name=apellido,
        )
        user.save()

        # Enviar correo con credenciales
        try:
            send_mail(
                subject='Registro en PokeAPI',
                message=f'Hola {nombre},\n\nTe registraste correctamente en la aplicación.\n\nUsuario: {usuario}\nContraseña: {password}\n\nSaludos!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'Usuario registrado correctamente. Se envió un correo con las credenciales.')
        except Exception as e:
            messages.warning(request, f'Usuario registrado pero no se pudo enviar el correo. Error: {e}')

        return redirect('login')

    return render(request, 'registro.html')