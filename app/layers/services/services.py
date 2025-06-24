# capa de servicio/lógica de negocio
import difflib
from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
import requests
from app.layers.transport.transport import getAllImages as get_raw_pokemon_list


# función que devuelve un listado de cards. Cada card representa una imagen de la API de Pokemon
#def getAllImages():
    # debe ejecutar los siguientes pasos:
    # 1) traer un listado de imágenes crudas desde la API (ver transport.py)
    # 2) convertir cada img. en una card.
 #   # 3) añadirlas a un nuevo listado que, finalmente, se retornará con todas las card encontradas.
#    pass

def getAllImages():
    pokemon_cards = []
    raw_pokemon_list = get_raw_pokemon_list()

    for data in raw_pokemon_list:
        types = [t['type']['name'] for t in data['types']]

        # Lógica de color según el tipo
        if 'grass' in types:
            border = 'success'   # verde
        elif 'fire' in types:
            border = 'danger'    # rojo
        elif 'water' in types:
            border = 'primary'   # azul
        else:
            border = 'warning'   # naranja

        card = {
            'id': data['id'],
            'name': data['name'].capitalize(),
            'image': data['sprites']['front_default'],
            'types': types,
            'height': data['height'],
            'weight': data['weight'],
            'base': data['base_experience'],
            'border': border
        }

        pokemon_cards.append(card)

    return pokemon_cards
        
# función que filtra según el nombre del pokemon:

def filterByCharacter(name):
    filtered_cards = []
    name = name.lower()

    for card in getAllImages():
        pokemon_name = card['name'].lower()

        # Si el nombre buscado es parte del nombre del Pokémon o es similar
        if name in pokemon_name or difflib.SequenceMatcher(None, name, pokemon_name).ratio() > 0.6:
            filtered_cards.append(card)

    return filtered_cards


# función que filtra las cards según su tipo:

def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        if type_filter.lower() in [t.lower() for t in card['types']]:
            filtered_cards.append(card)

    return filtered_cards


# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

#obtenemos el id para eliminar el pokemon correspondiente:
def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId)

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)