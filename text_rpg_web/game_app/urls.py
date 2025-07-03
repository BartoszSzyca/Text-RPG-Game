from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_glowne, name='menu_glowne'),
    path('nowa_gra/', views.nowa_gra, name='nowa_gra'),
    path('wczytaj_gre/', views.wczytaj_gre, name='wczytaj_gre'),
    path('opcje/', views.opcje_gry, name='opcje_gry'),
    path('scena_las/', views.scena_las, name='scena_las'),
    path('po_walce/', views.wybory_po_walce, name='wybory_po_walce'),
    path('game_over/', views.game_over, name='game_over'),
]