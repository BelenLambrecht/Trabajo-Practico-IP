from django.contrib import admin
from django.urls import include, path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('favourites/', views.getAllFavouritesByUser, name='favourites'),
    path('favourites/save/', views.saveFavourite, name='save_favourite'),
    path('favourites/delete/<int:favourite_id>/', views.deleteFavourite, name='delete_favourite'),
    path('exit/', views.exit, name='exit'),
]

